import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
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
    rehypePlugins: [rehypeKatex, rehypeLazyImages],
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark-dimmed',
      },
      defaultColor: false,
    },
  },
});
