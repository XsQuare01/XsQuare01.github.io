# 리뷰 리포트: tape-storage

- schema_version: review-report/v2
- target: tape-storage
- generated_at: 2026-06-17
- strict: false

## 결정적 검사: src/content/posts/tape-storage.md
발견 사항 없음 ✅

## LLM 비평: src/content/posts/tape-storage.md

### 🟢 [L6] 원본에 없는 수치 예시 추가 — `src/content/posts/tape-storage.md:71-78`
- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/tape-storage.md:71-78
- quote: "데이터 $A = (4, 1)$ 과 $B = (1, 4)$ 두 개만 놓자. … $B \to A$ 순서: $4 \cdot 1 + 1 \cdot (1 + 4) = 4 + 5 = 9$."
- message: Notion 원본("📼 Tape Storage")에는 없는 구체적 수치 예시(A·B, 비용 24 vs 9)와 intuition.svg를 추가했다. 사용자 요청("이해가 쉽도록 SVG를 많이")에 부합하고 계산도 정확하나, 원본 대비 추가분임을 기록으로 남긴다.
- recommendation: 추가 의도가 명확하므로 유지 권장. 원본 충실성만 기록.
- gate_effect: info

### 🟢 [L6] 원본 용어 오류 교정 (확률·기댓값 → 빈도 가중 총 접근 시간) — `src/content/posts/tape-storage.md:44-48`
- severity: 🟢
- source: L
- rule_id: L6
- location: src/content/posts/tape-storage.md:44-48
- quote: "모든 데이터에 대해 합하면 우리가 최소화하려는 **총 접근 시간** $P$ 가 된다."
- message: 원본은 $F_i$를 "사용 빈도"로 정의해 놓고 비용을 "접근 시간 기댓값"·"데이터 읽을 확률"로 혼용했다. $F_i$는 빈도(횟수)이므로 최소화 대상은 빈도 가중 총 접근 시간이다. 의미가 더 정확하도록 교정했다.
- recommendation: 교정 유지.
- gate_effect: info

### 🟢 [L7] 증명 경우 분류 완결성 — `src/content/posts/tape-storage.md:96-152`
- severity: 🟢
- source: L
- rule_id: L7
- location: src/content/posts/tape-storage.md:96-152
- quote: "모든 이웃 쌍이 내림차순이라면 전체가 이미 내림차순일 테니 가정에 어긋난다."
- message: $P-P' = F_{i+1}L_i - F_iL_{i+1} = L_iL_{i+1}(F_{i+1}/L_{i+1} - F_i/L_i)$ 계산을 직접 검산했고 정확하다. "내림차순이 아니면 인접 역순 쌍이 존재한다"는 대우 논증도 완결적(MECE)이다. 예시 24·9 계산도 일치.
- recommendation: 조치 불필요.
- gate_effect: info

### 🟢 [L1] 문체 검토 완료, 이슈 없음 — `src/content/posts/tape-storage.md`
- severity: 🟢
- source: L
- rule_id: L1
- location: src/content/posts/tape-storage.md
- quote: not-recorded
- message: 줄표(—)는 제목(시리즈 관례)·정의 리스트(`scheduling-1.md:30-31`과 동일 패턴)·SVG alt-text에만 쓰였고 본문 산문 남발은 없다. 경구식 마무리·과한 비유·대칭 반복 없음. ~다 평서체 일관.
- recommendation: 없음.
- gate_effect: info

### 🟢 [L2] 설명 흐름 검토 완료, 이슈 없음 — `src/content/posts/tape-storage.md`
- severity: 🟢
- source: L
- rule_id: L2
- location: src/content/posts/tape-storage.md
- quote: not-recorded
- message: 문제정의 → 비용모델 → 직관 → 증명 → 복잡도로 도약 없이 이어진다. 비용식 도입 후 "앞 데이터 길이가 반복 가산된다"는 관찰로 직관을 자연스럽게 연결.
- recommendation: 없음.
- gate_effect: info

### 🟢 [L3] 용어·어체 일관성 검토 완료, 이슈 없음 — `src/content/posts/tape-storage.md`
- severity: 🟢
- source: L
- rule_id: L3
- location: src/content/posts/tape-storage.md
- quote: not-recorded
- message: 데이터/길이/빈도/비율/접근 시간 용어가 일관되게 쓰인다. 기호 $L_i, F_i, F_i/L_i$ 표기 통일.
- recommendation: 없음.
- gate_effect: info

### 🟢 [L4] SVG ↔ 본문 일치 검토 완료, 이슈 없음 — `public/images/tape/*.svg`
- severity: 🟢
- source: L
- rule_id: L4
- location: src/content/posts/tape-storage.md:50,71,114,157
- quote: not-recorded
- message: tape-model(총 접근 시간 식·D₃ 비용=L₁+L₂+L₃), intuition(24 vs 9, F/L=4 vs 0.25), exchange(P−P′ 공식), sorted(F/L 내림차순·O(N log N)) 모두 본문 수치·주장과 일치.
- recommendation: 없음.
- gate_effect: info

### 🟢 [L5] 제목·description 적합성 검토 완료, 이슈 없음 — `src/content/posts/tape-storage.md:2-3`
- severity: 🟢
- source: L
- rule_id: L5
- location: src/content/posts/tape-storage.md:2-3
- quote: not-recorded
- message: 제목·description이 문제(접근 시간 최소화)·전략(F/L 내림차순)·증명(교환 논증)을 정확히 대표한다.
- recommendation: 없음.
- gate_effect: info

요약: 🔴 0 · 🟡 0 · 🟢 8
