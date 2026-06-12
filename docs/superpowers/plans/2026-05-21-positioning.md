# Homepage Positioning Alignment — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 홈 화면 카피와 태그를 실제 글 콘텐츠(계산 이론·암호학·알고리즘)와 일치시킨다.

**Architecture:** 코드 로직 변경 없음. 텍스트 라인만 교체하는 콘텐츠 정렬 작업. `src/pages/index.astro` 두 군데(설명 문구, 태그 목록)와 `src/layouts/BaseLayout.astro` 한 군데(기본 description) 수정.

**Tech Stack:** Astro 6, TypeScript. 빌드 검증은 `npm run build`, 시각 검증은 `npm run dev`.

**Spec:** `docs/superpowers/specs/2026-05-21-positioning-design.md`

---

## Pre-flight

- 작업 브랜치는 main에서 시작 (이미 main에 있음)
- `node_modules`가 설치돼 있는지 확인. 없다면 `npm install`
- spec 문서를 한 번 읽고 결정 사항 숙지

---

### Task 1: A안 카피·태그·메타 정렬 적용

**Files:**
- Modify: `src/pages/index.astro:36-38` (설명 문구), `src/pages/index.astro:42-48` (태그 목록)
- Modify: `src/layouts/BaseLayout.astro:14` (기본 description)

이 작업은 텍스트 교체뿐이라 단위 테스트가 의미가 없다. 검증은 (a) `npm run build` 통과, (b) dev 서버에서 사람이 시각 확인.

---

- [ ] **Step 1: `src/pages/index.astro`의 설명 문구 교체**

36–38행:

```diff
     <p class="desc">
-      Unity 클라이언트 개발, CS 이론, UI/UX 구현 과정을 기록합니다.<br />
-      결과보다 과정과 이유를 남기는 것을 중요하게 생각합니다.
+      계산 이론·암호학·알고리즘을 풀어 쓰며 정리하는 노트입니다.<br />
+      정답보다 이해의 과정을 우선합니다.
     </p>
```

`<br />` 자리(36행 끝)는 그대로 유지. 마침표·중점(·) 형태도 spec과 정확히 일치시킬 것.

---

- [ ] **Step 2: `src/pages/index.astro`의 태그 목록 교체**

42–48행:

```diff
     <div class="tags">
-      <span class="tag tag--accent">Unity</span>
-      <span class="tag tag--accent">C#</span>
-      <span class="tag tag--accent">UI 설계</span>
-      <span class="tag">TypeScript</span>
-      <span class="tag">C++</span>
-      <span class="tag">알고리즘</span>
-      <span class="tag">CS 이론</span>
+      <span class="tag tag--accent">계산 이론</span>
+      <span class="tag tag--accent">암호학</span>
+      <span class="tag tag--accent">알고리즘</span>
+      <span class="tag">정수론</span>
+      <span class="tag">복잡도</span>
+      <span class="tag">자료구조</span>
     </div>
```

7개 → 6개로 줄어듦. accent 3 + 일반 3. 순서·CSS 클래스명 정확히 일치시킬 것.

---

- [ ] **Step 3: `src/layouts/BaseLayout.astro`의 기본 description 교체**

14행:

```diff
 const {
   title,
-  description = 'XsQuare01의 기술 블로그',
+  description = '계산 이론·암호학·알고리즘을 정리하는 학습 노트 — XsQuare01',
   ogImage = 'https://github.com/XsQuare01.png',
   ogType = 'website',
 } = Astro.props;
```

이 default는 페이지가 description prop을 안 넘길 때 `<meta name="description">`, `<meta property="og:description">`, `<meta name="twitter:description">` 세 곳 모두의 fallback이다. 홈 페이지(`index.astro:28`의 `<BaseLayout title="홈">`)가 prop을 안 넘기므로 홈의 OG description은 이 새 문자열이 된다.

---

- [ ] **Step 4: 빌드 통과 확인**

명령:

```bash
npm run build
```

기대 결과:
- 빌드가 에러 없이 끝나야 한다 (Astro가 `index.astro`·`BaseLayout.astro`를 SSG 컴파일).
- 출력 끝부분에 `Complete!` 또는 비슷한 성공 메시지가 보여야 한다.
- 만약 빌드 실패하면 — 들여쓰기·따옴표·중점(`·`, U+00B7) 오타가 가장 흔한 원인. 위 diff와 정확히 일치하는지 다시 확인.

---

- [ ] **Step 5: dev 서버 띄우고 시각 검증 (사람 확인)**

명령:

```bash
npm run dev
```

서버가 보통 `http://localhost:4321`에 뜬다. 브라우저로 열어 다음 체크리스트를 통과해야 한다:

**홈 화면 (`/`)**
- [ ] 헤드라인이 그대로 "배운 것을 정리하는 개발자"인지 (`배운 것` 부분이 주황색 강조)
- [ ] 설명 두 줄: `계산 이론·암호학·알고리즘을 풀어 쓰며 정리하는 노트입니다.` / `정답보다 이해의 과정을 우선합니다.`
- [ ] accent(주황) 태그 3개가 `계산 이론` `암호학` `알고리즘` 순서로
- [ ] 일반 태그 3개가 `정수론` `복잡도` `자료구조` 순서로
- [ ] 추천 글 카드 2개(RSA, 알고리즘 오리엔테이션)는 변경 없이 그대로
- [ ] 카테고리 탭, 최근 글 피드, 바 차트도 그대로

**테마 전환**
- [ ] 사이드바에서 라이트 모드로 전환해도 accent 태그가 자연스러운 명도로 보이는지
- [ ] 다시 다크로 돌아왔을 때도 정상

**모바일 뷰포트**
- [ ] DevTools에서 480px 폭으로 줄여 헤드라인 폰트 사이즈가 작아지는지 (`@media (max-width: 480px)` 적용)
- [ ] 태그 6개가 자연스럽게 줄바꿈되는지 (flex-wrap)

**메타 description**
- [ ] 홈 페이지에서 우클릭 → 페이지 소스 보기 → `<meta name="description">` 값이 `계산 이론·암호학·알고리즘을 정리하는 학습 노트 — XsQuare01`인지
- [ ] `<meta property="og:description">`, `<meta name="twitter:description">`도 같은 값인지
- [ ] `/blog`나 다른 페이지에서도 description fallback이 새 문자열로 떴는지 (description prop을 안 넘기는 페이지 한정)

문제가 있으면 Step 1–3으로 돌아가 수정. 통과하면 dev 서버를 Ctrl+C로 종료하고 Step 6으로.

---

- [ ] **Step 6: 단일 commit**

```bash
git add src/pages/index.astro src/layouts/BaseLayout.astro
git commit -m "Polish: 홈 카피·태그를 실제 콘텐츠(CS 이론·암호학) 정체성에 정렬

spec: docs/superpowers/specs/2026-05-21-positioning-design.md"
```

기존 commit 메시지 패턴이 `<Type>: <Korean description>` 형태(`Polish:`, `Feature:`, `Fix:`, `Docs:`). 이 변경은 기능 추가가 아니라 텍스트 정렬이라 `Polish:`가 적절.

`git status`로 두 파일만 staged됐는지, 다른 untracked 파일은 그대로인지 확인 후 commit.

---

## Done Criteria

- 위 6단계 모두 체크박스 표시
- `git log -1`이 `Polish: 홈 카피·태그…` 새 commit을 보여줌
- 시각 검증 체크리스트 전부 통과
- dev 서버 종료됨
