import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';

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

// CSS 주석을 먼저 지운다. 지우지 않으면 /* ... */로 감싸 죽여 둔 선언과 규칙이
// 살아 있는 것으로 읽힌다 — 「있다」와 「산다」가 갈리는 자리다. 같은 이유로
// src/plugins/rehype-svg-steps.mjs도 단계를 세기 전에 SVG 주석을 먼저 지운다.
const CSS = readFileSync('src/styles/global.css', 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
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

// :root 블록에서만 선언을 읽는다. 파일 전체를 훑으면 같은 이름의 나중 선언이 이기므로
// :root 밖의 재선언이 정본 값을 가릴 수 있다 — 이 파일에는 html.rail-pinned와 :has()
// 선택자 안에서 --main-gap을 다시 선언하는 자리가 이미 있다.
const ROOT = [...CSS.matchAll(/:root\s*\{([\s\S]*?)\}/g)].map((m) => m[1]).join('\n');
const css = declarations(ROOT);
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
  assert.match(ROOT, /--dg-bg:\s*var\(--term-bg\);/, '--dg-bg는 --term-bg를 가리켜야 한다');

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

  // 문서의 표에도 같은 hex가 여러 벌 적혀 있고, 위 비교는 코드 블록만 본다. 표가 조용히
  // 거짓말하지 않도록 문서에 나오는 6자리 hex가 전부 팔레트나 레거시 중 하나임을 확인한다.
  // 8자리 예시(#4ade8014)는 여섯 자리 뒤에 단어 경계가 없어 이 정규식에 걸리지 않는다.
  const known = new Set([...TOKENS.map((n) => css.get(n)), ...LEGACY]);
  for (const m of DOC.matchAll(/#[0-9a-f]{6}\b/g)) {
    assert.ok(known.has(m[0]), `문서에 팔레트도 레거시도 아닌 색이 있다: ${m[0]}`);
  }
});

// 규칙을 문자열로 대조한다. 공백을 지워 비교하므로 줄바꿈·들여쓰기가 달라도 통과하고,
// 「어느 hex가 어느 토큰으로 가는가」는 정확히 붙잡는다.
const squash = (text) => text.replace(/\s+/g, '');

// 이 검사가 증명하는 것은 규칙 텍스트가 있다는 것뿐이다. 캐스케이드가 실제로 그 색을
// 전달하는지는 증명하지 않는다 — 같은 특이도의 규칙을 뒤에 더하거나 이 블록을 @media로
// 감싸면 검사는 초록인 채로 매핑이 죽는다. 거기까지 잡으려면 캐스케이드를 흉내내야 하므로
// 여기서 멈추고 한계를 적어 둔다.
test('검사 4 — 팔레트 값마다 fill·stroke 매핑 규칙이 있다', () => {
  const flat = squash(CSS);
  for (const name of TOKENS) {
    const hex = css.get(name);
    for (const prop of ['fill', 'stroke']) {
      const rule = squash(`.svg-steps svg [${prop}="${hex}"] { ${prop}: var(--${name}); }`);
      assert.ok(flat.includes(rule), `${prop} 매핑이 없다: ${hex} → --${name}`);
    }
  }
});

// 단계 도식만 검사한다. 기존 도식 180개를 대상에 넣으면 레거시 116색을 허용
// 목록에 적어야 하고, 그 목록이 검사를 스스로 무력화한다. 새 세대 파일만 조인다.
function steppedSvgs(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...steppedSvgs(full));
    else if (entry.name.toLowerCase().endsWith('-steps.svg')) out.push(full);
  }
  return out;
}

test('검사 3 — 단계 도식은 팔레트 색만, 소문자로만 쓴다', () => {
  const palette = new Set(TOKENS.map((n) => css.get(n)));
  const files = steppedSvgs('public');
  assert.ok(files.length > 0, '검사할 단계 도식이 없으면 이 검사는 아무것도 지키지 않는다');

  for (const file of files) {
    const text = readFileSync(file, 'utf8');
    for (const m of text.matchAll(/#[0-9a-fA-F]{3,8}\b/g)) {
      const value = m[0];
      assert.equal(
        value,
        value.toLowerCase(),
        `${file}: hex를 소문자로 쓴다 (${value}) — 매핑 선택자가 대소문자를 구별한다`,
      );
      assert.ok(palette.has(value), `${file}: 팔레트 밖의 색 ${value}`);
    }
  }
});
