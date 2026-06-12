import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import sitemap, { ChangeFreqEnum } from '@astrojs/sitemap';

const BLOG_POST_PATH = /^\/blog\/[^/]+\/?$/;

export default defineConfig({
  site: 'https://xsquare01.github.io',
  integrations: [
    sitemap({
      changefreq: ChangeFreqEnum.WEEKLY,
      priority: 0.7,
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
    rehypePlugins: [rehypeKatex],
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark-dimmed',
      },
      defaultColor: false,
    },
  },
});
