# dp-3-traceback 추가 설명 페이지 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 행렬 곱셈 최적 괄호화 복원(traceback)을 다루는 dp-3 동반 페이지 `dp-3-traceback`와 파스 트리 SVG를 만들고, dp-3 본편의 예고 문장을 하드 링크로 잇는다.

**Architecture:** Astro 정적 블로그. 포스트 `src/content/posts/dp-3-traceback.md`(마크다운 + raw HTML 콜아웃), 이미지 `public/images/dp-3/traceback.svg`(손 SVG). dp-2-traceback과 동일한 조판·팔레트·목소리를 따른다.

**Tech Stack:** Astro, 마크다운 + KaTeX, raw HTML `div.callout`/`callout-simple`, 손 SVG(sharp로 PNG 렌더 검증), C++ 의사코드.

## Global Constraints

- 소스/원문 보존: 이 페이지 전체가 **강의 노트 밖 확장**이다. dp-3 기반 DP(점화식·표)는 노션 원문, 분할점 기록·괄호화 복원은 노트 밖. 오프닝·문맥에서 확장임을 밝힌다. 권한 순서: AGENTS > 정본(`docs/writing-rules.md` 6단계) > 이 계획.
- 핵심 값(재검산 완료): `split[i][j]`는 `m[i][j]`의 최소를 낸 마지막 곱 분할점 `k`. `d=[3,2,4,2]`에서 `split[1][3]=1`, `split[2][3]=2`. 재귀 `build(1,3)` → **`(M₁(M₂M₃))`**, 비용 28(= dp-3의 더 저렴한 그룹).
- 복원 재귀: `build(i,j)` = `i==j`면 `Mᵢ`(잎), 아니면 `"(" + build(i, split[i][j]) + build(split[i][j]+1, j) + ")"`. 이 재귀 구조가 이진 파스 트리(잎 n개·내부 노드 n-1개).
- 문장: 초안 후 `docs/writing-rules.md` '바른 문장 쓰기'로 훑는다(문두 접속어 최소화 최우선). 코드는 C++ 의사코드.
- 커밋: **Co-Authored-By 트레일러 넣지 않음**. 콘텐츠 편집 중 `.astro` 캐시 삭제 금지.
- SVG 팔레트(dp-2와 동일, **다크 고정**): 배경 `#0f1117`(rx 10), 제목 `#e2e8f0`, 부제/캡션 `#64748b`/`#94a3b8`, 구분선 `#1e293b`/`#334155`/`#475569`, 중립 박스 `#1e293b`/`#475569` 글자 `#cbd5e1`, 파랑 `#1e3a5f`/`#3b82f6` 글자 `#dbeafe`, 초록 `#14352b`/`#34d399` 글자 `#d1fae5`, 앰버(정답) `#3a2c0f`/`#f59e0b` 글자 `#fef3c7`·강조 `#fbbf24`. 루트 `font-family="system-ui,-apple-system,sans-serif"`, viewBox 좌표의 1.5배를 width/height로.

---

### Task 1: 추가 설명 포스트 + dp-3 본편 링크 갱신

**Files:**
- Create: `src/content/posts/dp-3-traceback.md`
- Modify: `src/content/posts/dp-3.md` (`## 더 나가면` 절의 예고 문장을 하드 링크로)
- Reference(Task 2에서 생성): `/images/dp-3/traceback.svg`

**Interfaces:**
- Produces: slug `dp-3-traceback`, 제목 "추가 설명 — 어떤 순서로 곱했는지 되짚기". dp-3(`/blog/dp-3`)로 역링크. dp-3.md는 이 페이지로 하드 링크.

**먼저 `src/content/posts/dp-2-traceback.md`를 읽어** 오프닝 blockquote, `<div class="callout">`/`callout-title`, `<div class="callout callout-simple">`, 예시 조판, 코드 블록, 마치며 끝줄 링크의 정확한 형태를 그대로 따른다. dp-3 본편(`src/content/posts/dp-3.md`)의 기호(`M[i,j]`, `d_{i-1}d_k d_j`, `matrixChain`)와 일관되게 쓴다.

**Frontmatter(정확히):**
```yaml
---
title: "추가 설명 — 어떤 순서로 곱했는지 되짚기"
date: 2026-07-31T09:00:00
description: "동적 계획법 ③의 표는 최소 비용만 담는다. 어떤 괄호 순서로 곱해야 그 비용이 나오는지는 표에 없다. 채우는 동안 이긴 분할점 k를 함께 적어 두면 (1,n)에서 재귀로 (M₁(M₂M₃)) 같은 괄호화를 복원한다. d=[3,2,4,2] 예시로 되짚고, 파스 트리와 동점의 미묘함까지 짚는다."
tags: ["Algorithm", "Dynamic Programming", "Traceback", "Matrix Chain", "추가 설명"]
category: algorithm
difficulty: 고급
numbered: true
---
```

**본문 구성(내용·수치·표현 고정, 문장은 dp-2-traceback 목소리로):**

1. **오프닝 blockquote** — dp-3 링크. "[동적 계획법 ③](/blog/dp-3)은 표를 채워 최소 비용 28을 구했다. 표에는 숫자만 있을 뿐, **어떤 괄호 순서로 곱했는지**는 어디에도 적혀 있지 않다. 이 글은 강의 노트 밖 확장으로, 채운 표에 분할점을 함께 적어 그 순서까지 복원하는 방법을 다룬다."
2. **callout `이 글에서 다루는 내용`**(dp-2-traceback와 동일 구조) 불릿:
   - 표가 담는 것은 **최소 비용**뿐, 어떤 괄호 순서인지의 **구성**은 별개
   - 이긴 분할점 $k$를 $split[i][j]$에 함께 기록하기
   - $(1,n)$에서 **재귀로 되짚어** 괄호화를 복원(= 이진 파스 트리)
   - $d=[3,2,4,2]$ 예시로 $(M_1(M_2M_3))$ 확인, 동점과 $split$ 표 공간
3. **## 값과 구성은 다르다** — `m[1][3]=28`은 "28이 최소"라는 값만 말한다. 어느 $k$가 그 최소를 냈는지는 별개 질문이고, 그 승자는 표를 채우는 `min` 비교에서 이미 정해져 있다. 표를 지우지 않으면 그 정보는 남는다.
4. **## 분할점을 기록하기** — `m[i][j]`가 갱신되는 그 자리에서 이긴 `k`를 `split[i][j]`에 적는다. 안쪽 루프의 `min` 갱신을 조건문으로 풀어 저장 한 줄을 더한다. (아래 코드 조각 A.)
5. **## 거꾸로 짜맞추기** — `build(i,j)`: 기저 `i==j`는 잎 `Mᵢ`, 그 외에는 `split[i][j]`로 좌 `[i,k]`·우 `[k+1,j]`를 나눠 괄호로 감싼다. 시작은 `build(1,n)`. 이 재귀 호출 구조가 곧 이진 파스 트리다.
6. **## 예시로 복원** — `d=[3,2,4,2]`, `split[1][3]=1`·`split[2][3]=2`. `build(1,3)` = `"(" + build(1,1) + build(2,3) + ")"`; `build(1,1)="M₁"`; `build(2,3)="(" + M₂ + M₃ + ")"="(M₂M₃)"`. 최종 `(M₁(M₂M₃))`. 이 괄호화의 비용은 dp-3의 28과 같다(오른쪽부터 묶기). → 이미지: `![split 표를 따라 (1,3)부터 재귀로 되짚으면 파스 트리 (M₁(M₂M₃))가 나온다. 루트는 k=1, 오른쪽 내부 노드는 k=2.](/images/dp-3/traceback.svg)`
7. **## 코드** — 코드 조각 A(split 기록)와 B(재귀 복원)를 제시.

   조각 A:
   ```cpp
   // split[i][j]: m[i][j]의 최소를 낸 마지막 곱의 분할점 k.
   vector<vector<int>> split(n + 1, vector<int>(n + 1, 0));
   // ... matrixChain 안쪽 k 루프에서 min 갱신을 조건문으로:
   long long cost = m[i][k] + m[k+1][j] + 1LL*d[i-1]*d[k]*d[j];
   if (cost < m[i][j]) {          // 더 싼 분할을 찾으면
       m[i][j] = cost;
       split[i][j] = k;           // 그 분할점을 기록
   }
   ```
   조각 B:
   ```cpp
   // split 표를 따라 [i,j]의 괄호화를 문자열로 되짚는다.
   string reconstruct(const vector<vector<int>>& split, int i, int j) {
       if (i == j) return "M" + to_string(i);          // 잎: 행렬 하나
       int k = split[i][j];                            // 이 구간의 마지막 곱
       return "(" + reconstruct(split, i, k)
                  + reconstruct(split, k + 1, j) + ")";
   }
   // 호출: reconstruct(split, 1, n)  →  "(M1(M2M3))"
   ```
   조각 A 뒤에 `<`(등호 없음)를 쓴 이유는 8절 동점 논의로 연결한다.
8. **미묘한 점 `<div class="callout callout-simple">`**(dp-2-traceback와 동일 구조) — ① 동점: 여러 `k`가 같은 최소를 내면 유효한 괄호화가 여럿이다. 조각 A의 `<`(등호 없음)는 먼저 찾은 `k`를 남기고, `<=`로 바꾸면 다른 갈래가 선택된다. "유일한 정답"이 있어서가 아니다. ② 복원은 `split` 표($O(n^2)$ 공간)를 요구한다 — 비용값만으로는 순서를 되짚을 수 없다. 복원된 괄호화는 잎이 `n`개, 내부 노드가 `n-1`개인 완전 이진 트리다.
9. **## 마치며** — 표는 값을 구하면서 구성 정보도 남긴다. 분할점 하나만 함께 적어 두면 비용에서 순서를 되살린다. 끝줄 `[동적 계획법 ③ →](/blog/dp-3)`.

**dp-3 본편 링크 갱신:** `src/content/posts/dp-3.md`의 `## 더 나가면` 절에서 현재 문장
`그 복원 방법은 추가 설명 페이지에서 따로 다룬다.`
를 다음으로 바꾼다:
`그 복원 방법은 [추가 설명 — 어떤 순서로 곱했는지 되짚기](/blog/dp-3-traceback)에서 따로 다룬다.`

- [ ] **Step 1: 포스트 작성** — 위 구성대로 `src/content/posts/dp-3-traceback.md` 생성. 콜아웃 내부 `$수식$`·인라인 코드는 dp-2-traceback와 동일한 빈 줄 규칙으로 넣는다.
- [ ] **Step 2: dp-3 본편 링크 갱신** — 위 문장 치환. (dp-3.md의 다른 부분은 건드리지 않는다.)
- [ ] **Step 3: 문장 훑기** — `docs/writing-rules.md` '바른 문장 쓰기'로 문두 접속어·불필요 표현 점검, 과교정 금지.
- [ ] **Step 4: 링크/frontmatter 검증**
  Run: `node -e "const fs=require('fs'); const t=fs.readFileSync('src/content/posts/dp-3-traceback.md','utf8'); const p=fs.readFileSync('src/content/posts/dp-3.md','utf8'); console.log(/\]\(\/blog\/dp-3\)/.test(t)?'OK back-link':'FAIL back-link'); console.log(/\]\(\/blog\/dp-3-traceback\)/.test(p)?'OK forward-link':'FAIL forward-link'); console.log(t.match(/^---[\s\S]*?---/)[0]);"`
  Expected: `OK back-link` + `OK forward-link` + frontmatter 출력.
- [ ] **Step 5: raw 수식 누수 검사** — 콜아웃 div 안 `$`가 dp-2-traceback 방식(빈 줄 분리)으로 렌더되는지 확인.
  Run: `grep -nE '\$' src/content/posts/dp-3-traceback.md | head -30`
- [ ] **Step 6: 커밋**
  ```bash
  git add src/content/posts/dp-3-traceback.md src/content/posts/dp-3.md
  git commit -m "content(algo): 추가 설명 — 행렬 곱셈 최적 괄호화 복원(dp-3-traceback)"
  ```

---

### Task 2: traceback.svg (이진 파스 트리)

**Files:**
- Create: `public/images/dp-3/traceback.svg`

**Interfaces:**
- Consumes: 경로 `/images/dp-3/traceback.svg`, 복원 결과 `(M₁(M₂M₃))`, `split[1][3]=1`, `split[2][3]=2`.
- Produces: 훅/설명 이미지.

**먼저 `public/images/dp-3/table-fill.svg`와 `public/images/dp-2/traceback.svg`를 읽어** 팔레트·좌표 스케일·텍스트 스타일을 맞춘다.

**What to draw — `public/images/dp-3/traceback.svg`:** `(M₁(M₂M₃))`의 이진 파스 트리.
- 루트: 내부 노드(원/둥근 박스), 라벨 "k=1" — 이 구간의 마지막 곱.
- 루트의 왼쪽 자식: 잎 `M₁`(중립/파랑 박스).
- 루트의 오른쪽 자식: 내부 노드, 라벨 "k=2".
- 그 내부 노드의 두 잎: `M₂`, `M₃`.
- 노드를 잇는 간선(선). 내부 노드는 "마지막 곱", 잎은 개별 행렬임을 작은 범례로.
- 곁(또는 상단)에 작은 `split` 표: `split[1][3]=1`, `split[2][3]=2`.
- 하단 캡션에 결과 문자열 `(M₁(M₂M₃))` — 앰버 강조(정답).
- 짧은 제목 예: "표의 분할점을 따라 괄호화를 되짚는다".
- 다크 고정 팔레트·스케일은 Global Constraints 참조. 텍스트가 노드를 넘지 않게 여유.

- [ ] **Step 1: SVG 작성** — dp-2 SVG 루트 구조(`<svg viewBox … width height font-family>` + 배경 rect)를 본떠 작성.
- [ ] **Step 2: PNG 렌더 검증**
  Run: `node -e "const sharp=require('sharp'); sharp('public/images/dp-3/traceback.svg',{density:200}).png().toFile('C:/Users/bhmun/AppData/Local/Temp/claude/C--Users-bhmun-XsQuare01-github-io/bbe40d9c-a288-4d47-bfc3-16e4b176d2b7/scratchpad/traceback.png').then(i=>console.log('OK',i.width,i.height)).catch(e=>{console.error(e);process.exit(1)})"`
  Expected: `OK <w> <h>`. PNG를 Read로 열어 트리 구조(루트 k=1 → 왼쪽 M₁, 오른쪽 k=2 → M₂·M₃), split 표 값, 결과 문자열이 정확하고 겹침·넘침 없는지 확인. 고쳐 다시 렌더.
- [ ] **Step 3: 커밋**
  ```bash
  git add public/images/dp-3/traceback.svg
  git commit -m "content(algo): dp-3-traceback 파스 트리 SVG (M₁(M₂M₃))"
  ```

---

### Task 3: 통합 검증 (빌드 · 링크 · 리뷰 · 수치)

**Files:**
- Verify only(수정 없으면). 리뷰 지적이 포스트에 있으면 Task 1 파일만 고친다.

**Interfaces:**
- Consumes: Task 1~2 산출물 전부.

- [ ] **Step 1: 빌드 결정 검사(D1~D13)**
  Run: `npm run build`
  Expected: 빌드 성공, dp-3-traceback 페이지 생성. **새 하드 링크 유효**: dp-3 → dp-3-traceback(D6), dp-3-traceback → dp-3(D6) 모두 대상 존재. frontmatter(D7)·시리즈(D12) 통과, 깨진 링크 0.
- [ ] **Step 2: 수치 재검산** — `split[1][3]=1`, `split[2][3]=2`, `build(1,3)=(M₁(M₂M₃))`, 그 비용 28이 본문·SVG·재귀 코드와 일치하는지 다시 계산해 대조.
- [ ] **Step 3: review-post 리뷰** — `review-post`로 dp-3-traceback 리뷰 리포트(`docs/reviews/2026-07-31-dp-3-traceback.md`) 생성. L1~L7 전 범주 coverage row + 요약 포함(계약). 지적된 🔴/🟡는 반영. `test_review_post.py`는 **신규 실패 0** 기준(사전 실패 무시):
  Run: `python .claude/test_review_post.py -v 2>&1 | grep -E "^(FAIL|ERROR):" | grep -v test_all_existing_review_reports_conform_to_v2_schema`
  Expected: 빈 출력.
- [ ] **Step 4: 계약 테스트(정본 변경 없음, 회귀만)**
  Run: `python .claude/test_review_post.py TestAuthoringGuideContracts -v`
  Expected: `Ran 4 tests ... OK`.
- [ ] **Step 5: 리뷰 반영 커밋(있으면)**
  ```bash
  git add -A
  git commit -m "content(algo): dp-3-traceback 리뷰 반영"
  ```

---

## Self-Review

- **Spec 커버리지**: 값 vs 구성(T1 §3)·split 기록(T1 §4,조각 A)·재귀 복원(T1 §5,조각 B)·예시 복원(T1 §6, T2)·코드(T1 §7)·동점/공간(T1 §8)·마치며(T1 §9)·dp-3 링크 갱신(T1 Step 2)·SVG 파스 트리(T2)·원문 보존(constraints, T3 리뷰)·검증(T3) — 스펙 각 절이 대응 태스크를 가진다. 범위 밖(Hu–Shing 등)은 스펙에 명시.
- **Placeholder 스캔**: frontmatter·수치·코드 조각 A/B·팔레트·검증 명령을 구체값으로 박음. TODO/TBD 없음.
- **타입/이름 일관성**: 슬러그 `dp-3-traceback`, 함수 `reconstruct(split,i,j)`·`build`(설명용 재귀)·`matrixChain`, 표 `m[i][j]`/`split[i][j]`, 이미지 `/images/dp-3/traceback.svg`, 예시 `(M₁(M₂M₃))`·`split[1][3]=1`·`split[2][3]=2`를 전 태스크에서 동일 표기. (본문 설명은 `build`, 코드 함수명은 `reconstruct` — 8절/코드에서 "이 재귀를 reconstruct로 옮기면"으로 잇는다.)
