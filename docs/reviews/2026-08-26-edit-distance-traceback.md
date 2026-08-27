schema_version: review-report/v2
target: edit-distance-traceback
generated_at: 2026-08-26
strict: true
sources: src/content/posts/edit-distance-traceback.md
summary: 🔴 0 · 🟡 2 · 🟢 5

## Findings

### 🟡 [L2] src/content/posts/edit-distance-traceback.md:90

- severity: 🟡
- source: L
- rule_id: L2
- location: src/content/posts/edit-distance-traceback.md:90
- quote: 두 문자열을 각각 뒤집어 같은 표를 한 번 더 채우면 $(i, j)$ 에서 $(n, m)$ 까지의 최소 비용 $D'(i, j)$ 를 얻는다.
- message: 뒤집은 표의 칸 $(i, j)$ 는 뒤집은 문자열의 접두사 쌍을 가리키므로, 원래 좌표의 $D'(i, j)$ 에 해당하는 값은 뒤집은 표의 $(n-i, m-j)$ 칸이다. 이 첨자 대응이 빠져 있어 판정식을 글자대로 구현하면 어긋난다. 판정식 $D(i, j) + D'(i, j) = D(n, m)$ 자체는 옳다. 리뷰에서 정·역 두 표로 다시 계산해 abcab/abcba의 영역 열 칸을 그대로 재현했다.
- recommendation: "뒤집어 채운 표의 $(n-i, m-j)$ 칸이 $D'(i, j)$ 다"는 한 문장을 넣는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/edit-distance-traceback.md:85

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance-traceback.md:85
- quote: 경로는 오른쪽과 아래로만 움직이므로 $(3, 4)$ 를 지난 뒤에는 열 번호가 4보다 작은 칸으로 갈 수 없다.
- message: "두 칸을 함께 지나는 경로는 없다"는 주장은 두 순서로 갈린다. $(3,4)$ 다음에 $(4,3)$ 이 오는 경우는 적어 둔 열 번호 논증이 닫지만, $(4,3)$ 다음에 $(3,4)$ 가 오는 경우는 행 번호가 줄어들 수 없다는 대칭 논증이 필요하고 그 절반이 빠져 있다. 경우 분할이 전체를 덮지 않는다. 같은 문장의 "오른쪽과 아래로만 움직이므로"도 본편 145~147행이 세 걸음(대각선·아래·오른쪽)으로 적은 이동을 둘로 줄여, 대각선 걸음이 이 논증에 어떻게 들어가는지 독자가 스스로 메워야 한다. 결론 자체는 옳다.
- recommendation: "$(4,3)$ 을 지난 뒤에는 행 번호가 3보다 작은 칸으로 갈 수 없다"는 대칭 절을 한 개 더하고, 이동을 "행 번호와 열 번호가 줄지 않는 걸음"으로 적어 대각선까지 세 걸음을 모두 덮는다.
- gate_effect: warn

### 🟢 [L1] src/content/posts/edit-distance-traceback.md:158

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/edit-distance-traceback.md:158
- quote: 물음의 답이 하나가 아닐 수 있다는 것, 그래서 결과가 길 하나가 아니라 영역이 된다는 것이 되짚기가 값 계산과 갈리는 지점이다.
- message: 한 문장에 의존명사 '것' 구문이 두 번 겹쳐 주어가 길어졌다. 루브릭 L1이 가리키는 '것' 줄이기 항목에 해당한다. 그 밖의 문체 신호는 없다. 문두 접속어 0회, 줄표는 제목과 링크 제목에만, 굵게는 용어 도입과 callout 항목에만 쓰인다.
- recommendation: "답이 하나가 아닐 수 있고, 그래서 결과가 영역이 된다는 점이 …"처럼 한 번으로 줄인다.
- gate_effect: info

### 🟢 [L3] src/content/posts/edit-distance-traceback.md:100

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/edit-distance-traceback.md:100
- quote: $C(i, j)$ 를 $(0, 0)$ 에서 $(i, j)$ 까지 가는 최적 경로의 개수라 하자.
- message: '최적 경로'가 70·75행에서는 $(0,0)$ 에서 $(n,m)$ 까지 가는 전역 최적 경로를, 100행에서는 $(i,j)$ 까지의 최소 비용 경로를 가리킨다. 두 대상은 다르다. 영역 안 칸을 지나는 전역 최적 경로의 수는 $C(i, j)$ 가 아니라 그 칸까지의 수와 그 칸에서 끝까지의 수의 곱이다. 100행이 양 끝점을 함께 적어 문맥으로는 갈리므로 참고 사항으로 남긴다.
- recommendation: 100행에 "여기서 최적은 그 칸까지의 최소 비용을 뜻한다" 정도의 한정을 붙이면 두 쓰임이 확실히 갈린다.
- gate_effect: info

### 🟢 [L4] src/content/posts/edit-distance-traceback.md:46

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/edit-distance-traceback.md:46
- quote: not-recorded
- message: 검토 완료, 이슈 없음 — traceback-path.svg의 표 30개 값, 경로 칸 $(5,5)$→$(0,0)$, 점선으로 남긴 두 후보 $(4,5)$·$(5,4)$, 연산 라벨(바꾸기 두 번과 맞추기 세 번)이 48·54행 서술과 맞다. alignments.svg의 세 정렬은 위아래 글자와 빈 칸을 읽으면 각각 바꾸기 두 번, 넣기와 지우기, 지우기와 넣기이고 60~62행과 일치한다. region.svg의 파선 칸 열 개는 격자 좌표로 (0,0)·(1,1)·(2,2)·(3,3)·(3,4)·(4,3)·(4,4)·(4,5)·(5,4)·(5,5)이며 리뷰에서 판정식으로 다시 계산한 영역과 같고, 세 색 경로가 세 정렬과 하나씩 대응한다. 의사코드 countOptimalPaths는 100행 설명과 같은 분기·순회 순서를 쓰고, 다시 돌려 abcab/abcba 3, abcabcd/abcdabc 1, aaaa/aa 6 = C(4,2), aaaaaa/aaa 20 = C(6,3)을 확인했다. 126·128행의 수와 일치한다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/edit-distance-traceback.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/edit-distance-traceback.md:2
- quote: 추가 설명 — 되짚기는 길 하나가 아니라 영역을 준다
- message: 검토 완료, 이슈 없음 — 제목이 이 글의 결론(결과가 길 하나가 아니라 영역)을 그대로 담고, description 두 문장이 값과 연산의 분리, 되짚기, 동점일 때의 영역이라는 본문 축을 순서대로 담는다. 스펙 초안보다 짧아졌지만 담는 내용은 같다. 경로 개수 세기 절이 description에 들어가지 않았으나 요약의 범위로는 무리가 없다. 본편과의 상호 링크가 도입부와 마무리 callout 양쪽에 있어 제목의 '추가 설명' 표기와 실제 관계가 맞는다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] src/content/posts/edit-distance-traceback.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/edit-distance-traceback.md:1
- quote: not-recorded
- message: approved extension — 노션 원문에 직접 접근할 도구가 없어 승인된 설계 스펙 docs/superpowers/specs/2026-08-26-edit-distance-design.md를 대조 자료로 삼았다. 이 편은 원문 줄기 8(거슬러 올라가며 무슨 연산이었는지 찾고, 답이 여러 개 나올 수 있어 결과가 영역으로 나온다)과 원문 요청 4를 받는 확장 편이며, 스펙 provenance 표가 되짚기 규칙, 최적 경로 DAG, 영역의 정의, 경로 개수 세기, abcab/abcba 예시를 모두 확장으로 등재해 두었다. 절 구성이 스펙 2.4의 일곱 항목과 순서까지 같고 원문 줄기 8의 두 요소가 모두 보존된다. 스펙이 쓴 '부분 DAG'가 본문에서 '칸의 집합'으로 풀린 것은 원문 어휘가 아니라 스펙의 설명 어휘이고 뜻이 같아 불일치로 보지 않았다. 90행의 영역 판정식 callout은 provenance 표에 개별 항목으로 없으나 '영역의 정의'라는 승인 항목 안의 상세이고 원문의 의도를 훼손하지 않는다.
- recommendation: 스펙 provenance 표에 영역 판정식(정·역 두 표)을 한 줄로 등재하면 확장 목록과 본문이 정확히 맞는다. 본문 수정은 필요하지 않다.
- gate_effect: info

## 후속 처리

- 🟡 [L7] `src/content/posts/edit-distance-traceback.md:85` — **반영 완료**. "경로는 오른쪽과 아래로만 움직이므로 $(3, 4)$ 를 지난 뒤에는 열 번호가 4보다 작은 칸으로 갈 수 없다."를 두 순서($(3,4)$→$(4,3)$ 과 $(4,3)$→$(3,4)$)를 모두 닫는 대칭 논증으로 바꿨다. 이동도 오른쪽·아래 둘로 줄이던 서술을 "오른쪽·아래·대각선 셋"으로 고쳐, 본편(edit-distance.md) 145~147행이 적은 세 걸음과 표현을 맞췄다.
- 🟡 [L2] `src/content/posts/edit-distance-traceback.md:90` — **반영 완료**. "두 문자열을 각각 뒤집어 같은 표를 한 번 더 채우면 $(i, j)$ 에서 $(n, m)$ 까지의 최소 비용 $D'(i, j)$ 를 얻는다."에 뒤집은 표의 어느 칸이 $D'(i, j)$ 인지 밝히는 문장을 더했다. "뒤집은 표의 칸 $(n-i, m-j)$ 가 원래 표에서 $(i, j)$ 에서 $(n, m)$ 까지 가는 최소 비용이고, 이 값을 $D'(i, j)$ 라 하자."로 첨자 대응을 명시해, 판정식 $D(i, j) + D'(i, j) = D(n, m)$ 을 글자대로 구현할 수 있게 했다.

판정을 바꾸는 수정은 없다. 영역 판정식 자체, 두 표를 $O(NM)$ 에 채운다는 복잡도, abcab/abcba 예시는 그대로다.

재검증: `python .claude/review_post.py src/content/posts/edit-distance.md src/content/posts/edit-distance-traceback.md` 두 파일 모두 발견 사항 없음, `npm run build` 141 page(s) built, `npm run test:js` 21/21 통과.

### 전체 브랜치 리뷰 반영 (2026-08-26, 추가)

아래는 위 rubric finding에서 이미 다룬 지적이 아니라, 별도로 진행한 전체 브랜치(whole-branch) 리뷰가 새로 낸 지적을 반영한 기록이다. Important 2건, Minor 3건.

- `src/content/posts/edit-distance-traceback.md:28` — "값을 구하는 데 필요하지 않았기 때문이다." 뒤에 "본편이 두 행만 남겨 공간을 줄인 판을 보였는데, 되짚기는 그 판으로 할 수 없다. 지나온 칸을 하나씩 되물어야 하므로 표가 통째로 남아 있어야 한다."를 더했다. 본편의 두 행 공간 절약 판과 되짚기가 표 전체를 요구한다는 점이 이 쌍 어디에서도 맞물리지 않던 것을 닫았다(Important).
- `src/content/posts/edit-distance-traceback.md:38` — "$t(i, j) = 0$ 이면 맞추기, 1이면 바꾸기다"를 "$t(i, j)$ 는 $S_1[i]$ 와 $S_2[j]$ 가 같으면 0, 다르면 1이므로, 0이면 맞추기고 1이면 바꾸기다"로 풀었다. `t(i, j)`가 본편의 정리 1 안에서만 정의되고 이 글에는 무설명으로 등장하던 문제를 닫았다(Minor).
- `src/content/posts/edit-distance-traceback.md:100` — "나머지 칸에서는 되짚기 등식이 성립하는 이웃의 $C$ 를 더한다." 뒤에 "본편처럼 본문의 인덱스는 1부터 세고 배열은 0부터 세므로, 코드에서 글자를 꺼낼 때 하나를 뺀다."를 더했다. 본편이 밝힌 1-기반/0-기반 인덱스 관례를 이 글에서는 밝히지 않고 코드로 바로 넘어가던 것을 닫았다(Minor).
- `src/content/posts/edit-distance-traceback.md:136` — "대각선을 먼저 검사하면 빈 칸을 되도록 늦게 만들고, 위쪽을 먼저 검사하면 지우기를 앞으로 몰아 놓는다."를 "되짚기는 정렬을 뒤에서부터 복원하므로, 대각선을 먼저 보면 뒤쪽에서 최대한 글자를 짝지어 나가고 빈 칸은 정렬의 앞쪽으로 밀린다. 위쪽을 먼저 보면 지우기가 뒤쪽에 먼저 놓인다."로 바꿨다. 되짚기가 뒤에서부터 복원한다는 이 글 자신의 서술과 어긋나게 앞/뒤 방향이 뒤집혀 있던 문장을 바로잡았다(Important).
- `src/content/posts/edit-distance-traceback.md:138` — "빈 칸을 여는 비용과 늘리는 비용을 따로 두는 모델을 쓴다." 뒤에 "이 모델은 세 항의 상수만 바꿔서는 담기지 않고, 지금 열이 빈 칸의 연속인지를 함께 들고 가야 한다."를 더했다. affine gap 모델이 점화식 세 항의 상수 교체만으로 표현되는 것으로 잘못 읽힐 여지를 닫았다(Minor).
- `docs/superpowers/specs/2026-08-26-edit-distance-design.md`(「Provenance 분류」 표) — `abcab`/`abcba` 예시 행 뒤에 "영역 판정식 `D(i,j) + D'(i,j) = D(n,m)`"과 "최적 경로 수가 이항계수로 커지는 예" 두 행을 더해, 이 편이 실제로 반영한 두 확장이 표에 빠져 있던 것을 채웠다(record-keeping).
- `docs/superpowers/specs/2026-08-26-edit-distance-design.md`(「도판」 절, `region.svg` 행과 뒤이은 채움 규칙 문장) — "마름모 영역으로 채움"을 "칸을 파선으로 묶어 영역을 보인다"로 고치고 색 표기도 "영역 채움 `#1e3a5f`"에서 "영역은 `#93c5fd` 파선 테두리"로 고쳐, 실제로 배포된 도판(채움 없이 파선 테두리만 씀)과 스펙을 맞췄다(record-keeping).

재검증(위 반영 후): `python .claude/review_post.py src/content/posts/edit-distance.md src/content/posts/edit-distance-traceback.md` 두 파일 모두 발견 사항 없음, `npm run build` 141 page(s) built, `npm run test:js` 21/21 통과.
