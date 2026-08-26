schema_version: review-report/v2
target: edit-distance
generated_at: 2026-08-26
strict: true
sources: src/content/posts/edit-distance.md
summary: 🔴 0 · 🟡 4 · 🟢 8

## Findings

### 🟡 [L4] public/images/edit-distance/recurrence.svg:13

- severity: 🟡
- source: L
- rule_id: L4
- location: public/images/edit-distance/recurrence.svg:13
- quote: 한 칸은 세 이웃만 보고, 다시 세 칸에 쓰인다
- message: 도판 제목이 재사용 횟수를 조건 없이 세 번으로 못 박는데, 본문은 같은 주장을 표 내부 칸으로 한정한다(src/content/posts/edit-distance.md:180 "표 내부의 칸 D(i, j) 는 … 마지막 행과 열의 칸은 이보다 적게 쓰이고 D(n, m) 은 쓰이지 않는다"). 이 한정이 설계 스펙의 정정 3이므로 도판만 정정 전 문장을 되살려 놓은 상태다. 도판은 점화식 절(133행)에 먼저 나오므로 독자는 조건을 만나기 전에 무조건적 서술을 읽는다.
- recommendation: 제목이나 부제에 '내부 칸'이라는 조건을 넣는다. 예: 부제를 "실선은 이 칸을 계산하는 경로, 점선은 이 칸이 쓰이는 곳. 내부 칸이면 세 곳이다"로 고친다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/edit-distance.md:98

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance.md:98
- quote: 정렬의 비용은 열 비용의 합이고, 편집 거리는 비용이 가장 작은 정렬의 비용이다.
- message: 56행은 편집 거리를 '연산의 최소 횟수'로 정의했고 98행은 같은 값을 '최소 비용 정렬의 비용'으로 다시 적는다. 두 정의가 같다는 것은 자명하지 않다. 연산의 열을 같은 비용의 정렬로 바꿀 수 있고 그 역도 가능하다는 양방향 논증이 필요하다. 정리 1의 증명은 "편집 거리는 가능한 정렬 중 최소 비용이므로"(119행)와 최적 정렬 A 를 잡는 대목(121행)에서 이 등가성을 두 방향 모두의 전제로 쓰므로, 증명 전체가 논증되지 않은 한 줄에 얹혀 있다. 주장 자체는 참이며 검증에서 반례를 찾지 못했다.
- recommendation: 등가성을 한두 문장으로 닫거나(연산 열에서 같은 비용의 정렬을 만들고 그 역도 만든다), 98행을 '이 글에서는 편집 거리를 이렇게 다시 적는다'는 재정의로 명시하고 앞의 정의와 같은 값임을 짚는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/edit-distance.md:186

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance.md:186
- quote: 어떤 상수 $
- message: 176행이 $N$, $M$ 을 두 문자열의 길이 $n$, $m$ 이라고 못 박은 뒤 하한만 단일 기호 $n$ 으로 적는다. Backurs–Indyk의 결과는 길이가 각각 $n$ 인 두 문자열에 대한 진술이므로, $n
- recommendation: "길이가 각각 $n$ 인 두 문자열에 대해"처럼 적용 범위를 밝히거나 $N = M = n$ 인 경우로 한정해 적는다.
- gate_effect: warn

### 🟡 [L7] src/content/posts/edit-distance.md:257

- severity: 🟡
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance.md:257
- quote: 표는 칸마다 세 이웃만 보고 한 번씩 채우므로 $O(NM)$ 이며, 이보다 빠른 일반 알고리즘이 없다는 결론은 SETH 가정에 기대고 있다.
- message: 본문 186행은 SETH가 배제하는 대상을 강한 준이차 시간, 곧 $O(n^{2-
- recommendation: "강한 준이차 시간($O(n^{2-
- gate_effect: warn

### 🟢 [L1] src/content/posts/edit-distance.md:274

- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/edit-distance.md:274
- quote: 무엇을 연산 목록에 넣느냐가 무엇을 '비슷하다'고 볼지 정한다.
- message: 30행 "거리 함수를 어떻게 정하느냐가 무엇을 '비슷하다'고 볼지 정한다"와 문형이 그대로 겹친다. 루브릭 L1이 신호로 꼽는 대칭 문장 반복이지만 주어가 거리 함수에서 연산 목록으로 좁혀지며 내용이 한 걸음 나아가므로 의도된 여닫기로 읽힌다. 문두 접속어는 0회, 줄표는 제목과 링크 제목에만 있고, 굵게는 용어 도입과 callout 항목에만 쓰여 남발이 없다.
- recommendation: 반복이 의도가 아니라면 마지막 문장의 문형만 바꾼다. 유지해도 무리는 없다.
- gate_effect: info

### 🟢 [L2] src/content/posts/edit-distance.md:180

- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/edit-distance.md:180
- quote: 표는 그 칸을 한 번만 계산해 세 번 나눠 쓴다.
- message: 재귀의 지수 폭발과 표의 재사용이라는 기법의 실질은 다 적혀 있는데 기법의 이름(동적 계획법)은 두 편 어디에도 나오지 않는다. frontmatter는 Dynamic Programming 태그를 달고 있어 태그와 본문 어휘가 맞물리지 않고, 스펙이 옮긴 원문 줄기 6의 마무리인 "그래서 DP다"에 해당하는 한 줄이 비어 있다. 논증에는 빈틈이 없어 참고 사항으로 남긴다.
- recommendation: 이 문단이나 마치며에 기법의 이름을 한 번 붙인다. 시리즈 번호를 붙이지 않는다는 스펙 2.1의 결정과는 무관하다.
- gate_effect: info

### 🟢 [L3] src/content/posts/edit-distance.md:1

- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/edit-distance.md:1
- quote: not-recorded
- message: 검토 완료, 이슈 없음 — 넣기·지우기·바꾸기·맞추기, 정렬, 접두사, 격자·칸·경로, 그리고 $S_1$·$S_2$·$n$·$m$·$D(i, j)$·$t(i, j)$ 의 쓰임이 본문·수식·코드·도판에서 한 뜻으로 유지된다. $N$·$M$ 과 $n$·$m$ 이 같은 값을 가리킨다는 점을 176행에서 한 번 밝히고 그 뒤로 섞이지 않는다. 어체는 ~다 평서체로 일관된다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L4] src/content/posts/edit-distance.md:42

- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/edit-distance.md:42
- quote: not-recorded
- message: 검토 완료, 이슈 없음 — align-shift.svg는 어긋난 세 자리와 빈 칸 하나가 40·44행 서술과 맞다. subproblem.svg의 표시 칸 셋은 격자 좌표로 (2,4)·(5,1)·(7,7)이고 라벨 값 2·4·2가 맞다. table.svg의 64개 값을 전부 다시 계산해 스펙 3절 표와 한 칸도 다르지 않음을 확인했고, 답 칸 2와 161·162행의 v/wr 손계산(대각 1·위 3·왼쪽 2, 최솟값 2)도 일치한다. recurrence.svg의 화살표 방향과 비용 라벨은 정리 1의 세 항과 맞는다. 두 코드 블록은 본문의 순회 순서·기저·대칭 조건과 어긋나지 않으며, 두 행 판은 $m = 0$ 과 $n = 0$ 경계에서도 옳은 값을 낸다. 도판 제목 문구 하나는 별도 finding으로 올렸다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L5] src/content/posts/edit-distance.md:2

- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/edit-distance.md:2
- quote: 편집 거리 — 비슷하다는 말을 수로 바꾸기
- message: 검토 완료, 이슈 없음 — 제목이 '비슷함을 수로 바꾸는 일'이라는 글의 질문을 그대로 가리킨다. description 두 문장이 Hamming 거리의 한계, 빈 칸을 허용한 정의와 표, $O(NM)$ 하한의 정확한 뜻이라는 세 축을 실제 절 순서대로 담는다. 하한을 단정하지 않고 "말의 정확한 뜻까지 짚는다"로 적어 본문의 조건부 서술과 어긋나지 않는다.
- recommendation: not-recorded
- gate_effect: info

### 🟢 [L6] src/content/posts/edit-distance.md:1

- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/edit-distance.md:1
- quote: not-recorded
- message: approved extension — 노션 원문에 직접 접근할 도구가 없어 승인된 설계 스펙 docs/superpowers/specs/2026-08-26-edit-distance-design.md를 대조 자료로 삼았다. 스펙이 옮긴 원문 줄기 1~7이 모두 살아 있다(응용 셋, 거리 함수 셋과 move·copy 한계, 정의, $D(i, j)$ 와 지목한 두 칸, 점화식, 재귀 대비 재사용, tabular computation). 원문 요청 1·2·3이 각각 정리 1과 증명, 연산 열 절, 하한 절에서 닫히고 요청 4는 짝 편이 받는다. 정정 1~5가 모두 반영되어 있다(길이가 다른 쌍을 Hamming 거리라 부르지 않음, SETH 조건부 하한, 내부 칸 조건, $3^{n+m}$, $D(2,4)=2$·$D(5,1)=4$ 와 답 2). 원문 밖 내용은 정리 1의 증명, 조건부 하한과 참고 문헌, 두 행 공간이며 스펙 provenance 표에 확장으로 등재된 항목과 일치하고 원문의 구조·논증·의도를 훼손하지 않는다. 다만 원문의 "값이 NM개"를 "칸은 $(n+1)(m+1)$ 개"로 정확히 고친 것은 스펙의 정정 목록 다섯 항목에 없다. 결론인 $O(NM)$ 이 같고 구조와 주장을 바꾸지 않아 국소 불일치로 올리지 않았다.
- recommendation: 스펙의 「원문의 오류·부정확」 절에 칸 수 정확화를 한 줄 더해 정정 목록과 본문을 맞춘다. 본문 수정은 필요하지 않다.
- gate_effect: info

### 🟢 [L7] src/content/posts/edit-distance.md:180

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance.md:180
- quote: 호출 하나가 갈래 셋으로 벌어지고 깊이는 최대 $n + m$ 이므로 호출 수가 $3^{n+m}$ 까지 간다.
- message: 깊이 $n+m$ 인 삼분 트리의 노드 수는 $(3^{n+m+1}-1)/2$ 이므로 $3^{n+m}$ 은 호출 수의 상한이 아니라 규모다. 결론인 지수 폭발은 그대로 성립하고 스펙 정정 4가 적은 상한과 같은 뜻이라 참고 사항으로 남긴다. 깊이가 $n+m$ 이하라는 부분은 참조마다 $i+j$ 가 1 이상 줄어드는 것으로 닫힌다.
- recommendation: 엄밀히 적으려면 $O(3^{n+m})$ 이나 "$3^{n+m}$ 규모"로 쓴다. 필수 수정은 아니다.
- gate_effect: info

### 🟢 [L7] src/content/posts/edit-distance.md:186

- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/edit-distance.md:186
- quote: 무조건적인 하한은 알려져 있지 않다.
- message: 문맥이 $O(NM)$ 을 겨눈 하한이라는 점은 앞 문장이 정해 주지만, 문장만 떼어 놓으면 입력을 읽는 비용에서 나오는 $\Omega(N+M)$ 같은 자명한 하한까지 없다는 말로 읽힌다. 절 전체는 조건부 하한과 조건을 좁힌 더 빠른 방법을 함께 적어 '무조건 불가'로 읽히지 않으므로 참고 사항이다.
- recommendation: "무조건적인 이차 하한" 또는 "$O(NM)$ 에 맞는 무조건적 하한"으로 범위를 붙인다.
- gate_effect: info

## 후속 처리

- 🟡 [L4] `public/images/edit-distance/recurrence.svg:13` — **반영 완료**. 도판 제목 "한 칸은 세 이웃만 보고, 다시 세 칸에 쓰인다"를 "한 칸은 세 이웃만 보고, 표 안쪽에서는 다시 세 칸에 쓰인다"로 고쳐, 세 번 재사용이 표 안쪽 칸에 한정된다는 조건을 본문(180행)을 만나기 전에도 제목에서부터 밝혔다.
- 🟡 [L7] `src/content/posts/edit-distance.md:98` — **반영 완료**. "정렬의 비용은 열 비용의 합이고, 편집 거리는 비용이 가장 작은 정렬의 비용이다."를 양방향 논증으로 바꿨다. 연산의 열을 정렬로 옮기는 방향과 정렬을 연산의 열로 되짚는 방향을 각각 짚어, 최소 연산 수와 최소 정렬 비용이 같다는 결론을 정리 1의 증명이 기대는 전제로 명시했다.
- 🟡 [L7] `src/content/posts/edit-distance.md:186` — **반영 완료**. "Backurs와 Indyk는 SETH가 참이라면…"에 "길이가 모두 $n$ 인 두 문자열에 대해"를 앞세워, 176행에서 고정한 $N$, $M$ 표기와 하한 진술의 단일 기호 $n$ 이 같은 길이 조건($N = M = n$)을 가리킴을 밝혔다.
- 🟡 [L7] `src/content/posts/edit-distance.md:257` — **반영 완료**. 핵심 정리 콜아웃의 "이보다 빠른 일반 알고리즘이 없다는 결론은…"을 "강한 준이차 시간의 일반 알고리즘이 없다는 결론은…"으로 고쳐, 186행이 이미 밝힌 SETH의 배제 범위($O(n^{2-\varepsilon})$, 강한 준이차 시간)와 표현을 맞추고 Masek–Paterson처럼 더 빠른 준이차 알고리즘의 존재와 모순되지 않게 했다.

판정을 바꾸는 수정은 없다. 점화식, 정리 1의 진술, 손계산 예시, 의사코드, $O(NM)$ 판정은 그대로다.

재검증: `python .claude/review_post.py src/content/posts/edit-distance.md src/content/posts/edit-distance-traceback.md` 두 파일 모두 발견 사항 없음, `npm run build` 141 page(s) built, `npm run test:js` 21/21 통과, `public/images/edit-distance/recurrence.svg` minidom 파싱 통과 및 팔레트 색만 사용 확인.
