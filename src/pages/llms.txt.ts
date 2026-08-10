import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import { categories, getCategoryLabel } from '../data/categories';

/**
 * llms.txt — AI에게 사이트를 소개하는 마크다운 요약 (llmstxt.org 제안 형식).
 *
 * public/에 정적 파일로 두지 않고 엔드포인트로 만든 이유: 글 목록을 손으로 관리하면
 * 반드시 낡는다. rss.xml.ts, search-index.json.ts와 같은 방식으로 콘텐츠 컬렉션에서
 * 생성해 글이 늘어도 자동으로 따라온다.
 */
export async function GET(context: APIContext) {
  const site = (context.site ?? new URL('https://xsquare01.github.io')).toString().replace(/\/$/, '');

  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime()
  );

  // 글이 하나도 없는 카테고리는 목차에 넣지 않는다 — 빈 링크는 안내가 아니라 소음이다.
  const activeCategories = categories.filter((cat) =>
    posts.some((p) => p.data.category === cat.slug)
  );

  const fmtDate = (d: Date) => d.toISOString().slice(0, 10);

  const line = (post: (typeof posts)[number]) => {
    const desc = post.data.description?.replace(/\s+/g, ' ').trim();
    const meta = [getCategoryLabel(post.data.category ?? ''), fmtDate(post.data.date)]
      .filter(Boolean)
      .join(', ');
    return `- [${post.data.title}](${site}/blog/${post.id}/) — ${desc ? `${desc} ` : ''}(${meta})`;
  };

  const sections = activeCategories.map((cat) => {
    const inCat = posts.filter((p) => p.data.category === cat.slug);
    return [
      `## ${cat.label} (${inCat.length}편)`,
      '',
      cat.description.replace(/\n/g, ' '),
      '',
      ...inCat.map(line),
      '',
    ].join('\n');
  });

  const body = [
    '# XsQuare01 학습 노트',
    '',
    '> 계산 이론·암호학·알고리즘을 정의부터 증명까지 직접 풀어 정리하는 한국어 학습 노트입니다.',
    '> 결론만 옮기지 않고, 그 결론에 이르는 논증을 정의·정리·증명 형태로 끝까지 씁니다.',
    '',
    `총 ${posts.length}편, ${activeCategories.length}개 주제. 모든 글은 한국어로 작성되어 있습니다.`,
    '',
    '## 이 노트의 성격',
    '',
    '- 각 글은 하나의 개념 또는 알고리즘을 다루며, 강한 주장에는 증명을 붙입니다.',
    '- 알고리즘 글은 의사코드와 복잡도 분석을 함께 싣고, 비용 모델을 밝힙니다.',
    '- 시리즈로 이어지는 글이 많아 앞 글을 먼저 읽어야 하는 경우가 있습니다.',
    '',
    ...sections,
    '## 그 밖의 자료',
    '',
    `- [전체 글 목록](${site}/blog/)`,
    `- [카테고리](${site}/categories/)`,
    `- [태그](${site}/tags/)`,
    `- [RSS](${site}/rss.xml)`,
    '',
  ].join('\n');

  return new Response(body, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}
