# 도판 팔레트 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 도식 181개가 쓰는 116색에 역할 이름을 붙여 18색 팔레트로 정하고, 그 팔레트가 문서·CSS·단계 도식에서 어긋나지 않도록 검사로 묶는다.

**Architecture:** 팔레트 값은 `global.css`의 `--dg-*` 토큰과 `docs/design/DIAGRAM_PALETTE.md`의 표에 두 벌 존재하고, `test/palette.test.mjs`가 둘을 대조한다. 인라인된 단계 도식에는 **속성값 선택자**(`[fill="#4ade80"] { fill: var(--dg-green) }`)로 토큰을 얹으므로 SVG 파일은 바뀌지 않는다. 기존 도식 180개의 색은 옮기지 않고 레거시로 문서에 남긴다.

**Tech Stack:** Astro 6, 순수 CSS 커스텀 프로퍼티, node 내장 테스트 러너(`node --test`, 외부 의존 없음), GitHub Actions

**Spec:** `docs/superpowers/specs/2026-08-21-diagram-palette-design.md`

## Global Constraints

- 커밋에 `Co-Authored-By` 트레일러를 넣지 않는다.
- 모든 작업을 `feat/diagram-palette` 브랜치에서 한다. main에 직접 커밋하지 않는다.
- 새 의존성을 추가하지 않는다. 테스트는 node 내장 모듈만 쓴다(`node:test`, `node:assert/strict`, `node:fs`, `node:path`).
- hex는 **소문자 6자리**로만 쓴다. 매핑 선택자가 대소문자를 구별하기 때문이다.
- 문서 문장은 `docs/writing-rules.md`의 「바른 문장 쓰기」를 적용한다. 접속어를 최소화한다.
- 기존 도식 180개의 색을 바꾸지 않는다. 바꾸는 파일은 `public/images/convex-hull-2/scan-steps.svg` 하나뿐이다.
- 팔레트 18색의 값은 아래 표가 정본이다. 어느 파일에서도 이 값과 다르게 쓰지 않는다.

| 토큰 | 값 | 토큰 | 값 |
| --- | --- | --- | --- |
| `--dg-bg` | `var(--term-bg)` → `#0f1117` | `--dg-blue` | `#3b82f6` |
| `--dg-fg` | `#e2e8f0` | `--dg-blue-soft` | `#93c5fd` |
| `--dg-fg-soft` | `#cbd5e1` | `--dg-blue-fill` | `#1e3a5f` |
| `--dg-fg-muted` | `#94a3b8` | `--dg-red` | `#f87171` |
| `--dg-line` | `#64748b` | `--dg-red-fill` | `#7c2d12` |
| `--dg-line-dim` | `#475569` | `--dg-amber` | `#fbbf24` |
| `--dg-surface` | `#1e293b` | `--dg-amber-fill` | `#3a2c0f` |
| `--dg-green` | `#4ade80` | `--dg-violet` | `#a78bfa` |
| `--dg-green-soft` | `#6ee7b7` | | |
| `--dg-green-fill` | `#14352b` | | |

---

### Task 1: 팔레트 토큰·문서와 둘을 대조하는 검사

`--term-bg`를 도식 쪽 값으로 바꾸는 일이 이 태스크에 함께 들어간다. 팔레트의 `bg`가 `#0f1117`이고 문서도 그 값을 적으므로, 배경 정합이 먼저 되지 않으면 검사 1·2가 통과할 수 없다.

**Files:**
- Create: `test/palette.test.mjs`
- Create: `docs/design/DIAGRAM_PALETTE.md`
- Modify: `src/styles/global.css` (`:root` 안 `--term-bg` 값 한 줄, `--term-green` 뒤에 `--dg-*` 블록)
- Modify: `docs/design/DESIGN_DIRECTION.md` (§3 끝에 포인터 한 줄)
- Modify: `package.json` (`test:js`에 새 테스트 경로 추가)

**Interfaces:**
- Consumes: 없음. 첫 태스크다.
- Produces: `test/palette.test.mjs`가 내보내는 것은 없다. 다음 태스크가 이 파일에 테스트를 **덧붙인다.** 파일 상단의 상수 `TOKENS`(문자열 배열, `dg-` 접두어 없는 이름 18개), `LEGACY`(레거시 hex 8개), 헬퍼 `declarations(text)`(→ `Map<name, resolvedValue>`), 상수 `CSS`·`DOC`(파일 텍스트), `css`·`doc`(각각 `declarations()` 결과)를 Task 2·3이 그대로 쓴다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`test/palette.test.mjs`를 만든다.

```js
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
```

이 파서는 계획을 쓰는 동안 실제 `global.css`에 돌려 확인했다. 선언 37개를 뽑고 `--term-bg`를 `#15171c`로 읽으며, 별칭(`--amber: var(--ink-blue)`)을 `#1c3d5c`로 따라간다. 마크다운에 돌리면 코드 블록의 선언만 뽑고 산문·표 안의 `` `--dg-bg` `` 언급이나 레거시 표의 hex는 잡지 않는다. `squash` 비교는 줄바꿈·들여쓰기가 달라도 통과한다.

- [ ] **Step 2: 실패를 확인한다**

Run: `node --test test/palette.test.mjs`
Expected: FAIL. `docs/design/DIAGRAM_PALETTE.md`가 없어 `readFileSync`가 `ENOENT`로 던진다.

- [ ] **Step 3: `--term-bg`를 도식 쪽 값으로 바꾼다**

`src/styles/global.css` 38행:

```css
  --term-bg: #0f1117;
```

바로 위에 이유를 남긴다.

```css
  /* 도식 181개가 자기 배경으로 #0f1117을 칠한다. 판이 #15171c였을 때는 도판마다
     옅은 안쪽 패널이 한 겹 더 보였다(대비 1.1:1). 도식 쪽을 밝히면 그 안의 색이
     모두 이 값 위에서 골라진 것이라 181개의 내부 대비가 흔들리므로, 판을 도식에
     맞춘다. 영향받는 곳은 .prose pre · .astro-code · .post-figure 셋이다. */
  --term-bg: #0f1117;
```

- [ ] **Step 4: 팔레트 토큰을 넣는다**

`src/styles/global.css`의 `--term-green: #6fc07a;` 다음 줄에 빈 줄을 두고 붙인다.

```css
  /* 도판 팔레트 — 크롬에서 색은 장식이라 하나면 되지만, 도판 안에서 색은 데이터다.
     채택·거부·현재를 괘선이나 번호로 대신할 수 없다. 대신 역할 이름이 없는 색은
     쓰지 않고 계열을 다섯에서 멈춘다. 값·쓰임·대비의 정본은
     docs/design/DIAGRAM_PALETTE.md이고, test/palette.test.mjs가 둘을 대조한다.
     배경은 값을 베끼지 않고 판을 그대로 가리켜, 판과 도식의 검정이 어긋날 수 없게 한다. */
  --dg-bg: var(--term-bg);
  --dg-fg: #e2e8f0;
  --dg-fg-soft: #cbd5e1;
  --dg-fg-muted: #94a3b8;
  --dg-line: #64748b;
  --dg-line-dim: #475569;
  --dg-surface: #1e293b;
  --dg-green: #4ade80;
  --dg-green-soft: #6ee7b7;
  --dg-green-fill: #14352b;
  --dg-blue: #3b82f6;
  --dg-blue-soft: #93c5fd;
  --dg-blue-fill: #1e3a5f;
  --dg-red: #f87171;
  --dg-red-fill: #7c2d12;
  --dg-amber: #fbbf24;
  --dg-amber-fill: #3a2c0f;
  --dg-violet: #a78bfa;
```

- [ ] **Step 5: 팔레트 문서를 쓴다**

`docs/design/DIAGRAM_PALETTE.md`를 만든다. 첫 코드 블록이 검사 2의 대상이다 — `--name: value;` 열여덟 줄이 정확히 이 형태로 있어야 한다.

````markdown
# 도판 팔레트

- 정본: 이 문서와 `src/styles/global.css`의 `--dg-*`. `test/palette.test.mjs`가 둘을 대조한다.
- 설계: `docs/superpowers/specs/2026-08-21-diagram-palette-design.md`
- 이 문서는 **도판 내부** 팔레트다. 사이트의 다크 모드 팔레트(`DESIGN_DIRECTION.md` §5의 미결 항목)와 다르다.

## 원칙

크롬에서 색은 장식이라 하나면 된다. **도판 안에서 색은 데이터다** — 채택·거부·현재를 괘선이나 번호로 대신할 수 없다. 대신 대가를 치른다. 역할 이름이 없는 색은 쓰지 않고, 계열을 다섯에서 멈춘다. 여섯 번째 뜻이 필요하면 색이 아니라 모양·굵기·점선으로 가른다.

## 값 (18색)

```css
--dg-bg: #0f1117;
--dg-fg: #e2e8f0;
--dg-fg-soft: #cbd5e1;
--dg-fg-muted: #94a3b8;
--dg-line: #64748b;
--dg-line-dim: #475569;
--dg-surface: #1e293b;
--dg-green: #4ade80;
--dg-green-soft: #6ee7b7;
--dg-green-fill: #14352b;
--dg-blue: #3b82f6;
--dg-blue-soft: #93c5fd;
--dg-blue-fill: #1e3a5f;
--dg-red: #f87171;
--dg-red-fill: #7c2d12;
--dg-amber: #fbbf24;
--dg-amber-fill: #3a2c0f;
--dg-violet: #a78bfa;
```

`global.css`는 `--dg-bg`를 `var(--term-bg)`로 정의한다. 판과 도식의 검정이 어긋날 수 없게 하려는 것이고, 해석된 값은 위와 같다.

## 구조 7 — 모든 도식에 있는 것

| 토큰 | 값 | 대비 | 어디에 쓰는가 |
| --- | --- | --- | --- |
| `--dg-bg` | `#0f1117` | 기준 | 도식 전체의 판. 파일마다 첫 `rect`. |
| `--dg-fg` | `#e2e8f0` | 15.3:1 | 제목, 점 이름, 값. 반드시 읽어야 하는 글자. |
| `--dg-fg-soft` | `#cbd5e1` | 12.7:1 | 표 안의 값처럼 읽어야 하지만 주역은 아닌 글자. |
| `--dg-fg-muted` | `#94a3b8` | 7.4:1 | 범례, 단위, 부연. 미처리 점. |
| `--dg-line` | `#64748b` | 4.0:1 | 좌표축, 구분선, 화살표 몸통, 도형 경계. |
| `--dg-line-dim` | `#475569` | 2.5:1 | 격자, 보조선. **3:1 미달이므로 뜻을 지는 선에 쓰지 않는다.** |
| `--dg-surface` | `#1e293b` | 1.3:1 | 스택 상자, 표 칸, 패널 배경. 위에 `fg`·`fg-soft`를 얹는다. |

## 의미 11 — 뜻을 지는 색

계열마다 `선·글자` / `옅은 짝` / `채운 영역` 셋을 넘지 않는다. 채움은 대비가 1.4~2.0:1이므로 **글자를 얹지 않고** 영역 표시로만 쓴다.

| 계열 | 뜻 | 선·글자 | 옅은 | 채움 |
| --- | --- | --- | --- | --- |
| 초록 | 채택·확정 | `--dg-green` `#4ade80` (10.8:1) | `--dg-green-soft` `#6ee7b7` (12.4:1) | `--dg-green-fill` `#14352b` (1.4:1) |
| 파랑 | 현재·주목 | `--dg-blue` `#3b82f6` (5.1:1) | `--dg-blue-soft` `#93c5fd` (10.5:1) | `--dg-blue-fill` `#1e3a5f` (1.6:1) |
| 빨강 | 거부·실패 | `--dg-red` `#f87171` (6.8:1) | — | `--dg-red-fill` `#7c2d12` (2.0:1) |
| 앰버 | 경고·강조 | `--dg-amber` `#fbbf24` (11.3:1) | — | `--dg-amber-fill` `#3a2c0f` (1.4:1) |
| 보라 | 네 번째 범주 | `--dg-violet` `#a78bfa` (6.9:1) | — | — |

`--dg-blue`는 5.1:1이라 작은 글자에 쓰지 않는다. 파랑 요소의 라벨은 `--dg-blue-soft`로 쓴다. 빨강과 앰버에 옅은 짝을 두지 않은 이유는 기본값의 대비가 이미 충분해 라벨에 그대로 쓸 수 있기 때문이다.

보라는 초록·파랑·빨강으로 가를 수 없을 때만 꺼낸다. 집합 구분, 두 번째 자료구조, 보류 상태가 그 경우다.

## 저작 규칙

- hex는 **소문자 6자리**로만 쓴다. 인라인 도식의 매핑 선택자가 대소문자를 구별한다.
- `*-steps.svg`는 팔레트 밖의 색을 쓸 수 없다. `test/palette.test.mjs`의 검사 3이 막는다.
- 나머지 도식은 검사하지 않는다. 새로 그리는 그림에는 이 팔레트를 쓰고, 기존 그림은 그대로 둔다.
- 채움색 위에 글자를 얹지 않는다. 대비가 2:1 아래다.

## 레거시 8색 — 문서에 남기고 파일은 건드리지 않는다

| 지금 | 현재 | 대체 | 이유 |
| --- | --- | --- | --- |
| `#f97316` | 61파일 | `#fbbf24` | `DESIGN_DIRECTION.md` §4가 이미 걷어내라고 적었다. 대비도 6.7 → 11.3으로 오르고, 오렌지는 빨강과 인접해 「주의」와 「거부」가 붙어 보인다. |
| `#34d399` | 43파일 | `#4ade80` | 같은 역할의 다른 계열(emerald vs green). 채택률이 두 배 높은 쪽을 남긴다. |
| `#22c55e` | 34파일 | `#4ade80` | 같은 계열의 어두운 단계(8.3:1). 두 값을 나눠 쓴 적이 없다. |
| `#ef4444` | 27파일 | `#f87171` | 빨강 두 단계를 구별해 쓴 적이 없다. 대비가 높은 쪽을 남긴다(6.8 대 5.0). |
| `#4a5568` | 29파일 | `#475569` | Tailwind v1 회색 잔재. v3 슬레이트로 통일한다. |
| `#2d3748` | 29파일 | `#1e293b` | 같은 이유. 대비 1.6:1로 면 역할이 겹친다. |
| `#1f2937` | 9파일 | `#1e293b` | 또 다른 회색 계열(gray-800). |
| `#cbd5e0` | 17파일 | `#cbd5e1` | 한 글자 차이의 v1 잔재. 눈으로 구별되지 않는다. |
````

- [ ] **Step 6: 설계 방향 문서에 포인터를 넣는다**

`docs/design/DESIGN_DIRECTION.md`의 §3 색 토큰 마지막 줄(`- **다크 모드 팔레트는 미확정** — 라이트 확정 후 별도로 정한다.`) 다음에 붙인다.

```markdown
- **도판 내부 팔레트는 별도 문서** → `docs/design/DIAGRAM_PALETTE.md`. 위의 다크 모드 팔레트와 다른 것이다. 도판 안에서는 색이 데이터를 지므로(채택·거부·현재) 단색 규율을 그대로 적용하지 않는다. 대신 역할 이름이 없는 색을 금지하고 계열을 다섯에서 멈춘다.
```

- [ ] **Step 7: 테스트를 등록한다**

`package.json`의 `test:js`를 바꾼다.

```json
    "test:js": "node --test src/plugins/rehype-svg-steps.test.mjs test/palette.test.mjs"
```

- [ ] **Step 8: 통과를 확인한다**

Run: `npm run test:js`
Expected: PASS. 검사 1·2 두 개와 기존 플러그인 테스트 16개, 합계 18개가 통과한다.

- [ ] **Step 9: 검사가 실제로 문다는 것을 확인한다**

`docs/design/DIAGRAM_PALETTE.md`의 코드 블록에서 `--dg-green: #4ade80;`을 `--dg-green: #34d399;`로 바꾼 뒤 `npm run test:js`를 돌린다.
Expected: 검사 2가 `--dg-green이 문서와 CSS에서 다르다`로 실패한다.
확인한 뒤 되돌리고 다시 통과를 확인한다.

- [ ] **Step 10: 커밋**

```bash
git add test/palette.test.mjs docs/design/DIAGRAM_PALETTE.md docs/design/DESIGN_DIRECTION.md src/styles/global.css package.json
git commit -m "feat(palette): 도판 팔레트 18색을 정하고 문서와 CSS를 검사로 묶는다"
```

---

### Task 2: 인라인 도식에 토큰을 얹는 매핑과 검사 4

**Files:**
- Modify: `src/styles/global.css` (`.svg-steps.is-live svg g[data-step].is-hidden` 규칙 다음, `@media print` 블록 앞)
- Modify: `test/palette.test.mjs` (검사 4 추가)

**Interfaces:**
- Consumes: Task 1의 `TOKENS`, `CSS`, `css`(`Map<name, hex>`).
- Produces: 헬퍼 `squash(text)` — 공백을 모두 지운 문자열. Task 3은 쓰지 않는다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

`test/palette.test.mjs` 끝에 붙인다.

```js
// 규칙을 문자열로 대조한다. 공백을 지워 비교하므로 줄바꿈·들여쓰기가 달라도 통과하고,
// 「어느 hex가 어느 토큰으로 가는가」는 정확히 붙잡는다.
const squash = (text) => text.replace(/\s+/g, '');

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
```

- [ ] **Step 2: 실패를 확인한다**

Run: `npm run test:js`
Expected: FAIL. `fill 매핑이 없다: #0f1117 → --dg-bg`

- [ ] **Step 3: 매핑 규칙을 넣는다**

`src/styles/global.css`의 `.svg-steps.is-live svg g[data-step].is-hidden { visibility: hidden; }` 다음 줄에 붙인다.

```css
/* 도판 팔레트 매핑 — 인라인된 단계 도식의 프레젠테이션 속성을 토큰으로 덮는다.
   CSS가 프레젠테이션 속성을 이기므로, 인라인되면 토큰이 이기고 <img>로 물러나면
   속성값이 남는다. 그래서 SVG 파일을 한 글자도 고치지 않고 토큰이 닿는다.
   오늘은 토큰 값이 속성값과 같아 시각적으로 no-op이고, 팔레트 값이 바뀌는 날
   인라인 도식이 따라온다. 그게 이 층의 전부다.
   범위를 .svg-steps svg로 한정한 이유는 본문의 다른 요소가 같은 hex를 속성으로
   써도 영향받지 않아야 하기 때문이다. 18색 전부에 fill·stroke 두 규칙을 둔다 —
   예외를 두면 검사가 「어느 값에 어느 규칙이 필요한가」 목록을 알아야 하고,
   그 목록이 다음 드리프트의 자리가 된다. */
.svg-steps svg [fill="#0f1117"] { fill: var(--dg-bg); }
.svg-steps svg [stroke="#0f1117"] { stroke: var(--dg-bg); }
.svg-steps svg [fill="#e2e8f0"] { fill: var(--dg-fg); }
.svg-steps svg [stroke="#e2e8f0"] { stroke: var(--dg-fg); }
.svg-steps svg [fill="#cbd5e1"] { fill: var(--dg-fg-soft); }
.svg-steps svg [stroke="#cbd5e1"] { stroke: var(--dg-fg-soft); }
.svg-steps svg [fill="#94a3b8"] { fill: var(--dg-fg-muted); }
.svg-steps svg [stroke="#94a3b8"] { stroke: var(--dg-fg-muted); }
.svg-steps svg [fill="#64748b"] { fill: var(--dg-line); }
.svg-steps svg [stroke="#64748b"] { stroke: var(--dg-line); }
.svg-steps svg [fill="#475569"] { fill: var(--dg-line-dim); }
.svg-steps svg [stroke="#475569"] { stroke: var(--dg-line-dim); }
.svg-steps svg [fill="#1e293b"] { fill: var(--dg-surface); }
.svg-steps svg [stroke="#1e293b"] { stroke: var(--dg-surface); }
.svg-steps svg [fill="#4ade80"] { fill: var(--dg-green); }
.svg-steps svg [stroke="#4ade80"] { stroke: var(--dg-green); }
.svg-steps svg [fill="#6ee7b7"] { fill: var(--dg-green-soft); }
.svg-steps svg [stroke="#6ee7b7"] { stroke: var(--dg-green-soft); }
.svg-steps svg [fill="#14352b"] { fill: var(--dg-green-fill); }
.svg-steps svg [stroke="#14352b"] { stroke: var(--dg-green-fill); }
.svg-steps svg [fill="#3b82f6"] { fill: var(--dg-blue); }
.svg-steps svg [stroke="#3b82f6"] { stroke: var(--dg-blue); }
.svg-steps svg [fill="#93c5fd"] { fill: var(--dg-blue-soft); }
.svg-steps svg [stroke="#93c5fd"] { stroke: var(--dg-blue-soft); }
.svg-steps svg [fill="#1e3a5f"] { fill: var(--dg-blue-fill); }
.svg-steps svg [stroke="#1e3a5f"] { stroke: var(--dg-blue-fill); }
.svg-steps svg [fill="#f87171"] { fill: var(--dg-red); }
.svg-steps svg [stroke="#f87171"] { stroke: var(--dg-red); }
.svg-steps svg [fill="#7c2d12"] { fill: var(--dg-red-fill); }
.svg-steps svg [stroke="#7c2d12"] { stroke: var(--dg-red-fill); }
.svg-steps svg [fill="#fbbf24"] { fill: var(--dg-amber); }
.svg-steps svg [stroke="#fbbf24"] { stroke: var(--dg-amber); }
.svg-steps svg [fill="#3a2c0f"] { fill: var(--dg-amber-fill); }
.svg-steps svg [stroke="#3a2c0f"] { stroke: var(--dg-amber-fill); }
.svg-steps svg [fill="#a78bfa"] { fill: var(--dg-violet); }
.svg-steps svg [stroke="#a78bfa"] { stroke: var(--dg-violet); }
```

- [ ] **Step 4: 통과를 확인한다**

Run: `npm run test:js`
Expected: PASS. 19개가 통과한다.

- [ ] **Step 5: 매핑을 지우면 검사가 우는지 확인한다**

`.svg-steps svg [stroke="#a78bfa"] { stroke: var(--dg-violet); }` 한 줄을 지우고 `npm run test:js`를 돌린다.
Expected: `stroke 매핑이 없다: #a78bfa → --dg-violet`으로 실패한다.
확인한 뒤 되돌리고 다시 통과를 확인한다.

- [ ] **Step 6: 빌드가 깨지지 않는지 확인한다**

Run: `npm run build`
Expected: 136 페이지가 만들어지고 본문 검사가 통과한다.

- [ ] **Step 7: 커밋**

```bash
git add src/styles/global.css test/palette.test.mjs
git commit -m "feat(palette): 인라인된 단계 도식의 색을 토큰으로 덮는다"
```

---

### Task 3: 단계 도식을 팔레트 안으로 들인다

**Files:**
- Modify: `test/palette.test.mjs` (검사 3 추가)
- Modify: `public/images/convex-hull-2/scan-steps.svg` (레거시 3색 교체)

**Interfaces:**
- Consumes: Task 1의 `TOKENS`, `css`.
- Produces: 없음. 마지막 검사다.

- [ ] **Step 1: 실패하는 테스트를 쓴다**

먼저 `test/palette.test.mjs`의 import 줄을 늘린다. 파일을 훑는 데 두 모듈이 더 필요하다.

```js
import { readFileSync, readdirSync } from 'node:fs';
import path from 'node:path';
```

그다음 파일 끝에 붙인다.

```js
// 단계 도식만 검사한다. 기존 도식 180개를 대상에 넣으면 레거시 116색을 허용
// 목록에 적어야 하고, 그 목록이 검사를 스스로 무력화한다. 새 세대 파일만 조인다.
function steppedSvgs(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...steppedSvgs(full));
    else if (entry.name.endsWith('-steps.svg')) out.push(full);
  }
  return out;
}

test('검사 3 — 단계 도식은 팔레트 색만, 소문자로만 쓴다', () => {
  const palette = new Set(TOKENS.map((n) => css.get(n)));
  const files = steppedSvgs('public/images');
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
```

- [ ] **Step 2: 실패를 확인한다**

Run: `npm run test:js`
Expected: FAIL. `public/images/convex-hull-2/scan-steps.svg: 팔레트 밖의 색 #34d399`

- [ ] **Step 3: 레거시 3색을 교체한다**

`public/images/convex-hull-2/scan-steps.svg`에서 세 값을 모두 바꾼다. 다른 색은 건드리지 않는다.

- `#34d399` → `#4ade80` — 12곳(fill 5, stroke 7). 초록이 살짝 밝아진다(9.8:1 → 10.8:1).
- `#ef4444` → `#f87171` — 5곳(전부 stroke, pop 표시의 ✕와 거부된 경로). 빨강이 살짝 옅어진다(5.0:1 → 6.8:1).
- `#1f2937` → `#1e293b` — 1곳(회색 상자).

교체 후 남은 색이 팔레트의 12개인지 확인한다: `#0f1117` `#e2e8f0` `#94a3b8` `#64748b` `#1e293b` `#4ade80` `#6ee7b7` `#3b82f6` `#93c5fd` `#1e3a5f` `#f87171` `#fbbf24`.

```bash
grep -o '#[0-9a-f]\{6\}' public/images/convex-hull-2/scan-steps.svg | sort -u
```

- [ ] **Step 4: 통과를 확인한다**

Run: `npm run test:js`
Expected: PASS. 20개가 통과한다.

- [ ] **Step 5: 검사가 실제로 문다는 것을 확인한다**

`scan-steps.svg`의 `#4ade80` 한 곳을 `#22c55e`로 바꾸고 `npm run test:js`를 돌린다.
Expected: `팔레트 밖의 색 #22c55e`로 실패한다.
같은 자리를 `#4ADE80`으로 바꾸면 `hex를 소문자로 쓴다`로 실패한다.
둘 다 확인한 뒤 되돌리고 다시 통과를 확인한다.

- [ ] **Step 6: 산출물에 프레젠테이션 속성이 남아 있는지 확인한다**

Run: `npm run build`

그다음:

```bash
grep -c 'stroke="#4ade80"' dist/blog/convex-hull-2/index.html
```

Expected: 0보다 큰 수. 매핑이 속성을 지우지 않고 덮기만 하므로, `<img>`로 물러나도 색이 남는다는 뜻이다.

산출물이 갱신되지 않으면 Astro가 이전 렌더를 캐시에서 쓴 것이다. 이 태스크는 `.md`를 고치지 않으므로 그럴 수 있다. 그때는 `src/content/posts/convex-hull-2.md` 끝에 빈 줄을 넣고 빌드한 뒤 확인하고, 되돌린 뒤 다시 빌드한다.

- [ ] **Step 7: 커밋**

```bash
git add test/palette.test.mjs public/images/convex-hull-2/scan-steps.svg
git commit -m "feat(palette): 단계 도식을 팔레트 안으로 들인다"
```

---

### Task 4: CI가 JS 테스트를 돌리게 한다

지금 CI는 `npm run test:js`를 어디서도 돌리지 않는다. `deploy.yml`은 빌드와 Python 게이트만, `review-gate.yml`은 Python 게이트와 Python 테스트만 돌린다. #236에서 만든 플러그인 테스트 16개도 강제되지 않는 상태다. 팔레트 검사의 거처를 정하는 일이므로 함께 고친다.

**Files:**
- Modify: `.github/workflows/review-gate.yml`

**Interfaces:**
- Consumes: `package.json`의 `test:js`(Task 1에서 갱신됨).
- Produces: 없음.

- [ ] **Step 1: 워크플로에 node 단계를 넣는다**

`.github/workflows/review-gate.yml`의 `actions/setup-python@v5` 블록 다음에 붙인다.

```yaml
      - uses: actions/setup-node@v4
        with:
          node-version: 22
```

- [ ] **Step 2: 테스트 단계를 넣는다**

같은 파일의 마지막 단계(`python -m unittest discover`) 다음에 붙인다.

```yaml
      # 마크다운 파이프라인과 도판 팔레트의 계약을 지키는 테스트. node 내장 러너만
      # 쓰고 외부 의존이 없으므로 npm install이 필요하지 않다. 이 단계가 없으면
      # 플러그인과 팔레트 검사가 초록인 채로 깨질 수 있다.
      - name: 빌드 도구 테스트
        run: npm run test:js
```

- [ ] **Step 3: 워크플로가 문법상 유효한지 확인한다**

```bash
python -c "import yaml,sys; d=yaml.safe_load(open('.github/workflows/review-gate.yml',encoding='utf-8')); print([s.get('name') or s.get('uses') for s in d['jobs']['gate']['steps']])"
```

Expected: 단계 목록이 출력되고 `빌드 도구 테스트`가 마지막에 있다. `actions/setup-node`도 목록에 있어야 한다.

- [ ] **Step 4: 로컬에서 같은 명령이 도는지 확인한다**

`node_modules` 없이도 도는지 확인한다. 테스트가 node 내장 모듈만 쓰므로 설치가 필요하지 않다.

Run: `npm run test:js`
Expected: PASS 20개.

- [ ] **Step 5: 전체 검증**

```bash
npm run test:js
npm run build
python -m pytest .claude -q
python .claude/review_post.py --gate
```

Expected: 차례로 20 통과 · 136 페이지와 본문 검사 통과 · 220 통과 · exit 0.

- [ ] **Step 6: 커밋**

```bash
git add .github/workflows/review-gate.yml
git commit -m "ci: JS 테스트를 게이트 워크플로에 넣는다"
```

---

## 남는 확인 — 브라우저

이 작업에서 브라우저 도구를 쓸 수 없다. 아래는 **논증이 아니라 눈으로** 확인할 항목이고, 리포트에 미관측으로 표시한다.

1. **도판 배경 정합** — 도판 안쪽에 옅은 패널이 한 겹 더 보이던 것이 사라졌는지. 코드블록도 함께 어두워지므로 그쪽도 본다.
2. **테두리** — `.post-figure`의 `#23262e`가 새 바탕에서 어떻게 보이는지(대비 1.19:1 → 1.25:1).
3. **`convex-hull-2`의 단계 도식** — 초록이 밝아지고 빨강이 옅어진 것, 회색 상자가 조금 파래진 것. 빨강은 시안에 없던 변화다.

dev 서버가 떠 있으면 CSS 변경은 즉시 반영되지만, `scan-steps.svg` 교체는 캐시된 렌더에 걸릴 수 있다. 도식 색이 그대로 보이면 dev 서버를 재시작한다.
