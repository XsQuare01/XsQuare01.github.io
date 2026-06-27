## 결정적 검사: src/content/posts/quicksort.md
발견 사항 없음 ✅

## LLM 비평

### src/content/posts/quicksort.md

#### 🔴 [L7] src/content/posts/quicksort.md:37
- severity: 🔴
- source: L
- rule_id: L7
- location: src/content/posts/quicksort.md:37
- quote: `int sort(int a[], int n) {`
- message: partition 의사코드가 실제로 틀린 동작을 한다. (1) base case(`if (n <= 1) return;`)가 없다. pivot이 최솟값이라 분할 경계 `j`가 0이 되면 `sort(a, j)`가 `sort(a, 0)`으로 호출되고, 그 안에서 `j = n-1 = -1`, `swap(a[0], a[-1])`로 범위 밖 접근과 비종료 재귀가 일어난다(예: `[1,3,2]`는 분할 후 `sort(a, 0)`을 부른다). (2) base case를 두더라도 n=2 오름차순에서 틀린다. `[1,2]`는 `i=1, j=1`로 시작해 외부 `while(i<j)`가 한 번도 돌지 않아 `j`가 1로 남고, 마지막 `swap(a[0], a[j])`가 이미 정렬된 `[1,2]`를 `[2,1]`로 뒤집는다. 노션 원문 코드를 그대로 옮긴 것이지만, 요청한 "내용이 틀렸을 때만 수정" 기준에 정확히 해당하는 실제 결함이다.
- recommendation: `if (n <= 1) return;` base case를 추가하고, 분할 종료 시 경계 `j`가 항상 `a[j] <= p`를 만족하도록 포인터 진행을 정리한다. 가장 안전한 방법은 sort.md가 이미 채택·증명한 경계 인덱스 `s` 방식 partition으로 교체하는 것이다. 그게 아니면 "실행 코드가 아닌 도식적 의사코드"임을 명시해 독자가 그대로 컴파일·실행하지 않게 한다.
- gate_effect: fail

#### 🟡 [L3] src/content/posts/quicksort.md:189
- severity: 🟡
- source: L
- rule_id: L3
- location: src/content/posts/quicksort.md:189
- quote: `잘 알려진 대로 $H_n \approx \ln n$이다. 따라서 추가항들의 총합은 약 $2\ln n - 3$이고`
- message: 189행은 자연로그 `\ln n`으로 쓰고, 곧바로 192·204·207·219행은 `\log n`으로 표기가 바뀐다(`2\log n - 3`, `2(n+1)\log n`). 점근적으로는 상수배 차이뿐이라 결론 Θ(n log n)에 영향은 없지만, 심화 수학 글에서 같은 양을 `ln`과 `log`로 섞어 쓰면 독자가 로그의 밑(base)이 바뀐 것으로 오해할 수 있다.
- recommendation: `H_n \approx \ln n`을 유지하되 "상수배 차이뿐이라 $\Theta$에서는 $\log n$과 같다"는 한 줄을 덧붙이거나, 본문 전체를 `\log`(또는 `\ln`) 한쪽으로 통일한다.
- gate_effect: warn

#### 🟢 [L1] src/content/posts/quicksort.md:66
- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/quicksort.md:66
- quote: `분할의 **결과**는 같고 **경로**가 다를 뿐이다.`
- message: 대칭 구문("결과는 같고 경로가 다를")으로 문단을 닫는 경구식 마무리에 가깝다. 또한 본문에 줄표(—)가 약 5곳(18·22·61·93·176행) 쓰였다. 모두 기존 하우스 스타일(divide-and-conquer 등) 허용 범위 안이지만, L1 AI 신호 관점에서 참고로 남긴다.
- recommendation: 필요하면 66행을 "분할 결과는 같지만 거기에 이르는 경로가 다르다."처럼 풀고, 줄표 일부를 마침표·접속사로 바꾼다. 어체(~다 평서체)는 유지.
- gate_effect: info

#### 🟢 [L2] src/content/posts/quicksort.md:42
- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/quicksort.md:42
- quote: `if (i == n || j == 0) break;`
- message: 42행의 경계 가드(`i==n || j==0`)와, 43행 주석 "p보다 큰 값을 만날 때까지"가 실제로는 `a[i] < p`가 깨지는 지점(= p 이상)에서 멈춘다는 점(중복 값 `a[i]==p` 처리 포함)이 본문에서 설명되지 않는다. 흐름상 큰 지장은 없으나 심화 독자가 가드의 의도를 궁금해할 수 있다.
- recommendation: 가드의 역할(포인터가 배열 밖으로 나가지 않게 함)과 pivot과 같은 값의 처리 규칙을 한 문장 보강한다. sort.md의 3-way partition 설명으로 링크해도 좋다.
- gate_effect: info

#### 🟢 [L4] not-recorded
- severity: 🟢
- source: L
- rule_id: L4
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. partition-pointers.svg의 예제 `[5,3,8,1,7,2,6]`(pivot 5에서 i가 8, j가 2에 멈춰 swap)은 본문 과정 설명과 정확히 일치한다. average-split.svg의 등수 분배(k=1 / k≈n/2 / k=n)와 점화식 `E(n)=(1/n)·Σ(E(k−1)+E(n−k))+n`은 표·본문과 일치하고, recursion-depth.svg의 균형(O(n log n))·쏠림(O(n²)) 깊이도 본문과 일치한다.
- recommendation: 현행 유지.
- gate_effect: info

#### 🟢 [L5] not-recorded
- severity: 🟢
- source: L
- rule_id: L5
- location: not-recorded
- quote: not-recorded
- message: 검토 완료, 이슈 없음. 제목 "최악 O(n²)인데 평균은 왜 O(n log n)인가"와 description은 글의 핵심(최선/최악 격차와 기댓값 점화식으로 평균 Θ(n log n) 유도)을 잘 대표한다.
- recommendation: 현행 유지.
- gate_effect: info

#### 🟢 [L6] src/content/posts/quicksort.md:74
- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/quicksort.md:74
- quote: `퀵 정렬이 실측에서 빠른 큰 이유 중 하나가 **제자리(in-place) 분할**이라는 점을 생각하면`
- message: 노션 원본("⚡ Quick Sort", 154cb27e…)을 notion-fetch로 대조함. 원문 핵심(분할 코드, 7단계 과정, 배열 2개 방식, 최선/최악, 평균 점화식 유도, 겸손한 맺음말)은 모두 보존됨. 원문에 없는 추가 framing이 일부 있다: 제자리(in-place)·캐시 지역성(74·210·220행), 무작위 pivot/무작위화 퀵 정렬(210·227행). 모두 표준적이고 정확한 사실이며 sort.md 기존 서술과 일관되나, 원문 외 추가임을 투명하게 남긴다. 또한 원문 평균 유도의 표기 오류 한 줄(`E(n)/(n+1) = E(n-1)/n + 2log n − 3`)은 192행에서 의도적으로 보정함(누적합과 단일 점화 단계의 혼동 제거).
- recommendation: 추가 framing은 유지해도 무방하다. 원문 충실성을 엄격히 본다면 "무작위화 퀵 정렬" 언급을 sort.md 링크로 대체해 출처를 분명히 할 수 있다.
- gate_effect: info

#### 🟢 [L7] src/content/posts/quicksort.md:120
- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/quicksort.md:120
- quote: `E(n) = \sum_{k=1}^n \frac{E(k-1) + E(n-k)}{n} + n`
- message: 평균 케이스 유도는 각 단계를 검산한 결과 대수적으로 옳다. 점화식 → `nE(n)=2ΣE(k)+n²` → 차분으로 `nE(n)=(n+1)E(n-1)+2n-1` → 부분분수 `(2n-1)/(n(n+1)) = -1/n + 3/(n+1)` → 텔레스코핑 → `2H_n-3`(≈2ln n) → `E(n)≈2(n+1)log n = Θ(n log n)`까지 모두 일치한다. 192행의 "한 줄 주의" 콜아웃도 원문 함정(중복 계상)을 정확히 짚는다.
- recommendation: 현행 유지(표기 일관성은 L3 참고).
- gate_effect: info

요약: 🔴 1 · 🟡 1 · 🟢 6

---

## 반영 결과 (2026-06-27)

| 항목 | 판단 | 조치 |
|---|---|---|
| 🔴 L7 (line 37) | 반영 | partition 의사코드를 올바른 두 포인터 방식으로 교체. `if (n <= 1) return;` 기저 사례 추가, 외부 루프를 `while (i <= j)`로 바꾸고 swap 시 `i++/j--`로 진행해, 종료 시 경계 `j`가 항상 `a[j] ≤ p`를 만족하도록 정리. 반례 `[1,2]→[1,2]`, `[1,3,2]→[1,2,3]`(OOB 없음), 중복 `[2,2,1]→[1,2,2]`, SVG 예제 `[5,3,8,1,7,2,6]→[1,2,3,5,6,7,8]` 트레이스로 검증. 본문 7단계 서술과 SVG(첫 swap 8↔2)는 그대로 유효. |
| 🟡 L3 (line 189) | 보류 | `ln`/`log` 표기 혼용은 Θ 결론에 영향 없는 권장 사항. 사용자 요청(의사코드만 수정) 범위 밖이라 이번엔 미반영. 후속 정리 가능. |
| 🟢 L1·L2·L4·L5·L6·L7 | 정보 | 참고·coverage 항목. 조치 불필요. (L2의 `if (i==n||j==0)` 가드는 L7 코드 교체로 자연히 제거됨) |

`npm run build` 재검증 통과 (81 페이지). 반영 후 🔴 0 · 🟡 1(보류) · 🟢 6.
