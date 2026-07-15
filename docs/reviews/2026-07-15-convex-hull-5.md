## 결정적 검사: src/content/posts/convex-hull-5.md
발견 사항 없음 ✅

schema_version: review-report/v2
target: convex-hull-5
generated_at: 2026-07-15
strict: false
summary: 🔴 0 · 🟡 1 · 🟢 8

## findings

| severity | source | rule_id | location | quote | message | recommendation | gate_effect |
|---|---|---|---|---|---|---|---|
| 🟡 | L | L4 | public/images/convex-hull-5/calipers.svg:12 | `<line x1="470" y1="87" x2="650" y2="327" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="7 5"/>` | line 12와 line 13의 두 지지선이 거의 평행하게 보이지만 정확히 평행하지 않습니다. line 12의 기울기는 `240/180 = 4/3`이고 line 13의 기울기는 `227/170`이라, Rotating Calipers 설명의 평행 지지선 그림으로는 미세한 불일치가 있습니다. | 한쪽 선의 좌표를 다시 계산해 다른 선과 같은 기울기를 갖게 하되, 볼록 껍질에 대한 유효한 지지선 접촉 위치는 유지하세요. | warn |
| 🟢 | L | L1 | src/content/posts/convex-hull-5.md:10 | `> [1편](/blog/convex-hull-1)부터 [4편](/blog/convex-hull-4)까지, 우리는 흩어진 점들의 볼록 껍질을 **구하는** 네 가지 길을 걸었다.` | 검토 완료, 이슈 없음. 문체가 시리즈 맥락과 학습 노트 톤을 유지하며 AI식 과장 표현으로 흐르지 않습니다. | 조치 없음. | info |
| 🟢 | L | L2 | src/content/posts/convex-hull-5.md:58 | `## Rotating Calipers — $O(N)$` | 검토 완료, 이슈 없음. 1차원 직관, 껍질 꼭짓점 후보 축소, 대척점 쌍, Rotating Calipers 순회로 설명 흐름이 자연스럽게 이어집니다. | 조치 없음. | info |
| 🟢 | L | L3 | src/content/posts/convex-hull-5.md:50 | `볼록 다각형을 **평행한 두 직선**으로 양쪽에서 떠받친다고 하자(자를 양옆에 대는 느낌).` | 검토 완료, 이슈 없음. 지지선, 대척점 쌍, 포인터, 외적 같은 용어와 어체가 본문 전반에서 일관됩니다. | 조치 없음. | info |
| 🟢 | L | L4 | public/images/convex-hull-5/antipodal.svg:4 | `<text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">평행선 회전과 대척점 쌍 (antipodal pair)</text>` | 검토 완료, 이슈 없음. SVG의 대척점 쌍, 지름, 지지선 표기가 본문 설명과 맞습니다. | 조치 없음. | info |
| 🟢 | L | L4 | public/images/convex-hull-5/hull-vertices.svg:9 | `<text x="340" y="30" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">가장 먼 두 점은 껍질 꼭짓점이다</text>` | 검토 완료, 이슈 없음. 내부 점을 바깥으로 밀수록 멀어진다는 그림의 핵심이 본문 주장과 맞습니다. | 조치 없음. | info |
| 🟢 | L | L5 | src/content/posts/convex-hull-5.md:2 | `title: "볼록 껍질 ⑤ — 가장 먼 두 점과 Rotating Calipers"` | 검토 완료, 이슈 없음. 제목과 description이 글의 실제 범위인 볼록 껍질 기반 지름 찾기와 Rotating Calipers를 정확히 반영합니다. | 조치 없음. | info |
| 🟢 | L | L6 | src/content/posts/convex-hull-5.md:4 | `description: "볼록 껍질을 도구로 써서 평면의 가장 먼 두 점(지름)을 찾는다. 가장 먼 쌍은 껍질 꼭짓점이며, 평행선을 돌리며 대척점 쌍만 훑는 Rotating Calipers로 모든 쌍 O(N²) 대신 O(N)에 얻는다."` | 검토 완료, 이슈 없음. 관련 spec line 5가 Notion `Convex hull 2` / Farthest Point를 식별하지만, Notion URL이나 page ID가 제공되지 않아 source-page comparison은 수행할 수 없었습니다. 저장소 내 글만 기준으로는 소스 충실성에 추가 이슈가 없습니다. | Notion 원문 URL 또는 page ID가 확보되면 별도 비교 검토를 수행하세요. | info |
| 🟢 | L | L7 | src/content/posts/convex-hull-5.md:91 | `위 의사코드는 **일반 위치(동률 없는 경우)를 가정한 기본 뼈대**다.` | 검토 완료, 이슈 없음. 글은 의사코드를 no-tie skeleton 범위로 올바르게 제한하고, 그 stated scope 안에서 유효한 O(H) traversal / O(N log N) total complexity를 제시합니다. | 조치 없음. | info |

요약: 🔴 0 · 🟡 1 · 🟢 8

## 반영 결과 (2026-07-15)

- 🟡 [L4] `calipers.svg` 두 지지선이 정확히 평행하지 않음(위 4/3, 아래 227/170) — **반영 완료**. 아래 지지선을 `(70,193)-(240,420)` → `(69,192)-(240,420)`으로 바꿔 기울기를 정확히 `228/171 = 4/3`로 맞췄다. 위 지지선 `(470,87)-(650,327)`은 이미 `240/180 = 4/3`. 두 선이 정확히 평행. 아래 선은 여전히 포인터 j 중심 `(150,300)`을 지난다(x=150에서 y = 192 + 81·4/3 = 300). 지지선 접촉 위치·유효성 유지.
- 재검증: `npm run build` 성공, `python .claude/review_post.py convex-hull-5` "발견 사항 없음 ✅".
