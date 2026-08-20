import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// publicDir 기본값은 cwd가 아니라 이 파일의 위치를 기준으로 잡는다. astro.config.mjs가
// 항상 저장소 루트에서 실행된다고 가정하지 않기 위해서다 — 다른 디렉터리에서 빌드를
// 호출하면 상대경로 'public'이 조용히 엉뚱한 곳(혹은 존재하지 않는 곳)을 가리키고,
// 그 결과 모든 대상이 "파일이 없다"로 조용히 img로 되돌아간다. 옵션으로 넘긴 값은
// 그대로 path.join에 쓰이므로(테스트의 'test/fixtures'처럼 cwd 기준 상대경로도 그대로
// 동작), 이 기본값 계산이 override를 막지 않는다.
const DEFAULT_PUBLIC_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'public');

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
// 태그를 훑는 두 정규식([^>]* 대신) 모두 이 조각을 쓴다: 겹따옴표로 묶인 속성값
// 안의 '>'는 건너뛰고, 그 밖의 '>'에서만 태그가 끝난다고 본다. quote-unaware하게
// [^>]*로 훑으면 data-step-label="외적 > 0"처럼 값 안에 리터럴 '>'가 들어간 순간
// 여는 태그가 그 '>'에서 잘려 나간다.
//
// 이 코드가 실제로 강제하는 저작 규약(코드 어디에도 안 적혀 있던 것들):
// 1) data-step 그룹은 <svg>의 최상위 자식이어야 한다. 감싸는 <g transform="...">가
//    있으면 그 wrapper는 groupRe에 안 걸려 rest(leftover raw)에 그대로 남고, 안쪽의
//    data-step 그룹들만 뽑혀 나와 wrapper 밖에 다시 붙는다 — transform이 조용히 사라진다.
// 2) 모든 단계에 공통인 내용(배경, 미처리 점, 제목 등)은 파일에서 data-step 그룹보다
//    앞에 와야 한다. 빌더가 rest(leftover raw)를 먼저 넣고 그다음에 그룹들을 붙이므로,
//    공통 내용이 그룹 뒤에 있으면 z-order상 그룹들 밑에 깔려 버린다.
// 3) 허용 목록(viewBox, xmlns, role, aria-label, font-family, preserveAspectRatio)
//    밖의 루트 속성은 조용히 버려진다.
// 4) 엘리먼트 id는 인라인되는 순간 페이지 전역이 된다(예: 이 파일의 <marker id="ss-g">).
//    한 페이지에 단계 도식이 두 개면 id가 충돌한다 — 이 플러그인은 id를 재작성하지 않는다.
const TAG_ATTRS = '(?:[^>"]|"[^"]*")*';

function buildSvg(source, label) {
  const openMatch = source.match(new RegExp(`<svg\\b(${TAG_ATTRS})>`));
  if (!openMatch) return null;
  const attrs = parseAttrs(openMatch[0]);
  const inner = source.slice(openMatch.index + openMatch[0].length, source.lastIndexOf('</svg>'));

  // HTML 주석은 먼저 지운다. 주석 안에 data-step 예시나 초안이 남아 있어도(예:
  // <!-- draft: <g data-step="9" ...>...</g> -->) 그룹 정규식이 이를 실제 단계로
  // 잘못 세지 않도록 하는 것이다. 즉 도식 작성자는 단계를 끄고 싶을 때 주석 처리에
  // 의존하면 안 된다 — 주석은 통째로 사라지고, 남아 있던 실제 <g data-step="n">만
  // 살아남는다는 사실을 알고 있어야 한다.
  const withoutComments = inner.replace(/<!--[\s\S]*?-->/g, '');

  // data-step 그룹을 찾는다. 정규식이 non-greedy([\s\S]*?)이므로 그룹 본문 안에 중첩된
  // <g>가 있으면 그 안쪽의 첫 </g>에서 잘려 나간다 — 즉 data-step 그룹 내부에는
  // 추가 <g>를 두면 안 된다(도식을 만들 때 지켜야 할 제약, 이 태스크에서는 도식을 직접
  // 작성하지 않지만 다음 태스크를 위해 남겨 둔다).
  const groups = [];
  const groupRe = new RegExp(`<g\\b(${TAG_ATTRS}\\bdata-step="\\d+"${TAG_ATTRS})>([\\s\\S]*?)</g>`, 'g');
  let rest = withoutComments;
  for (const m of withoutComments.matchAll(groupRe)) {
    groups.push({ attrs: parseAttrs(`<g ${m[1]}>`), body: m[2] });
    rest = rest.replace(m[0], '');
  }
  if (groups.length === 0) return null;

  // groupRe 자신은 몇 개를 놓쳤는지 알 도리가 없다 — 애초에 그 개수만 있었는지,
  // 홑따옴표 속성(data-step='3')이나 잘못된 값(data-step="1a")이라 못 뽑아낸
  // 그룹이 있는지 구별할 수 없기 때문이다. 그래서 원문에서 data-step 속성이
  // (따옴표 종류·값 유효성과 무관하게) 실제로 몇 번 나오는지 별도로 세어 비교한다.
  // 둘이 다르면 잘못된 결과를 조용히 내보내는 대신 img로 안전하게 되돌아간다.
  const dataStepAttrCount =
    (withoutComments.match(/\bdata-step\s*=\s*(?:"[^"]*"|'[^']*')/g) || []).length;
  if (groups.length !== dataStepAttrCount) return null;

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
      ...(attrs.preserveAspectRatio ? { preserveAspectRatio: attrs.preserveAspectRatio } : {}),
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

export function rehypeSvgSteps({ publicDir = DEFAULT_PUBLIC_DIR } = {}) {
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
