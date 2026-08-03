schema_version: review-report/v2
target: quicksort
generated_at: 2026-08-03
strict: true
sources: src/content/posts/quicksort.md
summary: 🔴 0 · 🟡 1 · 🟢 6

## Findings

### 🟡 [L6] src/content/posts/quicksort.md:36-60

- severity: 🟡
- source: L
- rule_id: L6
- location: src/content/posts/quicksort.md:36-60
- quote: "while (i <= j && a[j] >= p) j--;  // p 이상인 동안 후진 → p 미만에서 멈춤"
- message: 노션 원문(⚡ Quick Sort, 알고리즘 수업 정리 하위)과 대조한 결과 이 글은 원문의 사실 오류 두 곳을 바로잡았는데, 그 사실이 스펙에도 인계물에도 기록되어 있지 않다. 첫째, 원문 분할 코드는 `while(j > 0 && a[j] > p) j--;`로 pivot과 같은 값에서 포인터가 멈추고, 바깥 조건도 `while(i < j)`에 `if(i == n || j == 0) break;` 가드를 둔 구조다. 이 글은 조건을 `a[j] >= p`로 바꾸고 `while (i <= j)` 구조로 재구성해 중복 원소 입력을 정확히 처리한다. 둘째, 원문 평균 분석의 마지막 식은 `E(n)/(n+1) = E(n-1)/n + 2log n - 3`으로, 한 칸 점화식의 우변에 텔레스코핑 총합을 그대로 더해 같은 양을 두 번 센다. 이 글은 이를 총합으로 대체하고 "한 줄 주의" 콜아웃에서 그 혼동을 명시적으로 경고한다. 두 수정 모두 내용상 옳고 AGENTS.md가 허용하는 사실 오류 정정에 해당하지만, 같은 규칙은 "원문의 의도와 달라지는 변경은 작업 결과에 명시한다"고 요구한다. quicksort는 `docs/superpowers/specs/`에 대응 스펙이 없어 이 정정이 남은 기록이 없다.
- recommendation: 이 리포트를 해당 기록으로 삼고, 이후 원문을 다시 대조할 때 참조할 수 있도록 두 정정을 스펙 또는 리뷰 인계물에 남긴다. 게시 본문에는 provenance 라벨을 넣지 않는다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/quicksort.md:1-236

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/quicksort.md:1-236
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L2] src/content/posts/quicksort.md:1-236

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/quicksort.md:1-236
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L3] src/content/posts/quicksort.md:1-236

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/quicksort.md:1-236
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] public/images/quicksort/partition-pointers.svg:51-52

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/quicksort/partition-pointers.svg:51-52
- quote: "j는 a[j] >= p 인 동안 후진 → p 미만인 값 2에서 멈춘다"
- message: 참조 SVG 세 개를 본문과 대조했다. `partition-pointers.svg`는 후진 조건을 `a[j] > p`로 적어 코드의 `a[j] >= p`와 어긋나 있었다. 그 표기대로면 pivot과 같은 값에서 포인터가 멈춰, 본문 63행이 "`[5, 5]`처럼 같은 값만 있는 입력에서도 멈추지 않는다"고 밝힌 성질이 깨진다. 이번 리뷰에서 두 레이블을 코드와 맞췄다. `average-split.svg`의 점화식 `E(n) = (1/n) · Σ ( E(k−1) + E(n−k) ) + n`은 본문 121행과 일치하고, `recursion-depth.svg`의 깊이 비교도 84행 최선·최악 서술과 일치한다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/quicksort.md:2-4

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/quicksort.md:2-4
- quote: not-recorded
- message: 검토 완료, 이슈 없음
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L7] src/content/posts/quicksort.md:104-211

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/quicksort.md:104-211
- quote: not-recorded
- message: 평균 분석 전개를 단계별로 검산했고 모두 맞는다. 점화식 `E(n) = Σ(E(k-1)+E(n-k))/n + n`에서 `nE(n) - (n-1)E(n-1) = 2E(n-1) + 2n - 1`, 따라서 `nE(n) = (n+1)E(n-1) + 2n - 1`이 옳다. 부분분수 `(2n-1)/(n(n+1)) = -1/n + 3/(n+1)`도 맞고, `F(n) = F(0) + 3(H_{n+1} - 1) - H_n ≈ 2 ln n - 3`으로 본문 결과와 일치한다. 분할 코드의 종료 후 불변식도 확인했다. 내부 루프가 `i > j`로 끝날 때 `j = i - 1`이고 `i`가 전진했다면 `a[i-1] < p`이므로, `swap(a[0], a[j])` 직전에 언제나 `a[j] < p` 또는 `j == 0`이다. `[5,5]`, `[2,1]`, `[3,1,2]`, `[1,3,2]`로 직접 추적해 정렬 결과가 옳음을 확인했다. 앞선 리포트(2026-06-27)가 지적한 중복 원소 무한 루프는 조건 비대칭으로 이미 해소돼 있었고, 남아 있던 "오른쪽에는 p보다 큰 값들만"이라는 서술은 이번 리뷰 직전 커밋에서 "p 이상"으로 바로잡았다.
- recommendation: not-recorded
- gate_effect: info
