# 볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers (포스트 설계)

- 날짜: 2026-07-14
- 상태: 승인됨 (사용자 확인)
- 원본 자료: 노션 `Convex hull 2` 노트의 Farthest Point 섹션
- 선행 포스트: `src/content/posts/convex-hull-4.md` (PR #32, 머지됨) — 5편을 예고함
- 시리즈: 볼록 껍질 마지막(5) 편

## 목표

볼록 껍질 시리즈의 마지막 편. 1~4편이 "껍질을 어떻게 구하는가"였다면, 5편은
**껍질을 도구로 쓰는** 문제로 전환한다. 평면에서 **가장 먼 두 점(지름, diameter)**
을 찾되, 모든 쌍 비교 $O(N^2)$ 대신 껍질을 구한 뒤 **Rotating Calipers**로
$O(N)$에 훑어 전체 $O(N \log N)$에 푼다. 시리즈를 매듭짓는 편.

## 스코프 결정 (브레인스토밍 확정)

- **본편**: 직관 + 의사코드로 Rotating Calipers 핵심 메커니즘까지 다룬다 —
  대척점 쌍(antipodal pair) 정의, 평행선 회전, hull 위 두 포인터를 "더 작은 각도로
  벌어진 쪽" 전진, 한 바퀴 순회 $O(N)$, C++ 의사코드.
- **엣지 케이스는 본문에서 제외**: 평행 변 동시 접촉, 대척점 쌍의 정확한 열거,
  두 포인터가 동시에 움직이는 경우 등은 흐름을 끊으므로 **별도 '추가 설명' 페이지**로
  분리(feedback-hard-topics-separate-page 방침). 본편은 "다음 글에서 상세"라는
  forward reference만 둔다(죽은 링크 아님).
- **추가 설명 페이지는 5편 발행 후 별도 작업**(별도 spec/plan/PR). 3편 → bst-tangent
  방식. difficulty 고급.
- difficulty는 **심화**(4편과 동일 톤). 마지막 편이라 마무리 톤을 얹는다.

## 파일 / 메타데이터

- 본문: `src/content/posts/convex-hull-5.md`
- 이미지: `public/images/convex-hull-5/*.svg` (1~4편 스타일·팔레트 유지)
- frontmatter
  - title: "볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers"
  - date: 2026-07-14T09:00:00 (실제 작성일 기준)
  - tags: ["Algorithm", "Convex Hull", "Computational Geometry", "Rotating Calipers"]
  - category: algorithm
  - difficulty: 심화
  - description: **160자 이하**(SEO — 지름=껍질 꼭짓점, 평행선 회전·대척점, Rotating
    Calipers로 O(N²)→O(N) 요지)

## 본문 구성

1. **되짚어보기 & 전환** (도입 blockquote)
   - 1~4편은 껍질을 *구했다*(Package Wrapping, Graham Scan, Plane Sweeping, D&C).
   - 5편은 껍질을 *도구로 쓴다*: 평면에서 가장 먼 두 점(지름).
   - 시리즈 마무리임을 짧게.
2. **목차 callout**.
3. **1차원 워밍업**
   - 1차원에서 가장 먼 두 점은 min·max → $O(N)$.
   - 2차원은 자명하지 않다. 모든 쌍 비교는 $O(N^2)$.
4. **가장 먼 두 점은 껍질 꼭짓점이다**
   - 내부에 있는 점이라면 바깥으로 밀어낼수록 더 멀어지므로 후보가 못 된다.
   - 따라서 껍질 위 꼭짓점만 검사하면 된다(짧은 논증). → hull을 먼저 구할 이유.
5. **평행선 회전과 대척점(antipodal pair)**
   - 평행한 두 지지선(supporting line)으로 껍질을 양쪽에서 떠받친다.
   - 각도를 0°→180°로 돌리면 맞닿는 점 쌍(대척점)이 바뀐다.
   - 각 대척점 쌍의 거리 중 최댓값이 지름. 가장 먼 쌍은 반드시 어떤 각도의
     대척점 쌍으로 나타난다.
6. **Rotating Calipers — $O(N)$**
   - 직선을 연속으로 돌리는 대신, hull 위 **두 포인터**를 회전시키며 대척점 쌍만
     순회한다.
   - 두 변 중 **더 작은 각도로 벌어진 쪽**의 포인터를 다음 꼭짓점으로 전진.
   - 두 포인터가 hull을 한 바퀴 도는 동안 만난 대척점 쌍 거리만 비교 → $O(N)$.
   - C++ 의사코드(1편 `struct P`/`ccw`, cross product 재사용).
   - 엣지 케이스(평행 변 동시 접촉 등)는 '추가 설명' 예고(callout-simple).
7. **복잡도**
   - 껍질 $O(N \log N)$ + 대척점 순회 $O(N)$ = 전체 $O(N \log N)$.
   - 모든 쌍 $O(N^2)$와 대비. 껍질을 먼저 구한 값이 여기서 회수된다.
8. **핵심 정리** (callout-key, 4개 항목).
9. **시리즈를 마치며** (callout)
   - 껍질을 구하는 네 가지 길 + 껍질을 도구로 쓰기로 시리즈 완결.
   - 엣지 케이스 '추가 설명' 예고, 계산 기하의 이웃 문제 [가장 가까운 점 쌍](/blog/closest-pair-1) 링크.

## SVG 도판 (3장)

1. `hull-vertices.svg` — 가장 먼 두 점이 껍질 위 꼭짓점임(내부 점은 밖으로 밀수록
   멀어짐)을 보이는 도판.
2. `antipodal.svg` — 볼록 다각형 + 평행한 두 지지선 + 맞닿는 대척점 쌍 + 지름 선분.
3. `calipers.svg` — hull 위 두 포인터(캘리퍼스)가 회전하며 대척점 쌍을 순회, 더 작은
   각도로 벌어진 쪽 포인터를 전진시키는 한 걸음.

스타일: 1~4편 `public/images/convex-hull-{1,2,3,4}/*.svg`와 동일 팔레트(배경
`#0f1117`, 제목 `#e2e8f0`, 각주 `#94a3b8`, 초록 `#34d399`/`#6ee7b7`, 파랑
`#93c5fd`/`#3b82f6`(채움 `#1e3a5f`), 주황 `#fbbf24`, 빨강 `#ef4444`/`#f87171`)와
viewBox ~680×420. 시리즈 도판과 톤 유지.

## 작업 절차 / 제약

- 모든 작업은 `feat/post-convex-hull-5` 브랜치에서. main 직접 커밋 금지.
- 커밋 메시지는 저장소 정책을 따른다(co-author 트레일러 넣지 않음 —
  feedback-no-coauthor-trailer).
- 코드는 실행 코드보다 의사코드 수준 C++, 컴파일 검증 불필요.
- `npm run build`로 content collection 스키마 + KaTeX 파싱 검증.
- 작성 후 `/review-post convex-hull-5`로 내용·문체·SVG 리뷰, 반영 후 재빌드.
- 5편 발행 후, 4편의 "이어지는 글" 텍스트 예고를 5편으로 하이퍼링크 연결
  (발행 후 앞 글 callout에 링크 연결 관례).
- 리뷰 반영 후 PR(Why 충분히, How 방법론 중심, 참조 코드 위치).

## 성공 기준

- 4편이 예고한 Farthest Point/지름(Rotating Calipers, $O(N \log N)$)을 전달한다.
- "가장 먼 두 점 = 껍질 꼭짓점"과 "대척점 쌍 최댓값 = 지름"의 직관이 분명히 남는다.
- Rotating Calipers 핵심(두 포인터, 더 작은 각도 전진, 한 바퀴 O(N))을 의사코드로
  전달하되, 어려운 엣지 케이스는 본문에 억지로 넣지 않고 '추가 설명'으로 예고한다.
- 1~4편과 문체·구성(callout, 핵심 정리, 마무리)이 일관된다.
- description이 160자 이하다.
