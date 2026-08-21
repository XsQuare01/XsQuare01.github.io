import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// 팔레트의 이름 목록을 이 파일에 손으로 적는다. CSS에서 읽어 오면 「CSS에 있는 것이
// 팔레트다」가 되어 검사가 아무것도 막지 못한다. 토큰을 더하거나 빼려면 이 배열을
// 고쳐야 하고, 그 편집이 결정의 기록이 된다.
const TOKENS = [
  'dg-bg', 'dg-fg', 'dg-fg-soft', 'dg-fg-muted', 'dg-line', 'dg-line-dim', 'dg-surface',
  'dg-green', 'dg-green-soft', 'dg-green-fill',
  'dg-blue', 'dg-blue-soft', 'dg-blue-fill',
  'dg-red', 'dg-red-fill',
  'dg-amber', 'dg-amber-fill',
  'dg-violet',
];

// 설계가 레거시로 판정한 값. 팔레트로 다시 들어오면 실패한다.
const LEGACY = [
  '#f97316', '#34d399', '#22c55e', '#ef4444',
  '#4a5568', '#2d3748', '#1f2937', '#cbd5e0',
];

const CSS = readFileSync('src/styles/global.css', 'utf8');
const DOC = readFileSync('docs/design/DIAGRAM_PALETTE.md', 'utf8');

// `--name: value;` 를 모두 뽑는다. 값이 `var(--other)`면 한 단계 따라간다.
// CSS와 문서에 같은 함수를 쓰므로 「같은 방식으로 읽어서 같아야 한다」가 된다.
function declarations(text) {
  const raw = new Map();
  for (const m of text.matchAll(/--([a-z0-9-]+):\s*([^;]+);/g)) raw.set(m[1], m[2].trim());
  const resolved = new Map();
  for (const [name, value] of raw) {
    const alias = value.match(/^var\(--([a-z0-9-]+)\)$/);
    resolved.set(name, alias ? (raw.get(alias[1]) ?? value) : value);
  }
  return resolved;
}

const css = declarations(CSS);
const doc = declarations(DOC);

test('검사 1 — global.css가 팔레트 18색을 정의한다', () => {
  const found = [...css.keys()].filter((k) => k.startsWith('dg-')).sort();
  assert.deepEqual(found, [...TOKENS].sort(), 'CSS의 --dg-* 목록이 팔레트와 정확히 같아야 한다');

  for (const name of TOKENS) {
    assert.match(
      css.get(name),
      /^#[0-9a-f]{6}$/,
      `--${name}은 소문자 6자리 hex로 해석되어야 한다 (지금: ${css.get(name)})`,
    );
  }

  // 배경은 값을 베끼지 않고 판을 가리켜야 한다. 그래야 판과 도식의 검정이
  // 구조적으로 어긋날 수 없다.
  assert.match(CSS, /--dg-bg:\s*var\(--term-bg\);/, '--dg-bg는 --term-bg를 가리켜야 한다');

  // 두 토큰이 같은 값을 가지면 매핑 규칙이 겹쳐 나중 것이 이긴다. 역할과 값은 1:1이어야 한다.
  const values = TOKENS.map((n) => css.get(n));
  assert.equal(new Set(values).size, TOKENS.length, '팔레트에 같은 값을 쓰는 토큰이 둘 있다');
});

test('검사 1-b — theme-color 메타가 판과 같은 색을 쓴다', () => {
  // theme-color는 --term-bg와 같은 값을 손으로 복제한다(HTML 메타는 CSS 변수를 읽지
  // 못한다). #41에서 둘을 함께 바꿨고, 그때부터 짝을 맞추는 일이 사람 기억에 맡겨져
  // 있었다. 주석이 아니라 검사로 붙잡는다.
  const layout = readFileSync('src/layouts/BaseLayout.astro', 'utf8');
  const meta = layout.match(/name="theme-color" content="(#[0-9a-f]{6})"/);
  assert.ok(meta, 'BaseLayout.astro에 theme-color 메타가 있어야 한다');
  assert.equal(meta[1], css.get('term-bg'), 'theme-color가 --term-bg와 다르다');
});

test('검사 2 — 문서의 팔레트가 CSS와 한 글자도 다르지 않다', () => {
  const docTokens = [...doc.keys()].filter((k) => k.startsWith('dg-')).sort();
  assert.deepEqual(docTokens, [...TOKENS].sort(), '문서 블록의 토큰 목록이 팔레트와 다르다');

  for (const name of TOKENS) {
    assert.equal(doc.get(name), css.get(name), `--${name}이 문서와 CSS에서 다르다`);
  }

  const values = TOKENS.map((n) => css.get(n));
  for (const legacy of LEGACY) {
    assert.ok(!values.includes(legacy), `레거시 색 ${legacy}가 팔레트에 들어왔다`);
  }
});
