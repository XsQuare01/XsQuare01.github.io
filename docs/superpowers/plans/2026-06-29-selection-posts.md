# Selection Problem 포스트 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 노션 "Selection Problem" 노트를 소스로, 메인 글 1편 + 추가설명 2편을 블로그에 추가한다.

**Architecture:** Astro content collection(`src/content/posts/*.md`)에 마크다운 글을 추가하고, KaTeX 수식과 `public/images/<slug>/*.svg` 다이어그램을 곁들인다. 검증은 `npm run build` 통과 + 내부 링크 정합성 + `review-post` 스킬 리뷰로 한다(코드 TDD 아님).

**Tech Stack:** Astro 6, remark-math + rehype-katex, 수작업 SVG.

## Global Constraints

- 브랜치: `feat/post-selection`. main 직접 커밋 금지(PR 워크플로).
- 모든 글 frontmatter: `category: algorithm`, `date: 2026-06-29T09:00:00`(실제 작성일 기준).
- 수식은 KaTeX 문법($...$ 인라인, $$...$$ 블록). 코드는 ```cpp 블록.
- 문체: 직전 글 `src/content/posts/quicksort.md`와 동일한 톤(평어체 "~다", callout 사용, 다른 글 상호링크).
- callout 클래스: `callout`(다루는 내용/이어지는 글), `callout-key`(핵심 정리), `callout-simple`(한 줄 주의).
- 이미지 경로: `public/images/<slug>/<name>.svg`, 글에서는 `/images/<slug>/<name>.svg`로 참조. alt 텍스트 필수.
- 소스 진실: Notion "Selection Problem" 노트. 노트의 "approximate median = 가운데 40%" 프레이밍 유지.

---

### Task 1: 메인 글 `selection.md` 작성

**Files:**
- Create: `src/content/posts/selection.md`

**Interfaces:**
- Produces: slug `selection`. 추가설명 글들이 이 글로 역링크함. README가 이 slug를 링크함.
- Consumes: 기존 글 slug — `quicksort`, `divide-and-conquer`, `sort`, `recursion`.

**내용 명세 (노트 충실 반영):**

frontmatter:
```yaml
---
title: "선택 문제 — k번째 원소를 정렬 없이 O(n)에 찾기"
date: 2026-06-29T09:00:00
description: "k번째로 작은 원소를 찾는 선택 문제. 정렬하면 O(n log n)이지만 선택은 정렬보다 쉬운 문제다. 퀵소트의 분할을 재활용해 한쪽으로만 재귀하는 quickselect를 보고, 최악 O(n²)을 없애기 위해 approximate median(가운데 40%)을 5개씩 묶어 찾는 median of medians로 최악에도 O(n)임을 증명한다."
tags: ["Algorithm", "Selection", "Quickselect", "Median of Medians", "Linear Time"]
category: algorithm
difficulty: 심화
---
```

본문 섹션(순서대로):
1. 인용구(>) 도입 — 퀵소트는 최악 $O(n^2)$. best pivot(중앙값)을 $O(n)$에 찾으면 최악도 $O(n\log n)$ 보장. 그 "중앙값 찾기"가 선택 문제다.
2. callout "이 포스트에서 다루는 내용" — 선택 문제 정의 / quickselect 한쪽 재귀 / approximate median / median of medians로 최악 $O(n)$ 증명.
3. `## 선택 문제란` — $a_1,\ldots,a_n$ 중 $k$번째 작은 수. 최대·최소·중앙값이 모두 같은 문제($k=1,n,n/2$).
4. `## 정렬보다 쉬운 문제` — naive: 정렬 후 인덱싱 $O(n\log n)$. 하지만 정렬은 $1\sim n$번째를 다 찾는 것 = $n$개의 선택 문제를 푼 셈. 선택은 하나만 찾으면 됨. 하한: 모든 원소를 봐야 하므로 $\Omega(n)$. (callout-simple: 다른 수들의 대소관계를 다 알면 그건 이미 정렬 — $O(n\log n)$로 회귀.)
5. `## Quickselect — 한쪽으로만 재귀` — [퀵소트](/blog/quicksort) partition 재활용. pivot 잡고 분할($O(n)$) 후, $k$가 왼쪽이면 왼쪽만, 오른쪽이면 오른쪽만 재귀. C++ 코드(아래) 포함.
   ```cpp
   int select(int a[], int n, int k) {  // k번째(1-indexed) 작은 값
       int p = a[0];
       int j = partition(a, n);   // pivot을 제자리로, 반환은 경계 인덱스
       int rank = j + 1;          // pivot의 등수
       if (k == rank) return a[j];
       if (k < rank)  return select(a, j, k);            // 왼쪽만
       else           return select(a + j + 1, n - j - 1, k - rank);  // 오른쪽만
   }
   ```
   - 최선: $S(n)=n+S(n/2)=n+\tfrac n2+\tfrac n4+\cdots=O(n)$ (등비수열).
   - 최악: $S(n)=n+S(n-1)=O(n^2)$ (매번 끝값 pivot).
   - callout-simple: "대부분 $O(n)$이지만 최악이 남는다. 평균이 정말 $O(n)$인지는 [별도 글](/blog/selection-average)에서 기댓값으로 따진다."
6. `## Approximate median — 정확할 필요는 없다` — 최악을 없애려면 pivot이 항상 중앙 근처면 됨. 정확한 중앙값 대신 "가운데 40%" 안의 값(approximate median)이면 충분. $Q(n)=n+Q(\tfrac14 n)+Q(\tfrac34 n)=O(n\log n)$ — 한쪽이 $\tfrac14$ 지점이어도 $O(n\log n)$ 유지(각 레벨 작업량 합이 $n$). 즉 pivot이 가운데 40%면 퀵소트가 $O(n\log n)$.
7. `## Median of medians — 5개씩 묶기` — approximate median을 $O(n)$에 찾는 법:
   1. $n$개를 5개씩 그룹으로 나눔.
   2. 각 그룹(5개)을 정렬해 그룹 중앙값 $X$를 구함.
   3. $X$들(총 $n/5$개)의 중앙값 $X'$를 (재귀로) 구함 → 이게 approximate median.
   - 보장: $X'$보다 작은 그룹중앙값이 절반($n/10$개), 각 그룹에서 그 중앙값 이하가 3개씩 → $3\cdot n/10=0.3n$개가 $X'$ 이하임이 보장. 대칭으로 $0.3n$개가 $X'$ 이상. → $X'$는 최소 30%·최대 70% 위치.
   - SVG `median-of-medians.svg` 삽입.
   - callout-simple: "왜 하필 5개일까? 3개면 왜 깨지는지는 [별도 글](/blog/selection-why-five)에서 다룬다."
8. `## 분석 — 최악에도 O(n)` — approximate median을 쓰면 반대편 최대 $0.7n$만 재귀: $S(n)=A(n)+n+S(0.7n)$. $A(n)$는 5묶음 정렬 $O(n)$ + 중앙값 $n/5=0.2n$개에서 재귀 → $A(n)=n+S(0.2n)$. 합치면 $S(n)=2n+S(0.2n)+S(0.7n)$. $S(n)=an+b$ 가정해 대입하면 $a=10,b=0$ → $S(n)=O(n)$.
9. callout-key "핵심 정리" — 선택은 정렬보다 쉽다 / quickselect는 평균 $O(n)$이나 최악 $O(n^2)$ / median of medians로 approximate median을 $O(n)$에 찾아 최악도 $O(n)$ / 단 상수·메모리가 커서 실전에선 정렬 후 인덱싱이 보통 더 빠름.
10. callout "이어지는 글" — [quickselect 평균 $O(n)$ 유도](/blog/selection-average), [왜 5개로 나누는가](/blog/selection-why-five), [퀵소트](/blog/quicksort), [분할 정복](/blog/divide-and-conquer) 링크.

- [ ] **Step 1: 글 작성** — 위 명세대로 `src/content/posts/selection.md` 생성. (SVG는 Task 2에서 만들므로 이미지 태그는 경로만 먼저 넣어 둠.)

- [ ] **Step 2: 빌드로 스키마·수식 검증**

Run: `npm run build`
Expected: 빌드 성공. content collection 스키마 통과, KaTeX 파싱 에러 없음. (이미지가 아직 없어도 빌드는 통과 — 404는 런타임.)

- [ ] **Step 3: 내부 링크 정합성 확인**

Run: `grep -oE '/blog/[a-z0-9-]+' src/content/posts/selection.md | sort -u`
Expected: 출력된 각 slug에 대응하는 `src/content/posts/<slug>.md`가 존재(`selection-average`, `selection-why-five`는 Task 3·4에서 생성 예정이므로 이 시점엔 미존재 허용).

- [ ] **Step 4: 커밋**

```bash
git add src/content/posts/selection.md
git commit -m "feat(selection): 선택 문제 메인 글 추가"
```

---

### Task 2: 메인 글 SVG 3종 제작

**Files:**
- Create: `public/images/selection/quickselect-one-side.svg`
- Create: `public/images/selection/approximate-median.svg`
- Create: `public/images/selection/median-of-medians.svg`

**Interfaces:**
- Consumes: Task 1의 `selection.md`가 이 3개 경로를 `/images/selection/...`로 참조.

기존 SVG 스타일 참고: `public/images/quicksort/partition-pointers.svg`, `average-split.svg`를 먼저 읽어 색상·폰트·viewBox 관례를 맞춘다.

각 SVG 내용:
- `quickselect-one-side.svg` — partition된 배열(왼쪽<pivot<오른쪽), $k$가 속한 한쪽만 색칠해 재귀, 반대쪽은 회색으로 버려짐.
- `approximate-median.svg` — 정렬된 수직선 위 가운데 40% 띠(approximate median 영역)와 좌우 30%씩, 최악 시 봐야 할 0.7n 표시.
- `median-of-medians.svg` — 5행 × (n/5)열 격자, 각 열 정렬, 그룹 중앙값 행 강조, $X'$ 위치와 "≤X' 보장" 블루 박스·"≥X' 보장" 퍼플 박스.

- [ ] **Step 1: 기존 SVG 2개 읽고 스타일 파악**

Run: `cat public/images/quicksort/partition-pointers.svg`
Expected: viewBox·색상·텍스트 스타일 확인.

- [ ] **Step 2: SVG 3개 작성**

위 명세대로 3개 파일 생성.

- [ ] **Step 3: 참조 정합성 확인**

Run: `grep -oE '/images/selection/[a-z0-9-]+\.svg' src/content/posts/selection.md | sort -u`
Expected: 3개 경로 모두 출력되고, 각각 `public/images/selection/`에 실제 파일 존재.

- [ ] **Step 4: 빌드 + 커밋**

```bash
npm run build
git add public/images/selection/
git commit -m "feat(selection): 메인 글 SVG 다이어그램 3종 추가"
```

---

### Task 3: 추가설명 A `selection-average.md` 작성

**Files:**
- Create: `src/content/posts/selection-average.md`

**Interfaces:**
- Produces: slug `selection-average`. 메인 글이 이 slug를 링크함.
- Consumes: `quicksort`(E(n) 대비), `selection`(역링크).

frontmatter:
```yaml
---
title: "추가 설명 — quickselect는 왜 평균 O(n)인가"
date: 2026-06-29T09:00:00
description: "선택 문제 본문이 '대부분 O(n)'으로 넘어간 quickselect의 평균 시간을 기댓값 점화식으로 엄밀히 따진다. 퀵소트와 달리 한쪽으로만 재귀하기 때문에 E(n)에 max 항이 생기고, 이를 상계로 풀면 E(n) ≤ 4n = O(n)이다."
tags: ["Algorithm", "Selection", "Quickselect", "Expected Value", "추가 설명"]
category: algorithm
difficulty: 심화
---
```

본문:
1. 도입 — [선택 문제](/blog/selection) 본문은 quickselect를 "대부분 $O(n)$"으로 넘어갔다. 정말 평균이 $O(n)$인지 기댓값으로 따진다.
2. `## 한쪽만 재귀한다는 차이` — [퀵소트 평균 분석](/blog/quicksort#평균은-왜-on-log-n인가)은 양쪽 다 재귀라 $E(k-1)+E(n-k)$를 더했다. quickselect는 $k$가 있는 **한쪽만** 재귀하므로 둘 중 **하나**만 비용에 들어간다 → 상계로 더 큰 쪽 $\max(E(k-1),E(n-k))$.
3. `## 기댓값 점화식` — pivot 등수가 $1/n$ 균등이라 가정.
   $$E(n) \le n + \frac1n\sum_{i=1}^{n}\max\big(E(i-1),\,E(n-i)\big)$$
   $\max$는 큰 절반에서 나오므로, $i$가 $n/2$ 이상일 때 $E(i-1)$, 그 합은 $E(n/2)\sim E(n-1)$를 두 번씩 훑음:
   $$E(n) \le n + \frac2n\sum_{i=n/2}^{n-1} E(i)$$
4. `## 상계 풀이` — $E(n)\le 4n$을 수학적 귀납법으로. 가정 $E(i)\le 4i$를 대입:
   $$E(n)\le n+\frac2n\sum_{i=n/2}^{n-1}4i \le n + \frac{8}{n}\cdot\frac{3n^2}{8}=n+3n=4n.$$
   (합 $\sum_{i=n/2}^{n-1} i \le \frac{3n^2}{8}$ 근사 설명 포함.)
5. callout-key — quickselect 평균 $E(n)\le 4n=O(n)$. 퀵소트가 $n\log n$인 건 양쪽을 다 재귀해서고, 선택은 한쪽만 버려 등비수열로 줄어 $n$이 된다. 단 이는 **평균**이며 최악은 여전히 $O(n^2)$ — 최악까지 없애려면 [median of medians](/blog/selection-why-five)가 필요.
6. callout "이어지는 글" — [선택 문제 본문](/blog/selection), [퀵소트 평균 분석](/blog/quicksort).

- [ ] **Step 1: 글 작성** — 위 명세대로 생성.

- [ ] **Step 2: 빌드 검증**

Run: `npm run build`
Expected: 성공, KaTeX 에러 없음.

- [ ] **Step 3: 커밋**

```bash
git add src/content/posts/selection-average.md
git commit -m "feat(selection): 추가설명 — quickselect 평균 O(n) 유도"
```

---

### Task 4: 추가설명 B `selection-why-five.md` + SVG 작성

**Files:**
- Create: `src/content/posts/selection-why-five.md`
- Create: `public/images/selection-why-five/group-size-compare.svg`

**Interfaces:**
- Produces: slug `selection-why-five`. 메인 글과 추가설명 A가 이 slug를 링크함.
- Consumes: `selection`(역링크).

frontmatter:
```yaml
---
title: "추가 설명 — 왜 하필 5개로 나누는가"
date: 2026-06-29T09:00:00
description: "median of medians가 그룹을 5개로 나누는 이유. 그룹 크기 g를 일반화해 두 부분문제 S(n/g)와 S(보장 못 한 나머지)의 비율 합이 1보다 작아야 선형이 됨을 보인다. g=3은 합이 1이 되어 깨지고, g=5는 0.2+0.7=0.9로 성립하며, g=7은 되지만 그룹 정렬 비용만 는다."
tags: ["Algorithm", "Selection", "Median of Medians", "추가 설명"]
category: algorithm
difficulty: 심화
---
```

본문:
1. 도입 — [선택 문제](/blog/selection)의 median of medians는 하필 5개씩 나눴다. 4도 6도 아닌 5인 이유를 따진다.
2. `## 그룹 크기 g로 일반화` — $g$개씩 나누면 그룹 $n/g$개. approximate median $X'$ 보장: 그룹중앙값의 절반($\tfrac{n}{2g}$ 그룹)에서 각 $\lceil g/2\rceil$개가 $X'$ 이하 → 보장 $\approx \tfrac{n}{2g}\cdot\tfrac{g+1}{2}$. 큰 $g$에서 $\approx n/4$.
3. `## 선형이 되는 조건` — 재귀 두 갈래: 그룹중앙값 찾기 $S(n/g)$ + 보장 못 한 나머지 $S(n - \text{보장})$. 합이 $1$보다 작아야 선형($S(n)=cn+S(\alpha n)+S(\beta n)$, $\alpha+\beta<1$).
   - $g=5$: $S(0.2n)+S(0.7n)$, $0.2+0.7=0.9<1$ ✓
   - $g=3$: $S(\tfrac13 n)+S(\tfrac23 n)$, 합 $=1$ ✗ (선형 안 됨, $n\log n$)
   - $g=7$: 합 $<1$로 되지만 그룹 정렬 비용↑, 5보다 이득 없음
   - SVG `group-size-compare.svg` 삽입(그룹 3 vs 5 보장 영역 비교).
4. `## 홀수여야 하는 이유` — 그룹 크기가 짝수면 중앙값이 두 개라 모호. 홀수면 가운데 하나로 명확.
5. callout-key — $g=5$는 "$\tfrac1g+\beta<1$"을 만족하는 가장 작은 실용적 홀수. 3은 등식이 되어 깨지고, 7+는 되지만 비용만 는다.
6. callout "이어지는 글" — [선택 문제 본문](/blog/selection).

- [ ] **Step 1: 글 작성**

- [ ] **Step 2: SVG 작성** — `group-size-compare.svg` (기존 스타일 따름).

- [ ] **Step 3: 빌드 + 참조 정합성**

Run: `npm run build && grep -oE '/images/selection-why-five/[a-z0-9-]+\.svg' src/content/posts/selection-why-five.md`
Expected: 빌드 성공, 참조 경로의 파일 존재.

- [ ] **Step 4: 커밋**

```bash
git add src/content/posts/selection-why-five.md public/images/selection-why-five/
git commit -m "feat(selection): 추가설명 — 왜 5개로 나누는가 + SVG"
```

---

### Task 5: README 알고리즘 섹션 갱신 + 상호링크 최종 점검

**Files:**
- Modify: `README.md` (알고리즘 시리즈 표)

**Interfaces:**
- Consumes: slug `selection`(메인 글). 추가설명 2편은 표에 넣지 않고 본문 내부 링크로만 노출(README는 시리즈 대표 글만).

- [ ] **Step 1: README 표에 행 추가** — `### 알고리즘` 표 마지막(테이프 스토리지 다음)에 추가:
```markdown
| [선택 문제](https://xsquare01.github.io/blog/selection) | k번째 원소를 정렬 없이 O(n)에 찾기 |
```

- [ ] **Step 2: 전체 내부 링크 정합성 검증**

Run: `for f in selection selection-average selection-why-five; do echo "== $f =="; grep -oE '/blog/[a-z0-9-]+' src/content/posts/$f.md | sort -u; done`
Expected: 모든 참조 slug에 대응하는 `src/content/posts/<slug>.md` 존재(세 글 상호링크가 끊김 없이 맞물림).

- [ ] **Step 3: 최종 빌드**

Run: `npm run build`
Expected: 성공.

- [ ] **Step 4: 커밋**

```bash
git add README.md
git commit -m "docs(readme): 알고리즘 시리즈에 선택 문제 추가"
```

---

### Task 6: review-post 리뷰 반영 + PR

**Files:**
- Modify: 리뷰 지적사항에 따라 세 글·SVG 수정.

- [ ] **Step 1: review-post 스킬 실행** — main 대비 변경된 selection 글들의 내용·문체·SVG 리뷰.

Run(스킬): `/review-post selection` (이어서 `selection-average`, `selection-why-five`)

- [ ] **Step 2: 지적사항 반영** — 리뷰 리포트의 🔴/🟡 항목 수정 후 커밋.

- [ ] **Step 3: 최종 빌드 + 푸시 + PR**

```bash
npm run build
git push -u origin feat/post-selection
gh pr create --title "feat(selection): 선택 문제 메인 + 추가설명 2편" --body-file <(...)
```
(PR 본문은 `--body-file`로 작성 — PowerShell here-string `@`가 새지 않도록.)

---

## Self-Review

**Spec coverage:** 설계 스펙의 3개 산출물(메인/A/B), SVG, 상호링크, README, 작업방식이 모두 Task 1~6에 매핑됨. ✓
**Placeholder scan:** 각 글의 핵심 수식·코드·섹션 순서를 본문에 명시함. SVG는 내용 명세 제공. ✓
**Type consistency:** slug 3종(`selection`/`selection-average`/`selection-why-five`)과 이미지 경로가 전 Task에서 일관. 링크 방향(메인↔A↔B) 일치. ✓
