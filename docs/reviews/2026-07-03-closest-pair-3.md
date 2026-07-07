# 블로그 포스트 리뷰: closest-pair-3

- schema_version: review-report/v2
- target: closest-pair-3
- generated_at: 2026-07-03

## 결정적 검사: src/content/posts/closest-pair-3.md

🔴 필수 (1)
- [D7] not-recorded  frontmatter enum 불일치: difficulty='고급' — 허용값: 심화, 입문, 중급

요약(결정적): 🔴 1 · 🟡 0 · 🟢 0

> **주의 — D7은 오탐(false positive)이다.** `src/content/config.ts:13`의 실제 enum은 `['입문','초급','중급','고급','심화']`로 `고급`을 허용하며, `npm run build`도 통과한다. 형제 글(`closest-pair-1/2`, `closest-pair-five-points`)도 모두 `difficulty: 고급`을 쓴다. 검사기(`.claude/review_post.py:54 CANONICAL_DIFFICULTIES`)와 `docs/reviews/README.md:72`가 난이도 3→5단계 세분화(커밋 a51d76a) 이후 갱신되지 않은 **낡은 3단계 목록**을 들고 있는 것이 원인이다. **포스트는 고치지 말고, 검사기·README를 5단계로 갱신해야 한다.** 아래 L 비평의 마지막 항목 참조.

## LLM 비평: src/content/posts/closest-pair-3.md

### L6 소스 자료 충실성 — Notion 대조 (핵심)
- severity: 🟢 · source: L · rule_id: L6 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:1
- quote: (Notion 「💑 Closest Pair」 > Plane Sweeping) "직선과 D 만큼 떨어진 왼쪽 점들을 이용하여 balanced binary tree ... 점들은 y 좌표로 정렬되어 있다."
- message: Notion 원문 「💑 Closest Pair」의 **Plane Sweeping** 절을 `notion-fetch`로 가져와 대조함. 핵심 알고리즘이 원문과 **충실히 일치**한다 — x정렬 후 sweep line, 왼쪽 폭 D의 균형 BST(원문 예시 AVL Tree ↔ 본문 `std::set`), x 작은 순 delete(점당 1회, 총 O(N log N)), `y−d ≤ y' ≤ y+d` 범위 조회 O(log N), insert O(log N), 전체 O(N log N)까지 모두 대응된다.
- recommendation: 유지. (원본 이미지 대신 자체 SVG로 대체한 것은 시리즈 관행과 일치.)

### L6 소스 대비 의도적 편차 — 후보 개수 5 → "상수 개"
- severity: 🟢 · source: L · rule_id: L6 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:66
- quote: "직사각형을 한 변 $D/2$인 칸으로 쪼개면 칸당 최대 1점, 그래서 후보는 $n$과 무관한 **상수 개**다."
- message: Notion 원문은 일관되게 "맞은편 정사각형 2개의 점 **5개**"라고 서술한다. 본문은 특정 숫자를 못박지 않고 "상수 개"로 두고, 칸 세기 논거를 [closest-pair-five-points](/blog/closest-pair-five-points)로 위임했다. 이는 이미 발행된 five-points 글이 "노트의 '5개'는 살짝 모자란 어림, 안전값은 7"이라고 **명시적으로 교정**한 것과 정합적이다(AGENTS.md의 "명확한 사실 오류는 예외적으로 바로잡을 수 있다"에 해당).
- recommendation: 유지. 시리즈 내부 정합성이 원문의 5보다 우선한다.

### L6 소스에 없는 추가분 — 전체 C++ 코드 (검증됨)
- severity: 🟢 · source: L · rule_id: L6 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:99
- quote: "set<pair<ll, ll>> active;  // 키는 {y, x}"
- message: Notion의 Plane Sweeping 절에는 산문 설명만 있고 **전체 코드가 없다**(코드가 붙은 것은 분할정복 아이디어 1·2뿐). 본문의 `std::set` 구현은 새로 저술한 것이나, 원문이 서술한 알고리즘의 충실한 실현이며 브루트포스와의 **차분 검증(3000 케이스: 클러스터·동일 y·음수 좌표 포함)에서 불일치 0건**으로 정답성을 확인했다. 시리즈 ①②가 매 편 전체 코드를 싣는 관행과도 일치.
- recommendation: 유지.

### L6 소스에 없는 추가분 — y창 폭 정수화 콜아웃
- severity: 🟢 · source: L · rule_id: L6 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:88
- quote: "`best`(거리 제곱)에서 $D = \\lceil\\sqrt{\\texttt{best}}\\rceil$로 올림해 쓴다."
- message: 원문의 `y−d ≤ y' ≤ y+d`를 정수 제곱거리(①②의 관행)와 접합하기 위한 구현 디테일 추가. 올림으로 창이 넓되 좁지 않아 후보를 놓치지 않는다는 설명은 옳고, 시리즈의 부동소수점 회피 원칙과 정합적. 원문과 모순되지 않는 정당한 보강.
- recommendation: 유지.

### L7 논증·복잡도 정확성 — 검증 완료
- severity: 🟢 · source: L · rule_id: L7 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:167
- quote: "n × O(log n) = O(n log n)"
- message: (1) 전체 O(n log n) 주장 옳음 — 초기 정렬 1회 O(n log n), 삽입/삭제 각 점당 상수 회 × O(log n), 구간 조회 O(log n + 상수). (2) "왼쪽 경계가 되돌아오지 않아 삭제 총 O(n)회" — `best`가 단조 감소하므로 옳음. (3) "후보는 D×2D 직사각형 안 상수 개" — 활성 집합의 두 점이 서로 ≥ 최소거리라는 사실 + 칸 세기로 성립. 코드 정답성은 브루트포스 차분 검증 3000건 통과로 확인.
- recommendation: 유지.

### L4 SVG↔본문 — sweep.svg y창 레이블 위치
- severity: 🟢 · source: L · rule_id: L4 · gate_effect: info
- location: public/images/closest-pair-3/sweep.svg:38
- quote: `<text x="537" y="196" ...>y_P + D</text>` / `<text x="537" y="230" ...>y_P − D</text>`
- message: y창 박스는 세로 150~270px(높이 120)인데, 경계 레이블 `y_P+D`(y=196)·`y_P−D`(y=230)가 박스 가장자리(150/270)가 아니라 중앙부에 몰려 있어, 창 높이(=2D)를 실제보다 좁게 오독할 여지가 있다. 캡션·색·나머지 요소는 본문과 일치.
- recommendation: 두 레이블을 박스 상·하단 가장자리(대략 y≈158, y≈266)로 옮기면 창 높이가 명확해진다. (경미)

### L1 문체(AI 신호)
- severity: 🟢 · source: L · rule_id: L1 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 줄표(—)와 마무리 문장("서로 다른 두 길이 같은 곳에서 만난 셈이다")의 밀도는 형제 글 ①②의 하우스 보이스와 동일 수준. 평서체(~다) 일관. 결정적 검사 D2(줄표 남발)·D3(강조 과다)도 통과.

### L2 설명 흐름·명료성
- severity: 🟢 · source: L · rule_id: L2 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 분할정복→훑기 전환 동기, 활성 집합, y창, BST 순으로 논리 도약 없이 이어진다.

### L3 용어·어체 일관성
- severity: 🟢 · source: L · rule_id: L3 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음. `best`(거리 제곱)와 `D`(실제 거리=√best)를 명확히 구분해 콜아웃에서 정의. "활성 집합/sweep line/창" 용어 일관.

### L5 제목·description 적합성
- severity: 🟢 · source: L · rule_id: L5 · gate_effect: info
- location: src/content/posts/closest-pair-3.md:2
- quote: "가장 가까운 점 쌍 ③ — Plane Sweeping과 균형 이진 탐색 트리"
- message: 검토 완료, 이슈 없음. 제목·description이 본문(평면 훑기 + std::set으로 O(n log n))을 정확히 대표.

### 검사 도구 결함 (D7 오탐의 근본 원인)
- severity: 🟡 · source: L · rule_id: L6 · gate_effect: warn
- location: .claude/review_post.py:54
- quote: `CANONICAL_DIFFICULTIES = {"입문", "중급", "심화"}`
- message: 검사기와 `docs/reviews/README.md:72`가 난이도 3단계 시절 목록을 유지하고 있어, `초급`·`고급`을 쓰는 모든 글에 대해 D7 오탐을 낸다(현재 발행된 closest-pair 3개 글 전부 해당). 스키마(`config.ts`)가 정답.
- recommendation: `CANONICAL_DIFFICULTIES`를 `{"입문","초급","중급","고급","심화"}`로, README의 difficulty 목록도 5단계로 갱신. **이 리포트 범위 밖 후속 작업**으로 처리 권장(포스트 수정 아님).

요약: 🔴 1 · 🟡 1 · 🟢 9

> 🔴 1건(D7)은 낡은 검사기로 인한 **오탐**이며 포스트 내용 결함이 아니다. 포스트 자체에서 발견된 콘텐츠 결함(🔴/🟡)은 없다. 경미한 폴리시 1건(sweep.svg 레이블 위치)만 선택적으로 반영 권장.
