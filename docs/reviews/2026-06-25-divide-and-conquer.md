## 결정적 검사: src/content/posts/divide-and-conquer.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/divide-and-conquer.md

### Findings

#### 🟢 [L1] src/content/posts/divide-and-conquer.md:194

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/divide-and-conquer.md:194
- quote: `분할 정복이 "나눠서" 정복한다면, 그리디는 "한 걸음씩" 정복한다 — 같은 문제도 전략에 따라 전혀 다른 모습으로 풀린다.`
- message: 본문 줄표(—) 사용은 대부분 섹션 제목(시리즈 컨벤션)에 한정되고 본문 내 남발은 없다. 마지막 "다음 글" 콜아웃의 대구 문장이 다소 경구식이나, 기존 포스트의 마무리 콜아웃 톤과 일관된 범위다.
- recommendation: 현재 문체를 유지한다. 평서체(~다)와 절제된 줄표 사용이 시리즈와 일치한다.
- gate_effect: info

#### 🟢 [L2] src/content/posts/divide-and-conquer.md:50

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/divide-and-conquer.md:50
- quote: `세 단계가 그대로 드러난다. sort(a, h) 와 sort(a + h, n - h) 가 나누고 푸는 부분이고, merge 가 합치는 부분이다.`
- message: 나누기→풀기→합치기 틀에서 병합 정렬, 점화식, 대입법, 메모리 약점, 힙 정렬, 하한으로 이어지는 논리 흐름에 도약이나 빠진 전제가 없다. 기존 sort/recursion 포스트로 상세 증명을 위임하는 처리도 명료하다.
- recommendation: 현재 설명 흐름을 유지한다.
- gate_effect: info

#### 🟢 [L3] src/content/posts/divide-and-conquer.md:62

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/divide-and-conquer.md:62
- quote: `**병합 정렬(merge sort)** 은 분할 정복의 교과서적 예다.`
- message: 병합 정렬·힙 정렬·퀵 정렬, 결정 트리, 정렬 순서, 제자리 정렬 등 용어가 본문과 SVG에서 일관되게 쓰였다. 어체도 ~다 평서체로 통일됐다.
- recommendation: 현재 용어 체계를 유지한다.
- gate_effect: info

#### 🟢 [L4] public/images/divide-and-conquer/dnc-framework.svg

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/divide-and-conquer/dnc-framework.svg
- quote: `나누고, 풀고, 합친다`
- message: 나누기(파랑, 하향)·풀기(초록, 기저 크기 1)·합치기(주황, 상향) 3단계와 본문의 분할 정복 틀이 정확히 대응한다. 병합 정렬의 절반 분할 구조와도 일치한다.
- recommendation: 현재 SVG와 본문 연결을 유지한다.
- gate_effect: info

#### 🟢 [L4] public/images/divide-and-conquer/decision-tree.svg

- severity: 🟢
- source: L
- rule_id: L4
- location: public/images/divide-and-conquer/decision-tree.svg
- quote: `잎 ≥ n! 개 ⟹ 높이 h ≥ log₂(n!) = Θ(n log n)`
- message: n=3 결정 트리의 6개 잎(abc·acb·cab·bac·bca·cba)이 각 비교 분기(a:b, b:c, a:c)의 결과와 모두 정확히 일치하며, abc·cba가 깊이 2, 나머지가 깊이 3인 비대칭 구조까지 올바르다. 하단 결론식이 본문의 하한 증명과 정확히 일치한다.
- recommendation: 현재 SVG와 본문 연결을 유지한다.
- gate_effect: info

#### 🟢 [L5] src/content/posts/divide-and-conquer.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/divide-and-conquer.md:2
- quote: `title: "분할 정복 — 나누어 풀고, 정렬의 한계를 증명하다"`
- message: 제목이 분할 정복 패러다임과 정렬 하한이라는 클라이맥스를 모두 담고, description이 대입법·메모리·힙 정렬·하한 증명 등 본문 구성을 정확히 대표한다.
- recommendation: 현재 제목과 description을 유지한다.
- gate_effect: info

#### 🟢 [L6] src/content/posts/divide-and-conquer.md:118

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/divide-and-conquer.md:118
- quote: `**힙 정렬(heap sort)** 은 배열 안에서 **최대 힙(max-heap)** 을 만들고 허무는 방식으로, 추가 배열 없이 정렬한다.`
- message: 노션 원본("Divide and Conquer", 151cb27e...)과 대조함. 기본 틀·재귀 병합 정렬·대입법 시간 분석·메모리 비용·힙 정렬·정렬 하한(비교 모델, n!, log(n!)) 6개 주제가 모두 반영됐다. 두 곳에서 원본을 의도적으로 보강했다: ① 힙 정렬은 원본의 다소 부정확한 단계 서술 대신 표준 in-place heapsort로 정리(원본 의도와 동일), ② 하한 증명은 원본이 log(n^n)>log(n!) 한쪽 방향만 제시한 것을 (n/2)^{n/2} 하계까지 더해 Θ(n log n)으로 엄밀화. 원본에 없는 자의적 주장 추가는 없다.
- recommendation: 보강 모두 정확성 향상 방향이라 유지 권고. 원본의 garbled한 힙 서술을 따르지 않은 것은 적절하다.
- gate_effect: info

#### 🟢 [L7] src/content/posts/divide-and-conquer.md:88

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/divide-and-conquer.md:88
- quote: `-a\,n + 2c + n = c`
- message: ① 대입법: T(n)=an log n+bn+c를 T(n)=2T(n/2)+n에 대입하면 log(n/2)=log n−1 전개 후 n계수 −a+1=0→a=1, 상수 2c=c→c=0이 정확히 떨어진다. ② 하한: 잎≥n!, 이진 트리이므로 2^h≥n!→h≥log₂(n!); n!≤n^n과 n!≥(n/2)^{n/2}로 log₂(n!)=Θ(n log n) 양방향이 닫혀 h=Ω(n log n) 결론이 MECE하게 완결된다. ③ 복잡도: 병합 정렬 Θ(n log n)+추가 메모리 O(n), 힙 정렬 O(n log n)+추가 메모리 O(1) 모두 정확. 결정 트리 잎 6개도 비교 결과와 일치.
- recommendation: 현재 논증과 복잡도 설명을 유지한다.
- gate_effect: info

요약: 🔴 0 · 🟡 0 · 🟢 8
