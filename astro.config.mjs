import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import katex from 'katex';
import sitemap, { ChangeFreqEnum } from '@astrojs/sitemap';

const BLOG_POST_PATH = /^\/blog\/[^/]+\/?$/;

// 본문 이미지에 lazy-load / async decoding을 부여해 로딩 성능(Core Web Vitals) 개선
function rehypeLazyImages() {
  return (tree) => {
    const walk = (node) => {
      if (node.tagName === 'img') {
        node.properties = node.properties || {};
        if (!('loading' in node.properties)) node.properties.loading = 'lazy';
        if (!('decoding' in node.properties)) node.properties.decoding = 'async';
      }
      if (node.children) node.children.forEach(walk);
    };
    walk(tree);
  };
}

// 본문 이미지(alt 있음)를 figure+figcaption으로 감싸 다크 플레이트 + 캡션 렌더
function rehypeFigureCaption() {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      node.children = node.children.flatMap((child) => {
        // Only wraps a <p> whose SOLE child is an <img alt="...">; a stray whitespace/text
        // node alongside the image (e.g. a newline in the source) will skip wrapping.
        if (
          child.tagName === 'p' &&
          child.children &&
          child.children.length === 1 &&
          child.children[0].tagName === 'img' &&
          child.children[0].properties &&
          child.children[0].properties.alt
        ) {
          const img = child.children[0];
          return [{
            type: 'element', tagName: 'figure', properties: { className: ['post-figure'] },
            children: [
              img,
              { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: img.properties.alt }] },
            ],
          }];
        }
        walk(child);
        return [child];
      });
    };
    walk(tree);
  };
}

// 콜아웃은 raw HTML 블록(<div class="callout">…)이라 remark-math가 내부 $…$를
// 파싱하지 못한다. Astro는 rehype-raw를 사용자 플러그인 이후에 돌리므로, 이 단계에서
// 콜아웃은 아직 'raw' 문자열 노드다. 그 문자열 안의 $…$·$$…$$를 빌드 시 KaTeX로
// 렌더해 넣으면(이후 rehype-raw가 그 HTML을 파싱) 본문 수식과 동일하게 표시된다.
function rehypeCalloutMath() {
  const render = (tex, displayMode) => {
    try {
      return katex.renderToString(tex.trim(), { displayMode, throwOnError: false });
    } catch {
      return null; // 실패 시 원문 유지
    }
  };
  const replaceMath = (s) => {
    let out = s.replace(/\$\$([^$]+?)\$\$/g, (w, t) => render(t, true) ?? w);
    out = out.replace(/\$([^$\n]+?)\$/g, (w, t) => render(t, false) ?? w);
    return out;
  };
  // <code>…</code> / <pre>…</pre> 내부의 $ 는 수식이 아니므로 건드리지 않는다
  const processValue = (value) =>
    value
      .split(/(<code[\s\S]*?<\/code>|<pre[\s\S]*?<\/pre>)/i)
      .map((part, i) => (i % 2 === 1 ? part : replaceMath(part)))
      .join('');
  const walk = (node) => {
    if (node.type === 'raw' && typeof node.value === 'string' && node.value.includes('class="callout')) {
      node.value = processValue(node.value);
    }
    if (node.children) node.children.forEach(walk);
  };
  return (tree) => walk(tree);
}

export default defineConfig({
  site: 'https://xsquare01.github.io',
  integrations: [
    sitemap({
      changefreq: ChangeFreqEnum.WEEKLY,
      priority: 0.7,
      // 통계 유틸리티 페이지는 검색 색인 대상이 아니므로 사이트맵에서 제외
      filter: (page) => !page.endsWith('/stats/') && !page.endsWith('/stats'),
      serialize(item) {
        const { pathname } = new URL(item.url);

        if (pathname === '/') {
          item.changefreq = ChangeFreqEnum.WEEKLY;
          item.priority = 1;
        } else if (BLOG_POST_PATH.test(pathname)) {
          item.changefreq = ChangeFreqEnum.MONTHLY;
          item.priority = 0.85;
        } else if (
          pathname === '/blog/' ||
          pathname.startsWith('/categories/') ||
          pathname.startsWith('/tags/')
        ) {
          item.changefreq = ChangeFreqEnum.WEEKLY;
          item.priority = 0.75;
        }

        return item;
      },
    }),
  ],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeCalloutMath, rehypeKatex, rehypeLazyImages, rehypeFigureCaption],
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark-dimmed',
      },
      defaultColor: false,
    },
  },
});
