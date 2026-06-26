# 리뷰 리포트: scheduling-1

schema_version: review-report/v2
target: scheduling-1
generated_at: not-recorded
strict: not-recorded
summary: 🔴 1 · 🟡 3 · 🟢 0
status: MIGRATED
migrated_from: legacy review report

## 결정적 검사

```text
## 결정적 검사: src/content/posts/scheduling-1.md

🟡 권장 (1)
- [D2] —  줄표(—) 19회 — 임계치(10) 초과. AI 문체 신호

요약: 🔴 0 · 🟡 1 · 🟢 0
```

## Findings

### 🔴 필수 [L2]

- severity: 🔴
- source: L
- rule_id: L2
- location: `src/content/posts/scheduling-1.md:91`, `src/content/posts/scheduling-1.md:96`
- quote: `S의 t가 비어 있다면 — S에 J_{i+1}을 그냥 추가하면 이익이 더 커진다`
- message: `S의 t가 비어 있다면 — S에 J_{i+1}을 그냥 추가하면 이익이 더 커진다`는 설명은 뒤의 `S가 J_{i+1}을 이미 다른 시간 t'에 가지고 있다면` 경우와 충돌할 수 있다. `S`가 이미 `J_{i+1}`을 더 이른 시간에 가진 상태라면, 시간 `t`가 비어 있어도 “추가”가 아니라 “이동”을 해야 한다.
- recommendation: 경우 분류를 먼저 `S가 J_{i+1}`을 이미 포함하는지 여부로 나눈 뒤, 포함하지 않을 때만 `t`가 비어 있으면 추가한다고 고치는 것이 안전하다.
- gate_effect: fail

### 🟡 권장 [D2]

- severity: 🟡
- source: D
- rule_id: D2
- location: not-recorded
- quote: not-recorded
- message: 줄표(—) 19회 — 임계치(10) 초과. AI 문체 신호
- recommendation: not-recorded
- gate_effect: warn

### 🟡 권장 [D2/L1]

- severity: 🟡
- source: L
- rule_id: D2/L1
- location: `src/content/posts/scheduling-1.md:2`, `src/content/posts/scheduling-1.md:16`, `src/content/posts/scheduling-1.md:18`, `src/content/posts/scheduling-1.md:68`, `src/content/posts/scheduling-1.md:91`, `src/content/posts/scheduling-1.md:92`, `src/content/posts/scheduling-1.md:107`, `src/content/posts/scheduling-1.md:109`, `src/content/posts/scheduling-1.md:121`
- quote: `핵심 아이디어는 이렇다 — *어떤 최적해가 있더라도...*`
- message: 줄표가 제목, 목록, 증명, 성능 설명에 반복된다. 특히 `핵심 아이디어는 이렇다 — *어떤 최적해가 있더라도...*`처럼 줄표와 기울임이 함께 쓰인 문장은 AI 문체 신호가 강하다.
- recommendation: 줄표는 마침표나 콜론으로 바꾸고, 기울임 강조는 평서문으로 낮추는 편이 좋다.
- gate_effect: warn

### 🟡 권장 [L2/L3]

- severity: 🟡
- source: L
- rule_id: L2/L3
- location: `src/content/posts/scheduling-1.md:112`
- quote: `트리는 D_i가 몇 번째로 큰 값인지 알려 주고`
- message: `트리는 D_i가 몇 번째로 큰 값인지 알려 주고`는 균형 이진 탐색 트리의 핵심 연산을 rank 질의처럼 설명한다. 이 문맥에서 필요한 것은 순위가 아니라 predecessor 질의, 즉 `$D_i$ 이하의 최댓값` 찾기다.
- recommendation: “트리에서 $D_i$ 이하의 가장 큰 빈 칸을 찾는다”처럼 직접 표현하면 더 명확하다.
- gate_effect: warn

LLM 비평 요약: 🔴 1 · 🟡 2 · 🟢 0
요약: 🔴 1 · 🟡 3 · 🟢 0
