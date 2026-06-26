import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime()
  );

  return rss({
    title: 'XsQuare01 학습 노트',
    description: '계산 이론·암호학·알고리즘을 정의부터 증명까지 정리하는 학습 노트',
    site: context.site ?? 'https://xsquare01.github.io',
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description ?? '',
      pubDate: post.data.date,
      link: `/blog/${post.id}/`,
      categories: post.data.tags,
    })),
    customData: '<language>ko</language>',
  });
}
