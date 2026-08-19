import { readFileSync } from 'node:fs';
import path from 'node:path';

// 대상 판별은 wrapper 클래스가 아니라 파일명 규약(-steps.svg)으로 한다.
// Astro는 rehype-raw를 사용자 rehype 플러그인 뒤에 돌리므로, 마크다운에 쓴 raw HTML
// wrapper(예: <div class="...">)는 이 단계에서 아직 파싱되지 않은 'raw' 문자열 노드다
// (astro.config.mjs의 rehypeCalloutMath가 콜아웃을 문자열로 다루는 것과 같은 이유).
// 그래서 className으로는 찾을 수 없고, <img src="...-steps.svg">라는 평범한 마크다운
// 이미지 문법으로만 대상을 찾는다. rehypeFigureCaption이 바로 앞 단계에서 img를
// <figure class="post-figure">(img, figcaption)</figure>로 감싸 두므로, 그 안의 img만 본다.
const STEPS_SUFFIX = '-steps.svg';

// <tag a="1" b="2"> 의 속성을 뽑는다. 값은 항상 겹따옴표로 쓴다(우리 SVG 규약).
function parseAttrs(openTag) {
  const attrs = {};
  for (const m of openTag.matchAll(/([a-zA-Z-]+)="([^"]*)"/g)) attrs[m[1]] = m[2];
  return attrs;
}

// 자식은 그대로 문자열로 넘긴다. rehype-raw 이후 단계이므로 raw 노드가 그대로 직렬화된다.
function raw(value) {
  return { type: 'raw', value };
}

// source(svg 파일 전체 텍스트)에서 최상위 data-step 그룹만 뽑아 최소 hast 구조로 다시
// 세운다. 도식이 우리가 직접 쓴 SVG이므로 임의 SVG 파서가 필요하지 않다.
// 그룹이 하나도 없으면 null을 돌려주고, 호출자는 원래의 <img>를 그대로 둔다.
function buildSvg(source, label) {
  const openMatch = source.match(/<svg\b([^>]*)>/);
  if (!openMatch) return null;
  const attrs = parseAttrs(openMatch[0]);
  const inner = source.slice(openMatch.index + openMatch[0].length, source.lastIndexOf('</svg>'));

  // data-step 그룹을 찾는다. 정규식이 non-greedy([\s\S]*?)이므로 그룹 본문 안에 중첩된
  // <g>가 있으면 그 안쪽의 첫 </g>에서 잘려 나간다 — 즉 data-step 그룹 내부에는
  // 추가 <g>를 두면 안 된다(도식을 만들 때 지켜야 할 제약, 이 태스크에서는 도식을 직접
  // 작성하지 않지만 다음 태스크를 위해 남겨 둔다).
  const groups = [];
  const groupRe = /<g\b([^>]*\bdata-step="\d+"[^>]*)>([\s\S]*?)<\/g>/g;
  let rest = inner;
  for (const m of inner.matchAll(groupRe)) {
    groups.push({ attrs: parseAttrs(`<g ${m[1]}>`), body: m[2] });
    rest = rest.replace(m[0], '');
  }
  if (groups.length === 0) return null;

  const children = [raw(rest)];
  for (const g of groups) {
    children.push({
      type: 'element',
      tagName: 'g',
      properties: {
        'data-step': g.attrs['data-step'],
        'data-step-label': g.attrs['data-step-label'] || '',
      },
      children: [raw(g.body)],
    });
  }

  return {
    type: 'element',
    tagName: 'svg',
    properties: {
      viewBox: attrs.viewBox,
      xmlns: 'http://www.w3.org/2000/svg',
      role: 'img',
      'aria-label': label,
      ...(attrs['font-family'] ? { 'font-family': attrs['font-family'] } : {}),
    },
    children,
  };
}

// figure의 className에 svg-steps를 더한다(이미 있으면 중복시키지 않는다). 이 클래스가
// 스타일시트와 Task 4의 플레이어 스크립트가 대상을 찾는 훅이 된다.
function addStepsClass(figure) {
  figure.properties = figure.properties || {};
  const existing = Array.isArray(figure.properties.className) ? figure.properties.className : [];
  if (!existing.includes('svg-steps')) {
    figure.properties.className = [...existing, 'svg-steps'];
  }
}

export function rehypeSvgSteps({ publicDir = 'public' } = {}) {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;

      if (node.tagName === 'figure') {
        node.children = node.children.map((leaf) => {
          if (leaf.tagName !== 'img') return leaf;
          const src = leaf.properties?.src;
          if (typeof src !== 'string' || !src.toLowerCase().endsWith(STEPS_SUFFIX)) return leaf;

          let source;
          try {
            source = readFileSync(path.join(publicDir, src.replace(/^\//, '')), 'utf8');
          } catch {
            return leaf; // 파일이 없거나 읽을 수 없으면 지금 동작(img)으로 되돌아간다
          }

          const svg = buildSvg(source, leaf.properties.alt || '');
          if (!svg) return leaf; // data-step 그룹이 없으면 교체하지 않는다

          addStepsClass(node);
          return svg;
        });
      }

      node.children.forEach(walk);
    };
    walk(tree);
  };
}
