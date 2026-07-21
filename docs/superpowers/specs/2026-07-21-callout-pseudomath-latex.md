# 콜아웃 평문 pseudo-math → LaTeX 전수 변환 (#61)

- 날짜: 2026-07-21
- 브랜치: `feat/callout-pseudomath-61`
- 전제: #60(PR) 머지됨 — 콜아웃 내부 `$…$`가 빌드 시 KaTeX로 렌더된다.
- 범위: 콜아웃(`<div class="callout…">…</div>`) **본문** 안의 평문 pseudo-math. 전수조사 결과 **35편, 137개 라인** 후보.

## 대상 포스트 (35)

algo-orientation, alice-bob, any-mst, before-physics, classes, closest-pair-bst, convex-hull-3, convex-hull-4, convex-hull-5, convex-hull-bst-tangent, convex-hull-calipers-edge, crt, data-structure, diffie-hellman, divide-and-conquer, division-theorem, dpda-npda, elgamal, fermat, find-prime, future-cryptography, gcd, hashing, kruskal, modular, np-alternative, np-complete, problem-and-solution, rsa, scheduling-1, scheduling-2, signature, toss-coin-over-telephone, turing-machine, zero-knowledge

## 원칙

- **콜아웃 본문 안에서만** 변환. 콜아웃 밖 본문은 이번 범위 아님.
- **진짜 수식만** `$…$`로 감싼다. 산문 화살표("그래서 → "), 목록 불릿, 순수 텍스트 라벨(제목의 한글)은 건드리지 않는다.
- 산문 속에 박힌 수식은 **그 조각만** 감싼다. 예: `gcd(12, 8) = 4이면` → `$\gcd(12, 8) = 4$이면`.
- 인라인은 `$…$`, 독립 수식 줄은 `$$…$$`.
- **의미 보존**: 연산자는 원문 그대로 옮긴다(`≡`는 항상 `\equiv`). 애매하면 원문 유지.
- 코드(`<code>`/`<pre>`), 난이도 별표(★☆☆)는 변환 금지.
- `<strong>`, `<li>`, `<p>` 등 콜아웃 내부 HTML 구조는 유지하고, 그 안의 텍스트만 감싼다.

## 매핑 규칙

| 원문 | LaTeX | 비고 |
|---|---|---|
| `≡` | `\equiv` | 합동 |
| `≠` | `\neq` | |
| `≤` `≥` | `\le` `\ge` | |
| `≈` | `\approx` | |
| `×` | `\times` | |
| `·` (곱) | `\cdot` | 불릿이면 변환 금지 |
| `÷` | `\div` | |
| `⊕` `⊗` | `\oplus` `\otimes` | |
| `∩` `∪` | `\cap` `\cup` | |
| `∈` `∉` | `\in` `\notin` | |
| `⊆` `⊂` | `\subseteq` `\subset` | |
| `→` (사상/귀착/변환) | `\to` | 산문 화살표면 그대로 |
| `↔` `⟺` | `\iff` | |
| `∀` `∃` | `\forall` `\exists` | |
| `∘` | `\circ` | |
| `√x` | `\sqrt{x}` | |
| `Σ` `Π` | `\sum` `\prod` | |
| `|` (나눔) | `\mid` | `d \mid a` |
| 그리스 `φ π θ λ μ σ α β γ δ` | `\varphi \pi \theta \lambda \mu \sigma \alpha \beta \gamma \delta` | |
| `Θ` `Ω` | `\Theta` `\Omega` | |
| 아래첨자 `m₁ mᵢ mᵣ` | `m_1 m_i m_r` | |
| 위첨자 `n² n³ ⁻¹` | `n^2 n^3 ^{-1}` | `Mᵢ⁻¹` → `M_i^{-1}` |
| `≤ₚ` | `\le_p` | 다항 귀착 |
| 캐럿 `m^e` `m^(ed)` | `m^e` `m^{ed}` | 2자 이상은 중괄호 |
| `(mod n)` | `\pmod{n}` | |
| `a mod n` (연산) | `a \bmod n` | |
| 함수 `gcd log max min` | `\gcd \log \max \min` | |
| `lcm` | `\operatorname{lcm}` | |
| 복잡도 클래스 `NP Co-NP P NP-Hard NP-Complete PSPACE EXP SAT` | `\text{NP}` 등 | 수식 안에서 텍스트로 |
| 위첨자 `Lᶜ` | `L^c` | 여집합 |

## 예시

- `ed ≡ 1 (mod φ(n))` → `$ed \equiv 1 \pmod{\varphi(n)}$`
- `C = m^e mod n → m = C^d mod n = m^(ed) mod n` → `$C = m^e \bmod n$ → $m = C^d \bmod n = m^{ed} \bmod n$` (사이 `→`는 산문이면 그대로)
- `A ≤ₚ B이면 B가 A만큼 어렵다` → `$A \le_p B$이면 B가 A만큼 어렵다`
- `L ∈ Co-NP ⟺ Lᶜ ∈ NP` → `$L \in \text{Co-NP} \iff L^c \in \text{NP}$`
- `d | a, d | b이고, c | a` → `$d \mid a$, $d \mid b$이고, $c \mid a$`
- `NP ∩ NP-Hard` → `$\text{NP} \cap \text{NP-Hard}$`

## 검증

정적 사이트(유닛 테스트 없음).

- 캐시 정리(`node_modules/.astro`, `.astro`) 후 `npm run build` 성공.
- 전체 산출물 **KaTeX 에러 0건**(`katex-error` 미출현).
- 콜아웃 본문에 **미처리 pseudo-math 잔존 최소화**(잔존 스캔).
- 대표 편(rsa, np-complete, gcd) 육안으로 의미·조판 확인.

## 실행 방식

포스트가 서로 독립 파일이므로 병렬 서브에이전트(capable model)로 청크 분담해 변환(파일 편집만, 커밋·빌드 없음)하고, 마지막에 전역 빌드+검증 후 한 번에 커밋한다.
