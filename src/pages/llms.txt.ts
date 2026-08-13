import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import { categories, getCategoryLabel, HOME_FEATURED } from '../data/categories';

/**
 * llms.txt — AI에게 사이트를 소개하는 마크다운 안내문 (llmstxt.org 제안 형식).
 *
 * 사이트맵의 복제본이 아니라 큐레이션된 안내문을 지향한다. 전체 목록을 그대로 부으면
 * 모델이 무엇부터 읽어야 할지 판단할 근거가 없어진다. 그래서 대표 글은 설명과 함께
 * 본문에 싣고, 나머지는 제목만 ## Optional 아래로 내린다. Optional은 형식 규약상
 * "짧은 맥락만 필요하면 건너뛰어도 되는 부분"을 뜻한다.
 *
 * 대표성 판단은 categories.ts의 HOME_FEATURED와 featured를 그대로 쓴다. 홈에서 사람에게
 * 먼저 권하는 글과 기계에게 먼저 권하는 글이 다를 이유가 없고, 목록을 두 벌 관리하면
 * 반드시 어긋난다.
 *
 * public/에 정적 파일로 두지 않고 엔드포인트로 만든 이유도 같다. 손으로 관리하는 목록은
 * 낡는다. rss.xml.ts, search-index.json.ts와 같은 방식으로 콘텐츠에서 생성한다.
 */
export async function GET(context: APIContext) {
  const site = (context.site ?? new URL('https://xsquare01.github.io')).toString().replace(/\/$/, '');

  const posts = (await getCollection('posts')).sort(
    (a, b) => b.data.date.getTime() - a.data.date.getTime()
  );
  const byId = new Map(posts.map((p) => [p.id, p]));

  // 큐레이션 목록의 오타를 조용히 넘기면 링크가 소리 없이 사라진다. 빌드에서 바로 깬다.
  const resolve = (ids: string[], where: string) =>
    ids.map((id) => {
      const post = byId.get(id);
      if (!post) throw new Error(`llms.txt: ${where}의 대표 글 '${id}'에 해당하는 글이 없습니다.`);
      return post;
    });

  const activeCategories = categories.filter((cat) =>
    posts.some((p) => p.data.category === cat.slug)
  );

  const fmtDate = (d: Date) => d.toISOString().slice(0, 10);
  const clean = (s?: string) => s?.replace(/\s+/g, ' ').trim() ?? '';

  /** 대표 글 — 무엇에 관한 글인지 판단할 수 있도록 설명과 날짜를 붙인다. */
  const detailed = (post: (typeof posts)[number]) =>
    `- [${post.data.title}](${site}/blog/${post.id}/) — ${clean(post.data.description)} (${fmtDate(post.data.date)})`;

  /** Optional 목록 — 존재를 알리는 것이 목적이므로 제목과 링크만 싣는다. */
  const brief = (post: (typeof posts)[number]) =>
    `- [${post.data.title}](${site}/blog/${post.id}/)`;

  const featuredIds = new Set<string>(HOME_FEATURED);
  const sections: string[] = [];

  for (const cat of activeCategories) {
    const inCat = posts.filter((p) => p.data.category === cat.slug);
    const picks = resolve(cat.featured ?? [], cat.label);
    picks.forEach((p) => featuredIds.add(p.id));

    sections.push(
      [
        `## ${cat.label}`,
        '',
        clean(cat.intro ?? cat.description),
        '',
        `전체 ${inCat.length}편 — [${cat.label} 글 목록](${site}/categories/${cat.slug}/)`,
        '',
        '대표 글 (읽기 권장 순서):',
        '',
        ...picks.map(detailed),
        '',
      ].join('\n')
    );
  }

  const rest = posts.filter((p) => !featuredIds.has(p.id));

  const body = [
    '# XsQuare01 학습 노트',
    '',
    '> 계산 이론·암호학·알고리즘을 정의부터 증명까지 직접 풀어 정리하는 한국어 학습 노트입니다.',
    '> 결론만 옮기지 않고, 그 결론에 이르는 논증을 정의·정리·증명 형태로 끝까지 씁니다.',
    '',
    `총 ${posts.length}편, ${activeCategories.length}개 주제. 모든 글은 한국어로 작성되어 있습니다.`,
    '',
    // 사이트 식별 정보를 링크 안에만 두면 안내문을 읽는 쪽이 출처·연락처를 따로 추출해야 한다.
    // 이름·URL·언어·저자·연락처를 앞에 명시해 문서 자체로 완결되게 한다.
    '## 사이트 정보',
    '',
    `- 이름: XsQuare01 학습 노트`,
    `- 사이트: ${site}/`,
    `- 설명: 계산 이론·암호학·알고리즘을 정의부터 증명까지 정리하는 한국어 학습 노트`,
    `- 언어: 한국어 (ko)`,
    `- 저자: XsQuare01`,
    `- 연락처: https://github.com/XsQuare01`,
    `- 사이트 소개: ${site}/ (홈에 다루는 주제와 대표 글을 정리해 두었습니다)`,
    `- 전체 글 색인: ${site}/blog/`,
    `- 변경 알림: ${site}/rss.xml`,
    '',
    '## 이 노트의 성격',
    '',
    '- 각 글은 하나의 개념 또는 알고리즘을 다루며, 강한 주장에는 증명을 붙입니다.',
    '- 알고리즘 글은 의사코드와 복잡도 분석을 함께 싣고, 비용 모델을 밝힙니다.',
    '- 시리즈로 이어지는 글이 많아 앞 글을 먼저 읽어야 하는 경우가 있습니다.',
    '',
    '## 먼저 읽을 글',
    '',
    '사이트 전체를 대표하는 글입니다. 이 노트가 어떤 깊이로 쓰였는지 여기서 판단할 수 있습니다.',
    '',
    ...resolve(HOME_FEATURED, '사이트 대표').map(detailed),
    '',
    ...sections,
    '## 그 밖의 자료',
    '',
    `- [전체 글 목록](${site}/blog/)`,
    `- [카테고리](${site}/categories/)`,
    `- [태그](${site}/tags/)`,
    `- [RSS](${site}/rss.xml)`,
    '',
    '## Optional',
    '',
    `위 대표 글에 포함되지 않은 나머지 ${rest.length}편입니다. 짧은 맥락만 필요하면 건너뛰어도 됩니다.`,
    '',
    ...activeCategories.flatMap((cat) => {
      const inCat = rest.filter((p) => p.data.category === cat.slug);
      if (inCat.length === 0) return [];
      return [`### ${getCategoryLabel(cat.slug)}`, '', ...inCat.map(brief), ''];
    }),
  ].join('\n');

  return new Response(body, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}
