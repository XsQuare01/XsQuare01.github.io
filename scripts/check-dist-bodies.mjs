// astro build 뒤 dist/blog/**/index.html을 훑어, 각 글의 <article> 본문이 실수로
// 텅 비지 않았는지 확인한다. 예전에 플러그인 등록이 잘못돼 발행 글 본문이 통째로
// 사라진 적이 있는데, 그때 astro build·npm run test:js·게이트가 모두 초록이었고
// 사람이 dist를 눈으로 봐서야 발견됐다. 그 사고를 다시 사람 눈에만 맡기지 않도록,
// npm run build 뒤에 자동으로 도는 검사 하나를 둔다.
//
// dist/blog/index.html(글 목록 페이지)은 마크업이 다르므로(article이 없다) 건너뛴다.
import { readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DIST_BLOG = path.join(REPO_ROOT, 'dist', 'blog');
const LISTING_PAGE = path.join(DIST_BLOG, 'index.html');
const FLOOR = 800; // 실측한 가장 짧은 실제 글 본문이 3172자라 여유가 넓다

function findIndexHtmlFiles(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...findIndexHtmlFiles(full));
    else if (entry.isFile() && entry.name === 'index.html') out.push(full);
  }
  return out;
}

// <article>...</article>의 내용만 뽑아 태그를 지우고 공백을 접는다. 첫 <article>과
// 그다음에 나오는 첫 </article>을 짝으로 본다 — 이 저장소의 페이지 하나당 article은
// 하나뿐이므로 중첩을 걱정할 필요가 없다.
function extractArticleText(html) {
  const openStart = html.indexOf('<article');
  if (openStart === -1) return null;
  const openEnd = html.indexOf('>', openStart);
  if (openEnd === -1) return null;
  const closeStart = html.indexOf('</article>', openEnd);
  if (closeStart === -1) return null;
  const inner = html.slice(openEnd + 1, closeStart);
  return inner.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

const files = findIndexHtmlFiles(DIST_BLOG).filter((f) => f !== LISTING_PAGE);

const failures = [];
for (const file of files) {
  const html = readFileSync(file, 'utf8');
  const text = extractArticleText(html);
  const len = text === null ? 0 : text.length;
  if (text === null || len < FLOOR) {
    failures.push({ file: path.relative(REPO_ROOT, file), len, missing: text === null });
  }
}

if (failures.length > 0) {
  console.error(`dist 본문 검사 실패: <article> 본문이 ${FLOOR}자 미만인 페이지 ${failures.length}개`);
  for (const { file, len, missing } of failures) {
    console.error(`  - ${file}: ${missing ? '<article> 태그를 찾지 못함' : `${len}자`}`);
  }
  process.exit(1);
}

console.log(`dist 본문 검사 통과: 글 ${files.length}개 모두 <article> 본문 ${FLOOR}자 이상`);
