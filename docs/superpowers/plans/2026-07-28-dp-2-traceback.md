# 추가 설명: 어느 날을 골랐는지 되짚기 (dp-2-traceback) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** dp-2의 '추가 설명' 참고 페이지 `dp-2-traceback.md`(선택 복원/traceback)를 SVG 1개와 함께 만들고, dp-2 "더 나가면"의 복원 문단을 이 페이지 링크로 교체한다.

**Architecture:** 기존 '추가 설명' 페이지 관례(제목 "추가 설명 — …", 태그 "추가 설명", difficulty 고급, 본편과 상호 링크)를 따른다. 검증은 `python .claude/review_post.py`(D1~D13)와 `/review-post`(L1~L7).

**Tech Stack:** Astro content collection Markdown, KaTeX, 인라인 SVG, 저장소 리뷰 스크립트.

## Global Constraints

- 참고 페이지 = **선택 복원(traceback)만.** O(1) 이야기는 dp-2 "더 나가면"에 유지.
- 예시 배열 `[3,5,6,10]` (1-indexed), 복원 결과 **{2일, 4일}**, 합 15. 채운 표 — 안 함행 `0·3·5·9`, 함행 `3·5·9·15`.
- 역추적 규칙: 시작 `max(r[n][0], r[n][1])` 중 큰 쪽 → `r[i][1]`(근무)에서 왔으면 i일 선택 후 `r[i-1][0]`로(i−1 강제 제외, i−2로) / `r[i][0]`(쉼)에서 왔으면 i일 미선택, i−1로.
- 새 페이지 frontmatter: title `"추가 설명 — 어느 날을 골랐는지 되짚기"`, date `2026-07-28T10:00:00`, tags `["Algorithm","Dynamic Programming","Traceback","추가 설명"]`, category `algorithm`, difficulty `고급`, numbered `true`, description ≤160자.
- 문체: `docs/writing-rules.md` 바른 문장 쓰기(문두 접속어 최소화), ~다 평서체. 코드 C++. 본문 이모지 금지. 커밋 co-author 없음. 브랜치 `content/dp-2`.
- SVG 스타일: 배경 `#0f1117`, viewBox + width/height 1.5배, `font-family="system-ui,-apple-system,sans-serif"`, dp-2 기존 SVG 팔레트 통일, 세로 클리핑 없게.

---

### Task 1: traceback.svg 생성

**Files:**
- Create: `public/images/dp-2/traceback.svg`

**Interfaces:**
- Produces: `/images/dp-2/traceback.svg` (Task 2 페이지가 참조).

**내용**
- 채운 2행 표를 배경: 일자 `1 2 3 4`, 일급 `3 5 6 10`, 안 함행 `0 3 5 9`, 함행 `3 5 9 15`.
- **역방향(오→왼) 화살표**로 역추적 경로: `r[4][1]=15` → `r[2][1]=5` → 시작 이전(r[1][0]=0). 선택 칸(4일 함, 2일 함) 하이라이트.
- 하단 캡션: 되짚기 결과 `선택 = {2일, 4일}, 합 5+10 = 15`.
- table-fill.svg(순방향)와 대비되는 역방향 시각임을 제목에 드러냄.

- [ ] **Step 1: 작성** — `public/images/dp-2/table-fill.svg`를 스타일 레퍼런스로 열어 팔레트·뷰박스·표 레이아웃을 맞추고, 화살표 방향만 역방향으로 그린다.
- [ ] **Step 2: well-formedness** — `python -c "import xml.dom.minidom; xml.dom.minidom.parse('public/images/dp-2/traceback.svg'); print('ok')"` → `ok`.
- [ ] **Step 3: 값 대조** — 표 값(0·3·5·9 / 3·5·9·15)과 역추적 경로(4일→2일), 결과 {2,4}·15가 Global Constraints와 일치하는지 확인.
- [ ] **Step 4: Commit**

```bash
git add public/images/dp-2/traceback.svg
git commit -m "content(algo): DP② 추가설명 SVG — 역추적 되짚기"
```

---

### Task 2: 참고 페이지 작성 + dp-2 링크 교체

**Files:**
- Create: `src/content/posts/dp-2-traceback.md`
- Modify: `src/content/posts/dp-2.md` (`## 더 나가면` 섹션의 복원 문단 → 링크)

**Interfaces:**
- Consumes: `/images/dp-2/traceback.svg` (Task 1), dp-2의 표·점화식.
- Produces: `/blog/dp-2-traceback` 경로(제공), dp-2에서의 인바운드 링크.

- [ ] **Step 1: 참고 페이지 작성**

`src/content/posts/dp-2-traceback.md`를 스펙 본문 구성대로 작성한다(도입 blockquote + 목차 callout + 값vs구성 + 표를 거꾸로 읽기 + 예시 되짚기 + 역추적 의사코드 + 미묘한 점 callout + 마치며). frontmatter는 Global Constraints대로.

- 도입에 `[동적 계획법 ②](/blog/dp-2)` 링크, 강의 노트 밖 확장 명시.
- 예시 되짚기 서술(검산): r[4] max(9,15)=15=`r[4][1]`(4일 근무)→4일 선택, `r[3][0]=5`로; r[3][0]=`r[2][1]`=5(2일 근무)→2일 선택, `r[1][0]=0`로; 결과 {2,4}, 합 15.
- traceback.svg 삽입:
  `![채운 표를 마지막 칸부터 거꾸로 되짚는다. r[4][1]=15에서 4일, r[2][1]=5에서 2일을 골라 선택 {2,4}·합 15를 복원한다.](/images/dp-2/traceback.svg)`
- 역추적 의사코드(C++, 채운 `r`을 받아 뒤에서 선택 날짜를 모은다). 예:

```cpp
// r: selectWorkingDays가 채운 2행 표.  고른 날짜를 오름차순으로 돌려준다.
vector<int> reconstruct(const vector<array<int,2>>& r, const vector<int>& a, int n) {
    vector<int> days;
    int i = n;
    bool worked = r[n][1] > r[n][0];   // 마지막 칸에서 함/안 함 중 큰 쪽
    while (i >= 1) {
        if (worked) {                  // i일 근무 → i-1일은 반드시 쉼
            days.push_back(i);
            i -= 2;
            if (i >= 1) worked = r[i][1] > r[i][0];
        } else {                       // i일 쉼 → i-1로
            i -= 1;
            if (i >= 1) worked = r[i][1] > r[i][0];
        }
    }
    reverse(days.begin(), days.end());
    return days;
}
```
  코드 뒤에 동점(`>` vs `>=`) 선택이 복원 결과를 하나로 고정한다는 설명 한 줄.
- 미묘한 점 callout: 동점이면 최적해가 여럿일 수 있고 규칙에 따라 하나가 잡힌다; O(1) 공간이면 표가 없어 복원 불가(→ dp-2 "더 나가면" 상호 참조).
- 마치며 + `[동적 계획법 ② →](/blog/dp-2)`.

- [ ] **Step 2: 새 페이지 결정적 검사**

Run: `python .claude/review_post.py src/content/posts/dp-2-traceback.md`
Expected: `발견 사항 없음 ✅` (D4 SVG·D5 경로·D6 링크(dp-2 존재)·D7 frontmatter·D8 수식 짝 등)

- [ ] **Step 3: dp-2 "더 나가면" 링크 교체**

`src/content/posts/dp-2.md`의 `## 더 나가면`에서 복원 문단("표를 다 채운 뒤 마지막 칸에서 거꾸로 되짚으면 …")을 아래처럼 한 줄 링크로 교체한다. **O(1) 문단은 그대로 둔다.**

교체 예: `채운 표를 거꾸로 읽으면 어느 날을 골랐는지까지 복원된다. 그 되짚기 방법은 [추가 설명 — 어느 날을 골랐는지 되짚기](/blog/dp-2-traceback)에서 다룬다.`

- [ ] **Step 4: dp-2 재검**

Run: `python .claude/review_post.py src/content/posts/dp-2.md`
Expected: `발견 사항 없음 ✅` (특히 D6 — `/blog/dp-2-traceback` 링크가 새 파일로 유효)

- [ ] **Step 5: Commit**

```bash
git add src/content/posts/dp-2-traceback.md src/content/posts/dp-2.md
git commit -m "content(algo): DP② 추가설명 페이지(선택 복원) + 본편 링크"
```

---

### Task 3: 리뷰와 마무리

**Files:**
- Modify: `src/content/posts/dp-2-traceback.md`, `public/images/dp-2/traceback.svg` (필요 시)
- Create: `docs/reviews/2026-07-28-dp-2-traceback.md`

- [ ] **Step 1: `/review-post dp-2-traceback` 실행 (L1~L7)** — 특히 L4(traceback.svg ↔ 본문 역추적 경로·값), L7(되짚기 {2,4}·합 15 및 의사코드 검산), L6(노션 밖 확장 명시). dp-2 변경분도 함께 대상이 되면 재확인.
- [ ] **Step 2: 🔴/🟡 반영** — 리포트 지적을 판단 후 편집(자동 수정 아님). L4·L7 불일치는 반드시 정정.
- [ ] **Step 3: 결정적 재검** — `python .claude/review_post.py src/content/posts/dp-2-traceback.md` → `발견 사항 없음 ✅`.
- [ ] **Step 4: (선택) 빌드** — `npm run build` 성공, 두 페이지 생성. `.astro` 캐시 삭제 금지.
- [ ] **Step 5: Commit** — `git add ... docs/reviews/2026-07-28-dp-2-traceback.md && git commit -m "content(algo): DP② 추가설명 리뷰 반영 및 리포트"`.

---

## Self-Review (플랜 작성자 체크)

**1. Spec coverage** — 도입/값vs구성/거꾸로읽기/예시/의사코드/callout/마치며 → Task 2. traceback.svg → Task 1. dp-2 링크 교체(O(1) 유지) → Task 2 Step 3. 검증·리포트 → Task 3. 전부 커버.

**2. Placeholder scan** — 의사코드·frontmatter·표 값·링크 텍스트 실제 값 기재. TBD 없음.

**3. 값 일관성** — 표 `0·3·5·9`/`3·5·9·15`, 결과 {2,4}, 합 15, 역추적 경로 r[4][1]→r[2][1], 링크 `/blog/dp-2-traceback` 및 `/blog/dp-2`가 Task 1·2·3 전반에서 동일. 의사코드의 `worked = r[i][1] > r[i][0]` 규칙이 본문 서술·SVG 경로와 일치.
