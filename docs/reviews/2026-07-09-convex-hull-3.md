## 결정적 검사: src/content/posts/convex-hull-3.md

🟡 권장 (1)
- [D2] src/content/posts/convex-hull-3.md:32, src/content/posts/convex-hull-3.md:38, src/content/posts/convex-hull-3.md:44  줄표(—) 10회 — 임계치(9) 초과. AI 문체 신호 샘플 위치: src/content/posts/convex-hull-3.md:32, src/content/posts/convex-hull-3.md:38, src/content/posts/convex-hull-3.md:44

요약: 🔴 0 · 🟡 1 · 🟢 0

## LLM 비평: src/content/posts/convex-hull-3.md

🟡 권장 (1)
- severity: 🟡 · source: L · rule_id: L1 · location: src/content/posts/convex-hull-3.md:78 · gate_effect: warn
  - quote: `**안쪽 추가 — 껍질은 그대로다.**`
  - message: 문장 내부·굵게 리드의 줄표가 임계치를 1회 초과(D2와 동일 사안). 섹션 제목과 이미지 alt의 구조적 줄표는 1·2편과 일관되어 유지 가능하지만, Dynamic Case의 굵게 리드 두 곳("안쪽 추가 —", "바깥쪽 추가 —")은 접속형으로 풀 수 있다.
  - recommendation: 굵게 리드 줄표를 "~라면"으로 풀어 임계치 이하로 낮춘다.

🟢 참고 (11)
- severity: 🟢 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-3.md:60 · gate_effect: info
  - quote: `if (ccw(p, hull[up],  hull[i]) > 0) up  = i;`
  - message: 접점을 쌍대 비교로 갱신하는 선형 탐색이 옳다. p가 항상 가장 오른쪽이라 모든 껍질 점이 x < p.x 반평면에 있고, p에서 본 방향각이 180° 미만 구간에 모여 전순서를 이룬다. 따라서 "더 위로/아래로 도는 점"을 쌍대로 누적하면 실제 접점에 수렴한다. Dynamic Case에서는 p가 최우측 보장이 없어 이 스캔이 그대로 통하지 않는데, 본문이 "조금 더 갈린다"며 상세를 미룬 것과 일치.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L7 · location: src/content/posts/convex-hull-3.md:91 · gate_effect: info
  - quote: `각 점은 평생 한 번 삽입되고 최대 한 번 삭제된다.`
  - message: 삭제 분할상환 논증 정확. 삽입 O(log N)×N, 삭제 총합 ≤ N회×O(log N) → 전체 O(N log N). 복잡도 주장 옳음.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L6 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 소스 대조 완료(노션 `Convex hull 2` 노트, 대화 내 fetch본 기준). Plane Sweeping O(N²)/O(N log N), upper·lower 분해, Dynamic Case(내부는 BST+CCW 판정, 외부는 접선 2개 splice)가 모두 반영됨. 노션의 "right hull" 프레이밍을 upper/lower 분해로 정리했는데 노트가 두 분해를 모두 소개하므로 왜곡 아님. BST 방향 판정 케이스 분석은 계획대로 예고로 분리. 자의적 추가 없음.
  - recommendation: 조치 불요. n=3 base case, "right hull 점 1개 불가" 등 지엽 항목은 생략(허용 범위).
- severity: 🟢 · source: L · rule_id: L1 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 줄표 외 항목(경구식 마무리, 과한 비유, 대칭 반복, 과한 강조) 검토 완료, 이슈 없음. ~다 평서체 일관.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L2 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. upper/lower 분해 → 스위핑 O(N²) → BST O(N log N) → Dynamic으로 이어지는 흐름이 자연스럽고, 각 절이 앞 절 도구를 재사용하는 서사가 명확.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L3 · location: not-recorded · gate_effect: info
  - quote: not-recorded
  - message: 검토 완료, 이슈 없음. 용어(껍질/사슬/접선/접점/upper·lower hull/CCW) 일관.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L4 · location: src/content/posts/convex-hull-3.md:34 · gate_effect: info
  - quote: `![껍질을 반으로 나누기 — 최좌측 L과 최우측 R이...](/images/convex-hull-3/upper-lower.svg)`
  - message: SVG 5장 검토 완료, 이슈 없음. upper-lower(L 최좌·R 최우 확인, 상·하 사슬 색 구분), sweep-tangent/sweep-result(공유 점 배치, p 최우측, 접점 사이 c3·c4가 버려지고 새 껍질에서 내부로), bst-idea(y오름차순 B<A<C<E<D의 균형 BST 구조가 in-order와 일치), dynamic(안쪽 X 불변 / 바깥쪽 X 접선 2개+제거점) 모두 본문 서술과 부합.
  - recommendation: 조치 불요.
- severity: 🟢 · source: L · rule_id: L5 · location: src/content/posts/convex-hull-3.md:2 · gate_effect: info
  - quote: `title: "볼록 껍질 ③ — Plane Sweeping과 동적 갱신"`
  - message: 검토 완료, 이슈 없음. 제목·description이 Plane Sweeping(O(N²)→O(N log N))과 Dynamic Case라는 실제 범위를 대표.
  - recommendation: 조치 불요.

요약(전체): 🔴 0 · 🟡 2 · 🟢 11

## 반영 결과 (2026-07-09)

- [D2/L1] Dynamic Case 굵게 리드 두 곳의 줄표를 "~라면"으로 풀어 줄표 임계치 이하로 낮춤. 재검사 결과 "발견 사항 없음 ✅".
- L6(소스 충실성)·L7(논증·복잡도)은 검증 통과로 조치 없음.
- 반영 후 `npm run build` 통과 (104 pages).
