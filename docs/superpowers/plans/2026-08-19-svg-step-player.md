# SVG 단계 재생기 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `convex-hull-2`의 그레이엄 스캔 도식을 단계별로 되짚어 볼 수 있게 만들고, JS가 없으면 완성된 그림이 그대로 남게 한다.

**Architecture:** 마크다운 이미지 구문을 유지한 채 `.svg-steps` raw HTML 래퍼로 opt-in한다. 새 rehype 플러그인이 빌드 시 그 `<figure>` 안의 `<img>`를 인라인 `<svg>`로 교체하고, `PostLayout.astro`의 스크립트가 `data-step` 그룹을 접어 재생기로 만든다. 단계는 더하기만 하며 색이 바뀌는 요소는 덮어 그린다.

**Tech Stack:** Astro 마크다운 파이프라인(rehype), 순수 JS(프레임워크 없음), Node 내장 테스트 러너(`node --test`), 기존 Python 계약 테스트(`pytest`)

**Spec:** `docs/superpowers/specs/2026-08-19-svg-step-player-design.md`

## Global Constraints

- 브랜치는 `feat/svg-step-player`다. main에 직접 커밋하지 않는다.
- 커밋 메시지에 `Co-Authored-By` 트레일러를 넣지 않는다.
- **마크다운 이미지 구문 `![alt](/images/....svg)`을 유지한다.** `.claude/review_post.py`의 `IMG_RE`가 SVG를 찾는 유일한 경로이며 D4·D5·D13 검사가 여기 걸려 있다. 새 이미지 문법을 만들지 않는다.
- `.claude/review_post.py`와 리포트 스키마를 수정하지 않는다.
- 새 npm 의존성을 추가하지 않는다. 테스트는 Node 내장 `node --test`를 쓴다.
- `rehypeFigureCaption` 뒤에서 도는 플러그인만 `<figure>` 안의 `<img>`를 볼 수 있다. 플러그인 배열 순서를 지킨다.
- SVG 단계는 **더하기만** 한다. 색 변경은 불투명한 표시를 위에 얹어 표현하고, 장면별 설명 문장은 SVG에 넣지 않는다.
- 자동 재생을 넣지 않는다.
- `scan-push.svg`·`scan-pop.svg`·`scan-result.svg`를 삭제하지 않는다.
- 좌표는 기존 파일에서 그대로 가져온다: Y(150,340) · 1(540,320) · 2(520,250) · 3(460,150) · 4(360,120) · 5(280,190) · 6(230,160) · 7(140,220). viewBox는 `0 0 680 420`.
- 기준선: `python -m pytest .claude -q` → `220 passed, 192 subtests passed`.

---

### Task 1: rehype 플러그인 — `.svg-steps` 안의 img를 인라인 svg로 교체

**Files:**
- Create: `src/plugins/rehype-svg-steps.mjs`
- Create: `src/plugins/rehype-svg-steps.test.mjs`
- Create: `test/fixtures/steps-ok.svg`
- Create: `test/fixtures/steps-none.svg`
- Modify: `package.json` (스크립트 한 줄)
- Modify: `astro.config.mjs` (import 1줄, 플러그인 배열 1곳)

**Interfaces:**
- Consumes: 없음 (첫 태스크)
- Produces: `export function rehypeSvgSteps(options)` — `options.publicDir`(문자열, 기본 `'public'`)를 받아 hast 변환 함수를 돌려준다. Task 3의 마크다운과 Task 4의 스크립트가 이 플러그인이 만든 DOM 구조에 의존한다. 만들어지는 구조는 아래 Step 3의 코드가 정본이다.

- [ ] **Step 1: 테스트 픽스처 두 개를 만든다**

`test/fixtures/steps-ok.svg`:

```svg
<svg viewBox="0 0 100 50" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="50" fill="#0f1117"/>
  <g data-step="1" data-step-label="첫 점을 놓는다"><circle cx="20" cy="25" r="4" fill="#34d399"/></g>
  <g data-step="2" data-step-label="둘째 점을 잇는다"><line x1="20" y1="25" x2="80" y2="25" stroke="#34d399"/></g>
</svg>
```

`test/fixtures/steps-none.svg`:

```svg
<svg viewBox="0 0 100 50" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="50" fill="#0f1117"/>
  <circle cx="20" cy="25" r="4" fill="#34d399"/>
</svg>
```

- [ ] **Step 2: 실패하는 테스트를 쓴다**

`src/plugins/rehype-svg-steps.test.mjs`. hast 트리를 손으로 만들어 넣는다 — 마크다운 전체를 돌리지 않으므로 빠르고 결정적이다.

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { rehypeSvgSteps } from './rehype-svg-steps.mjs';

// rehypeFigureCaption이 만들어 둔 모양을 그대로 흉내낸다:
// div.svg-steps > figure.post-figure > (img, figcaption)
function tree(src, { wrapper = 'svg-steps' } = {}) {
  return {
    type: 'root',
    children: [{
      type: 'element', tagName: 'div', properties: { className: [wrapper] },
      children: [{
        type: 'element', tagName: 'figure', properties: { className: ['post-figure'] },
        children: [
          { type: 'element', tagName: 'img', properties: { src, alt: '설명 문장' }, children: [] },
          { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: '설명 문장' }] },
        ],
      }],
    }],
  };
}

const run = (t) => { rehypeSvgSteps({ publicDir: 'test/fixtures' })(t); return t; };
const figure = (t) => t.children[0].children[0];

test('data-step이 있는 svg는 인라인 svg로 교체된다', () => {
  const t = run(tree('/steps-ok.svg'));
  const [first, second] = figure(t).children;
  assert.equal(first.tagName, 'svg');
  assert.equal(second.tagName, 'figcaption', 'figcaption은 그대로 남는다');
  const groups = first.children.filter((c) => c.tagName === 'g');
  assert.equal(groups.length, 2);
  assert.equal(groups[0].properties['data-step'], '1');
  assert.equal(groups[0].properties['data-step-label'], '첫 점을 놓는다');
});

test('alt는 접근 가능한 이름으로 옮겨진다', () => {
  const svg = figure(run(tree('/steps-ok.svg'))).children[0];
  assert.equal(svg.properties.role, 'img');
  assert.equal(svg.properties['aria-label'], '설명 문장');
});

test('data-step이 없는 svg는 img로 남는다', () => {
  const svg = figure(run(tree('/steps-none.svg'))).children[0];
  assert.equal(svg.tagName, 'img', 'data-step이 없으면 교체하지 않는다');
});

test('파일이 없으면 img로 남고 빌드를 깨지 않는다', () => {
  const svg = figure(run(tree('/does-not-exist.svg'))).children[0];
  assert.equal(svg.tagName, 'img');
});

test('.svg-steps 밖의 이미지는 건드리지 않는다', () => {
  const svg = figure(run(tree('/steps-ok.svg', { wrapper: 'other' }))).children[0];
  assert.equal(svg.tagName, 'img');
});
```

- [ ] **Step 3: 테스트가 실패하는지 확인한다**

먼저 `package.json`의 `scripts`에 한 줄을 넣는다. 새 의존성은 추가하지 않는다.

```json
"test:js": "node --test src/plugins/"
```

Run: `npm run test:js`
Expected: FAIL — `Cannot find module './rehype-svg-steps.mjs'`

- [ ] **Step 4: 플러그인을 만든다**

`src/plugins/rehype-svg-steps.mjs`. SVG 문자열을 hast로 바꾸는 데 새 의존성을 쓰지 않고, 단계 그룹만 뽑아 최소 구조로 다시 세운다. 도식이 우리가 쓴 SVG이므로 임의 SVG 파서가 필요하지 않다.

```javascript
import { readFileSync } from 'node:fs';
import path from 'node:path';

// <tag a="1" b="2"> 의 속성을 뽑는다. 값은 항상 겹따옴표로 쓴다(우리 SVG 규약).
function parseAttrs(openTag) {
  const attrs = {};
  for (const m of openTag.matchAll(/([a-zA-Z-]+)="([^"]*)"/g)) attrs[m[1]] = m[2];
  return attrs;
}

// 자식은 그대로 문자열로 넘긴다. rehype-raw 이후 단계이므로 raw 노드가 그대로 직렬화된다.
function raw(value) {
  return { type: 'raw', value };
}

function buildSvg(source, label) {
  const openMatch = source.match(/<svg\b([^>]*)>/);
  if (!openMatch) return null;
  const attrs = parseAttrs(openMatch[0]);
  const inner = source.slice(openMatch.index + openMatch[0].length, source.lastIndexOf('</svg>'));

  // data-step 그룹을 최상위에서만 찾는다. 중첩 <g>는 그룹 내부 문자열에 그대로 남는다.
  const groups = [];
  const groupRe = /<g\b([^>]*\bdata-step="\d+"[^>]*)>([\s\S]*?)<\/g>/g;
  let rest = inner;
  for (const m of inner.matchAll(groupRe)) {
    groups.push({ attrs: parseAttrs(`<g ${m[1]}>`), body: m[2] });
    rest = rest.replace(m[0], '');
  }
  if (groups.length === 0) return null;

  const children = [raw(rest)];
  for (const g of groups) {
    children.push({
      type: 'element', tagName: 'g',
      properties: {
        'data-step': g.attrs['data-step'],
        'data-step-label': g.attrs['data-step-label'] || '',
      },
      children: [raw(g.body)],
    });
  }

  return {
    type: 'element', tagName: 'svg',
    properties: {
      viewBox: attrs.viewBox,
      xmlns: 'http://www.w3.org/2000/svg',
      role: 'img',
      'aria-label': label,
      ...(attrs['font-family'] ? { 'font-family': attrs['font-family'] } : {}),
    },
    children,
  };
}

export function rehypeSvgSteps({ publicDir = 'public' } = {}) {
  return (tree) => {
    const walk = (node) => {
      if (!node.children) return;
      const classes = node.properties?.className || [];
      const inWrapper = Array.isArray(classes) && classes.includes('svg-steps');

      if (inWrapper) {
        for (const child of node.children) {
          if (child.tagName !== 'figure' || !child.children) continue;
          child.children = child.children.map((leaf) => {
            if (leaf.tagName !== 'img') return leaf;
            const src = leaf.properties?.src;
            if (typeof src !== 'string' || !src.toLowerCase().endsWith('.svg')) return leaf;
            let source;
            try {
              source = readFileSync(path.join(publicDir, src.replace(/^\//, '')), 'utf8');
            } catch {
              return leaf; // 파일이 없으면 지금 동작으로 되돌아간다
            }
            return buildSvg(source, leaf.properties.alt || '') || leaf;
          });
        }
      }

      node.children.forEach(walk);
    };
    walk(tree);
  };
}
```

- [ ] **Step 5: 테스트가 통과하는지 확인한다**

Run: `npm run test:js`
Expected: 5 tests pass

- [ ] **Step 6: 파이프라인에 연결한다**

`astro.config.mjs` 상단 import 옆에 한 줄:

```javascript
import { rehypeSvgSteps } from './src/plugins/rehype-svg-steps.mjs';
```

플러그인 배열에서 `rehypeFigureCaption` **뒤**에 넣는다. 캡션이 먼저 만들어져야 그 안의 `<img>`를 볼 수 있다.

```javascript
rehypePlugins: [rehypeCalloutMath, rehypeKatex, rehypeLazyImages, rehypeFigureCaption, rehypeSvgSteps()],
```

- [ ] **Step 7: 빌드가 깨지지 않는지 확인한다**

Run: `npm run build`
Expected: 성공. 아직 `.svg-steps`를 쓰는 글이 없으므로 출력은 변하지 않는다.

- [ ] **Step 8: 커밋한다**

```bash
git add src/plugins/ test/fixtures/ package.json astro.config.mjs
git commit -m "feat(svg-steps): .svg-steps 안의 도식을 인라인 svg로 전개한다"
```

---

### Task 2: 단계 도식 `scan-steps.svg`

**Files:**
- Create: `public/images/convex-hull-2/scan-steps.svg`

**Interfaces:**
- Consumes: Task 1의 저작 규약 — 최상위 `<g data-step="n" data-step-label="…">`, 나머지는 그룹 밖.
- Produces: 7단계 도식. Task 3의 마크다운이 이 경로를 참조하고, Task 4의 스크립트가 `data-step`을 센다.

- [ ] **Step 1: 도식을 만든다**

기존 세 파일의 좌표·색·서체를 그대로 쓴다. 공통 요소(배경·제목·마커 정의·미처리 회색 점)는 그룹 밖에 두고, 단계마다 표시를 얹는다. 색이 바뀌는 점은 불투명한 원을 덮어 그린다.

```svg
<svg viewBox="0 0 680 420" width="1020" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="420" rx="10" fill="#0f1117"/>
  <defs>
    <marker id="ss-g" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0,0 L9,4.5 L0,9 Z" fill="#34d399"/>
    </marker>
  </defs>

  <text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">Graham Scan — 스택이 볼록 껍질을 만들어 간다</text>

  <!-- 아직 처리하지 않은 점: 모든 단계에서 같은 자리에 있으므로 그룹 밖 -->
  <g fill="#64748b">
    <circle cx="540" cy="320" r="5"/>
    <circle cx="520" cy="250" r="5"/>
    <circle cx="460" cy="150" r="5"/>
    <circle cx="360" cy="120" r="5"/>
    <circle cx="280" cy="190" r="5"/>
    <circle cx="230" cy="160" r="5"/>
    <circle cx="140" cy="220" r="5"/>
  </g>

  <g data-step="1" data-step-label="기준점 Y를 잡고 각도 순으로 점을 정렬한다">
    <circle cx="150" cy="340" r="8" fill="#34d399"/>
    <text x="140" y="368" fill="#6ee7b7" font-size="12" font-weight="700">Y</text>
  </g>

  <g data-step="2" data-step-label="처음 두 점 Y와 1을 스택에 넣는다">
    <line x1="150" y1="340" x2="540" y2="320" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="540" cy="320" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="558" y="325" fill="#93c5fd" font-size="13" font-weight="700">1</text>
  </g>

  <g data-step="3" data-step-label="점 2가 좌회전이므로 push한다">
    <line x1="540" y1="320" x2="520" y2="250" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="520" cy="250" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="540" y="255" fill="#93c5fd" font-size="13" font-weight="700">2</text>
  </g>

  <g data-step="4" data-step-label="점 3도 좌회전 — 1→2 방향에서 2→3이 왼쪽으로 꺾인다">
    <path d="M 528 278 A 30 30 0 0 0 504 224" fill="none" stroke="#fbbf24" stroke-width="2"/>
    <text x="560" y="215" fill="#fbbf24" font-size="12" font-weight="600">좌회전 → push</text>
    <line x1="520" y1="250" x2="460" y2="150" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="460" cy="150" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="476" y="145" fill="#93c5fd" font-size="13" font-weight="700">3</text>
  </g>

  <g data-step="5" data-step-label="점 4와 5가 차례로 쌓인다">
    <line x1="460" y1="150" x2="360" y2="120" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="360" cy="120" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="360" y="105" text-anchor="middle" fill="#93c5fd" font-size="13" font-weight="700">4</text>
    <line x1="360" y1="120" x2="280" y2="190" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="280" cy="190" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="294" y="196" fill="#93c5fd" font-size="13" font-weight="700">5</text>
  </g>

  <g data-step="6" data-step-label="점 6에서 4→5→6이 우회전이다 — 5는 선분 4–6보다 안쪽이다">
    <line x1="280" y1="190" x2="230" y2="160" stroke="#ef4444" stroke-width="2" stroke-dasharray="6 5"/>
    <text x="322" y="185" fill="#f87171" font-size="12" font-weight="600">우회전!</text>
    <circle cx="230" cy="160" r="7" fill="#34d399"/>
    <text x="226" y="145" text-anchor="middle" fill="#6ee7b7" font-size="13" font-weight="700">6</text>
  </g>

  <g data-step="7" data-step-label="5를 pop하고 4→6을 잇는다 — 4→6은 좌회전이라 여기서 멈춘다">
    <circle cx="280" cy="190" r="7" fill="#1f2937" stroke="#ef4444" stroke-width="2" opacity="0.75"/>
    <line x1="271" y1="181" x2="289" y2="199" stroke="#ef4444" stroke-width="2" opacity="0.75"/>
    <line x1="289" y1="181" x2="271" y2="199" stroke="#ef4444" stroke-width="2" opacity="0.75"/>
    <line x1="360" y1="120" x2="230" y2="160" stroke="#34d399" stroke-width="2.5" marker-end="url(#ss-g)"/>
  </g>

  <g data-step="8" data-step-label="점 7까지 처리하면 스택에 껍질 꼭짓점만 남는다">
    <polygon points="150,340 540,320 520,250 460,150 360,120 230,160 140,220" fill="#34d39914" stroke="#34d399" stroke-width="2.5"/>
    <circle cx="140" cy="220" r="7" fill="#1e3a5f" stroke="#3b82f6" stroke-width="2"/>
    <text x="122" y="215" fill="#93c5fd" font-size="13" font-weight="700">7</text>
    <text x="340" y="400" text-anchor="middle" fill="#94a3b8" font-size="12">최종 스택 [Y, 1, 2, 3, 4, 6, 7] — 각 점은 최대 한 번 push, 한 번 pop되므로 스캔은 O(N)</text>
  </g>
</svg>
```

단계가 8개인 이유를 적어 둔다. 스펙은 7단계로 잡았으나 점 4와 5를 한 단계로 묶고 나니 마지막 마무리(점 7과 껍질 완성)가 별도 단계로 남았다. 8단계가 실제 장면 수다.

- [ ] **Step 2: SVG가 유효한지 확인한다**

Run: `python -c "import xml.dom.minidom as m; m.parse('public/images/convex-hull-2/scan-steps.svg'); print('ok')"`
Expected: `ok`

- [ ] **Step 3: 단계 수와 라벨을 확인한다**

Run: `python -c "import re,pathlib; s=pathlib.Path('public/images/convex-hull-2/scan-steps.svg').read_text(encoding='utf-8'); g=re.findall(r'data-step=\"(\d+)\"',s); l=re.findall(r'data-step-label=\"([^\"]+)\"',s); print(g); print(len(l))"`
Expected: `['1'..'8']`이 순서대로, 라벨 8개

- [ ] **Step 4: 커밋한다**

```bash
git add public/images/convex-hull-2/scan-steps.svg
git commit -m "feat(convex-hull-2): 그레이엄 스캔을 8단계 도식 하나로 합친다"
```

---

### Task 3: 본문 교체

**Files:**
- Modify: `src/content/posts/convex-hull-2.md:63-71` (그림 세 개와 사이 문장)

**Interfaces:**
- Consumes: Task 2의 `/images/convex-hull-2/scan-steps.svg`, Task 1의 `.svg-steps` 래퍼 규약.
- Produces: 없음

- [ ] **Step 1: 현재 상태를 확인한다**

Run: `sed -n '55,75p' src/content/posts/convex-hull-2.md`
Expected: 스택 규칙 세 줄 뒤에 `scan-push` → 전환 문장 → `scan-pop` → 문장 → `scan-result` 순서

- [ ] **Step 2: 세 그림과 전환 문장을 하나로 바꾼다**

스택 규칙 세 줄(현재 59~61행)은 **그대로 둔다.** 그 뒤부터 `scan-result.svg` 줄까지를 아래로 교체한다.

```markdown
<div class="svg-steps">

![그레이엄 스캔 — 좌회전이면 push, 우회전이면 pop하며 스택이 볼록 껍질을 만들어 가는 8단계](/images/convex-hull-2/scan-steps.svg)

</div>

우회전이 나오는 순간이 이 알고리즘의 핵심 장면이다. 점 5까지는 순조롭게 쌓이지만 점 6이 도착하면 $4 \to 5 \to 6$이 우회전이다. 이는 **점 5가 선분 $4$–$6$보다 안쪽에 있다**는 뜻이다. 5는 껍질의 꼭짓점이 될 수 없으므로 pop하고, 다시 스택 위 두 점($3$, $4$)과 $6$의 회전을 본다. 이번엔 좌회전이므로 pop을 멈추고 6을 push한다.

위 도식은 이 과정을 단계로 나눠 놓았다. 마지막 단계까지 가면 스택에 남은 점이 그대로 반시계 방향 볼록 껍질을 이루고, pop된 5만 안쪽에 남는다.
```

"아래 그림에서"처럼 특정 장면을 가리키던 표현을 없앤 것이 요점이다. 그림이 하나가 되었으므로 방향 지시가 가리킬 대상이 사라졌다.

- [ ] **Step 3: 결정적 검사를 돌린다**

Run: `python .claude/review_post.py src/content/posts/convex-hull-2.md`
Expected: D4·D5가 새 SVG를 찾아 검사한다. 새 🔴이 없다. 마크다운 이미지 구문을 유지한 이유가 여기서 확인된다.

- [ ] **Step 4: 계약 테스트가 여전히 통과하는지 확인한다**

Run: `python -m pytest .claude -q`
Expected: `220 passed, 192 subtests passed`, 실패 0

- [ ] **Step 5: 커밋한다**

```bash
git add src/content/posts/convex-hull-2.md
git commit -m "content(convex-hull-2): 스캔 세 장면을 단계 도식 하나로 바꾼다"
```

---

### Task 4: 재생기 스크립트와 스타일

**Files:**
- Modify: `src/layouts/PostLayout.astro` (기존 `<script>` 블록 안, 247행에서 시작)
- Modify: `src/styles/global.css` (`.post-figure` 규칙 근처, 534행 부근)

**Interfaces:**
- Consumes: Task 1이 만든 `div.svg-steps > figure > svg > g[data-step][data-step-label]` 구조.
- Produces: 없음 (마지막 구현 태스크)

- [ ] **Step 1: 스타일을 넣는다**

`src/styles/global.css`의 `.post-figure` 규칙 뒤에 넣는다. 단계를 숨기는 규칙이 `.is-live` 아래에만 있는 것이 핵심이다 — CSS만 로드되고 JS가 실패한 상태에서 도식이 접히면 안 된다.

```css
.svg-steps figure { margin-bottom: 0.5rem; }

.svg-steps .step-controls {
  display: none;
  align-items: center;
  gap: 0.75rem;
  margin: 0.5rem 0 1.5rem;
  font-size: 0.875rem;
}
.svg-steps.is-live .step-controls { display: flex; }

.svg-steps .step-controls button {
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--rule, #cbd5e1);
  border-radius: 4px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font: inherit;
}
.svg-steps .step-controls button:disabled { opacity: 0.4; cursor: default; }
.svg-steps .step-counter { font-variant-numeric: tabular-nums; }
.svg-steps .step-label { flex: 1; color: var(--muted, #64748b); }

/* JS가 붙은 뒤에만 단계를 숨긴다 */
.svg-steps.is-live svg g[data-step].is-hidden { visibility: hidden; }

@media print {
  .svg-steps .step-controls { display: none !important; }
  .svg-steps.is-live svg g[data-step].is-hidden { visibility: visible; }
}
```

- [ ] **Step 2: 스크립트를 넣는다**

`src/layouts/PostLayout.astro`의 기존 `<script>` 블록(247행에서 시작) **안**, 끝나기 전에 넣는다. 새 `<script>` 태그를 만들지 않는다.

```javascript
  // SVG 단계 재생기 — .svg-steps 가 없으면 아무 일도 하지 않는다
  document.querySelectorAll('.svg-steps').forEach((wrap) => {
    const steps = [...wrap.querySelectorAll('svg g[data-step]')].sort(
      (a, b) => Number(a.dataset.step) - Number(b.dataset.step)
    );
    if (steps.length < 2) return;

    const controls = document.createElement('div');
    controls.className = 'step-controls';
    const prev = document.createElement('button');
    const next = document.createElement('button');
    prev.type = next.type = 'button';
    prev.textContent = '◀ 이전';
    next.textContent = '다음 ▶';
    prev.setAttribute('aria-label', '이전 단계');
    next.setAttribute('aria-label', '다음 단계');
    const counter = document.createElement('span');
    counter.className = 'step-counter';
    const label = document.createElement('span');
    label.className = 'step-label';
    label.setAttribute('aria-live', 'polite');
    controls.append(prev, counter, next, label);
    wrap.append(controls);

    let at = 1;
    const render = () => {
      steps.forEach((g) => {
        g.classList.toggle('is-hidden', Number(g.dataset.step) > at);
      });
      counter.textContent = `${at}/${steps.length}`;
      label.textContent = steps[at - 1].dataset.stepLabel || '';
      prev.disabled = at === 1;
      next.disabled = at === steps.length;
    };

    prev.addEventListener('click', () => { if (at > 1) { at -= 1; render(); } });
    next.addEventListener('click', () => { if (at < steps.length) { at += 1; render(); } });
    controls.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft' && at > 1) { at -= 1; render(); }
      else if (e.key === 'ArrowRight' && at < steps.length) { at += 1; render(); }
      else return;
      e.preventDefault();
    });

    wrap.classList.add('is-live');
    render();
  });
```

- [ ] **Step 3: 빌드하고 출력 HTML을 확인한다**

Run: `npm run build`
Expected: 성공

Run: `python -c "import pathlib,re; h=[p for p in pathlib.Path('dist').rglob('index.html') if 'convex-hull-2' in str(p)][0].read_text(encoding='utf-8'); print('inline svg:', '<svg' in h); print('data-step 수:', len(re.findall(r'data-step=\"\d+\"', h))); print('figcaption 유지:', '<figcaption' in h); print('img 남음:', 'scan-steps.svg' in h)"`
Expected: `inline svg: True`, `data-step 수: 8`, `figcaption 유지: True`, `img 남음: False`

`viewBox` 대소문자도 함께 본다. Astro는 사용자 플러그인 뒤에 `rehype-raw`를 돌리므로 우리가 만든 `<svg>`가 HTML 파서를 한 번 더 지나간다. HTML 파서는 속성을 소문자로 내리지만 SVG 보정 표가 `viewBox`를 되살린다. 되살아나지 않으면 도식이 크기를 잃으므로 확인이 필요하다.

Run: `python -c "import pathlib; h=[p for p in pathlib.Path('dist').rglob('index.html') if 'convex-hull-2' in str(p)][0].read_text(encoding='utf-8'); print('viewBox 살아있음:', 'viewBox=' in h); print('viewbox 소문자로 깨짐:', 'viewbox=' in h)"`
Expected: `viewBox 살아있음: True`, `viewbox 소문자로 깨짐: False`

소문자로 깨져 있으면 플러그인이 `raw` 노드 대신 완전한 hast 엘리먼트를 만들도록 고쳐야 한다. 그 경우 멈추고 보고한다.

- [ ] **Step 4: 브라우저에서 확인한다**

Run: `npm run preview`

`/blog/convex-hull-2`를 열고 확인한다.
- 컨트롤이 보이고 `1/8`에서 시작한다
- 다음을 누르면 표시가 더해지고 라벨이 바뀐다
- `8/8`에서 다음 버튼이 비활성이고, `1/8`에서 이전이 비활성이다
- 버튼에 포커스를 두고 ←→로 이동된다
- **개발자 도구에서 JS를 끄고 새로 고침** — 컨트롤이 사라지고 완성된 그림이 온전히 보인다
- 인쇄 미리보기에서 도식이 잘리지 않고 컨트롤이 나오지 않는다

- [ ] **Step 5: 커밋한다**

```bash
git add src/layouts/PostLayout.astro src/styles/global.css
git commit -m "feat(svg-steps): 단계 재생 컨트롤과 스타일을 넣는다"
```

---

### Task 5: 검증과 리뷰

**Files:** 수정 없음. 검증과 증거 수집만 한다.

**Interfaces:**
- Consumes: Task 1~4의 모든 변경
- Produces: 사용자에게 보고할 증거

- [ ] **Step 1: 전체 검증을 돌린다**

```bash
npm run test:js
python -m pytest .claude -q
npm run build
python .claude/review_post.py --gate
```

Expected: JS 5 pass · `220 passed, 192 subtests` · 빌드 성공 · 게이트 exit 0

- [ ] **Step 2: 재생기가 없어도 그림이 사는지 증명한다**

`src/layouts/PostLayout.astro`에서 방금 넣은 재생기 블록을 임시로 주석 처리하고 빌드해, 도식이 여전히 완전한 상태로 보이는지 확인한다. 확인 뒤 `git checkout src/layouts/PostLayout.astro`로 되돌리고 같은 확인을 다시 한다.

**주의:** 되돌리기 전에 `git status --short`가 깨끗한지 확인한다. 미커밋 변경이 있으면 `git checkout`이 지운다.

- [ ] **Step 3: 글 리뷰를 돌린다**

Run: `/review-post convex-hull-2`

L4 표현 정렬(본문 서술 순서와 단계 구분이 맞는지)과 L7(단계가 알고리즘을 옳게 나타내는지)을 특히 본다. 게이트 exit code를 보고한다.

- [ ] **Step 4: 변경 요약을 확인한다**

Run: `git diff --stat main...HEAD`
Expected: 스펙·계획 2개 + `src/plugins/` 2개 + `test/fixtures/` 2개 + `package.json` + `astro.config.mjs` + `public/images/convex-hull-2/scan-steps.svg` + `src/content/posts/convex-hull-2.md` + `src/layouts/PostLayout.astro` + `src/styles/global.css`

`.claude/review_post.py`가 목록에 있으면 범위 이탈이다. 멈추고 보고한다.

- [ ] **Step 5: 사용자에게 보고한다**

테스트 결과, 게이트 exit code, 리뷰 판정, 스크린샷 또는 브라우저 확인 결과를 함께 보고한다. PR 생성은 사용자 승인 뒤에 한다.

---

## 검증 요약

| 명령 | 기대 |
|---|---|
| `npm run test:js` | 5 pass |
| `python -m pytest .claude -q` | `220 passed, 192 subtests passed` |
| `npm run build` | 성공, 출력 HTML에 `data-step` 8개 |
| `python .claude/review_post.py --gate` | exit 0 |
| JS 끈 상태 | 완성된 그림이 온전히 보임 |

## 범위 밖

- 나머지 179개 SVG.
- 자동 재생, 줌·팬, 호버 강조, 값 조작.
- `scan-push.svg`·`scan-pop.svg`·`scan-result.svg` 삭제.
- SVG 색상을 라이트 테마에 맞추는 작업.
- `review_post.py`와 리포트 스키마 변경.
