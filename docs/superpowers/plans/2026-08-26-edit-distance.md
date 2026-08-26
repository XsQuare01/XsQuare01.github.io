# 편집 거리 두 편 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 편집 거리 본편과 되짚기 추가 설명 두 편을 SVG 7장과 함께 발행 가능한 상태로 만든다.

**Architecture:** 본편은 거리 함수의 실패 사슬에서 시작해 편집 거리의 점화식을 정리·증명으로 닫고 표를 채워 값을 구하는 데까지 간다. 추가 설명은 그 표를 거꾸로 읽어 연산을 복원하고, 최적 경로가 여럿일 때 결과가 왜 영역이 되는지를 세 정렬로 보인다. 도판은 저장소의 18색 팔레트만 쓰는 정적 SVG다.

**Tech Stack:** Astro content collection(마크다운 + KaTeX), 손으로 쓴 SVG, `npm run build`, `npm test`, `.claude/review_post.py`

**Spec:** `docs/superpowers/specs/2026-08-26-edit-distance-design.md`

## Global Constraints

- 브랜치는 `feat/post-edit-distance`. main에 직접 커밋하지 않는다.
- 커밋 메시지에 `Co-Authored-By` 트레일러를 넣지 않는다.
- 예상 독자: 자료구조·재귀를 알고 DP를 한 번은 만난 학부생. 기존 시리즈(`dp-1`~`dp-3`, `maximum-subarray`)와 같은 눈높이.
- 본문에 비공개 원천(강의 노트·노션)을 가리키는 서술을 넣지 않는다. 논문·URL 같은 공개 문헌은 밝힌다.
- 문두 접속어를 최소화한다. 문장 내부 줄표(`—`)는 결정적 검사의 임계치에 걸리므로 남발하지 않는다(섹션 제목·이미지 alt의 구조적 줄표는 허용).
- 인라인 수식 뒤 한국어 조사는 한 칸 띄운다: `$D(i,j)$ 는`.
- 코드는 C++ 의사코드. 컴파일 검증하지 않는다.
- SVG는 `docs/design/DIAGRAM_PALETTE.md`의 18색만 쓴다. hex는 소문자 6자리. 반투명은 `fill-opacity`. 채움색 위에 글자를 얹지 않는다. `id`는 파일별 접두어(`ed-`, `edt-`)를 붙인다.
- 본문 인덱스는 1부터, 코드 인덱스는 0부터. 두 관례가 만나는 자리에 `s1[i-1]` 형태로 명시한다.
- 날짜는 실제 작성일 2026-08-26. 본편 `T09:00:00`, 추가 설명 `T10:00:00`.

## File Structure

| 파일 | 책임 |
|---|---|
| `public/images/edit-distance/align-shift.svg` | 자리끼리 맞춘 비교와 빈 칸을 허용한 비교의 대조 |
| `public/images/edit-distance/subproblem.svg` | 표의 한 칸이 접두사 두 개의 거리라는 것 |
| `public/images/edit-distance/recurrence.svg` | 한 칸이 보는 세 이웃과, 그 칸이 쓰이는 세 곳 |
| `public/images/edit-distance/table.svg` | `abcabcd`×`abcdabc` 완성 표와 답 |
| `src/content/posts/edit-distance.md` | 본편 |
| `public/images/edit-distance-traceback/traceback-path.svg` | 되짚기 한 경로 |
| `public/images/edit-distance-traceback/region.svg` | 세 최적 경로와 그 합집합인 영역 |
| `public/images/edit-distance-traceback/alignments.svg` | 같은 비용의 정렬 세 개 |
| `src/content/posts/edit-distance-traceback.md` | 추가 설명 |
| `docs/reviews/2026-08-26-edit-distance.md` | 리뷰 리포트(6번 과제에서 생성) |

---

### Task 1: 본편 도판 4장

**Files:**
- Create: `public/images/edit-distance/align-shift.svg`
- Create: `public/images/edit-distance/subproblem.svg`
- Create: `public/images/edit-distance/recurrence.svg`
- Create: `public/images/edit-distance/table.svg`
- Test: `npm test` (팔레트 회귀), `grep`으로 팔레트 밖 hex 확인

**Interfaces:**
- Consumes: 없음 (첫 과제)
- Produces: 위 네 경로. 본편 본문이 `/images/edit-distance/<파일>` 로 참조한다.

- [ ] **Step 1: `align-shift.svg` 를 만든다**

```svg
<svg viewBox="0 0 680 360" width="1020" height="540" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="360" rx="10" fill="#0f1117"/>

  <text x="340" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">한 글자가 빠지면 그 뒤가 전부 밀린다</text>
  <text x="340" y="53" text-anchor="middle" fill="#64748b" font-size="11">위는 자리끼리만 맞춘 비교, 아래는 빈 칸을 허용한 비교</text>

  <!-- ===== 위: 자리끼리 맞춤 ===== -->
  <text x="178" y="105" text-anchor="end" fill="#94a3b8" font-size="12">S₁</text>
  <text x="178" y="147" text-anchor="end" fill="#94a3b8" font-size="12">S₂</text>

  <rect x="190" y="82" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="254" y="82" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="318" y="82" width="52" height="34" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="382" y="82" width="52" height="34" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="446" y="82" width="52" height="34" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>

  <g font-size="15" text-anchor="middle">
    <text x="216" y="105" fill="#cbd5e1">a</text>
    <text x="280" y="105" fill="#cbd5e1">b</text>
    <text x="344" y="105" fill="#f87171">a</text>
    <text x="408" y="105" fill="#f87171">b</text>
    <text x="472" y="105" fill="#f87171">c</text>
  </g>

  <rect x="190" y="124" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="254" y="124" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="318" y="124" width="52" height="34" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="382" y="124" width="52" height="34" rx="4" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="446" y="124" width="52" height="34" rx="4" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="4 3"/>

  <g font-size="15" text-anchor="middle">
    <text x="216" y="147" fill="#cbd5e1">a</text>
    <text x="280" y="147" fill="#cbd5e1">b</text>
    <text x="344" y="147" fill="#f87171">b</text>
    <text x="408" y="147" fill="#f87171">c</text>
  </g>
  <text x="472" y="146" text-anchor="middle" fill="#64748b" font-size="10">상대 없음</text>

  <text x="340" y="182" text-anchor="middle" fill="#f87171" font-size="12">어긋난 자리 세 곳 — 세 번 고쳐야 하는 것처럼 보인다</text>

  <line x1="60" y1="200" x2="620" y2="200" stroke="#1e293b" stroke-width="1"/>

  <!-- ===== 아래: 빈 칸 허용 ===== -->
  <text x="178" y="245" text-anchor="end" fill="#94a3b8" font-size="12">S₁</text>
  <text x="178" y="287" text-anchor="end" fill="#94a3b8" font-size="12">S₂</text>

  <rect x="190" y="222" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="254" y="222" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="318" y="222" width="52" height="34" rx="4" fill="#1e293b" stroke="#4ade80" stroke-width="1.8"/>
  <rect x="382" y="222" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="446" y="222" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>

  <g font-size="15" text-anchor="middle" fill="#cbd5e1">
    <text x="216" y="245">a</text>
    <text x="280" y="245">b</text>
    <text x="344" y="245" fill="#4ade80">a</text>
    <text x="408" y="245">b</text>
    <text x="472" y="245">c</text>
  </g>

  <rect x="190" y="264" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="254" y="264" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="318" y="264" width="52" height="34" rx="4" fill="none" stroke="#4ade80" stroke-width="1.8" stroke-dasharray="4 3"/>
  <rect x="382" y="264" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>
  <rect x="446" y="264" width="52" height="34" rx="4" fill="#1e293b" stroke="#475569" stroke-width="1"/>

  <g font-size="15" text-anchor="middle" fill="#cbd5e1">
    <text x="216" y="287">a</text>
    <text x="280" y="287">b</text>
    <text x="344" y="287" fill="#4ade80">–</text>
    <text x="408" y="287">b</text>
    <text x="472" y="287">c</text>
  </g>

  <text x="340" y="322" text-anchor="middle" fill="#4ade80" font-size="12">빈 칸 한 개 = 글자 하나를 지우는 연산 한 번</text>
  <text x="340" y="344" text-anchor="middle" fill="#64748b" font-size="10.5">S₁ = ababc · S₂ = abbc</text>
</svg>
```

- [ ] **Step 2: `subproblem.svg` 를 만든다**

```svg
<svg viewBox="0 0 680 400" width="1020" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="400" rx="10" fill="#0f1117"/>

  <text x="340" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">표의 한 칸은 접두사 두 개의 거리다</text>
  <text x="340" y="53" text-anchor="middle" fill="#64748b" font-size="11">행은 S₁의 앞부분, 열은 S₂의 앞부분. 0번째 줄은 빈 문자열이다</text>

  <!-- 열 머리 -->
  <g font-size="12" text-anchor="middle" fill="#94a3b8">
    <text x="110" y="110">–</text>
    <text x="150" y="110">a</text>
    <text x="190" y="110">b</text>
    <text x="230" y="110">c</text>
    <text x="270" y="110">d</text>
    <text x="310" y="110">a</text>
    <text x="350" y="110">b</text>
    <text x="390" y="110">c</text>
  </g>

  <!-- 행 머리 -->
  <g font-size="12" text-anchor="end" fill="#94a3b8">
    <text x="80" y="141">–</text>
    <text x="80" y="171">a</text>
    <text x="80" y="201">b</text>
    <text x="80" y="231">c</text>
    <text x="80" y="261">a</text>
    <text x="80" y="291">b</text>
    <text x="80" y="321">c</text>
    <text x="80" y="351">d</text>
  </g>

  <!-- 격자 -->
  <g stroke="#475569" stroke-width="0.8">
    <line x1="90" y1="118" x2="410" y2="118"/>
    <line x1="90" y1="148" x2="410" y2="148"/>
    <line x1="90" y1="178" x2="410" y2="178"/>
    <line x1="90" y1="208" x2="410" y2="208"/>
    <line x1="90" y1="238" x2="410" y2="238"/>
    <line x1="90" y1="268" x2="410" y2="268"/>
    <line x1="90" y1="298" x2="410" y2="298"/>
    <line x1="90" y1="328" x2="410" y2="328"/>
    <line x1="90" y1="358" x2="410" y2="358"/>
    <line x1="90" y1="118" x2="90" y2="358"/>
    <line x1="130" y1="118" x2="130" y2="358"/>
    <line x1="170" y1="118" x2="170" y2="358"/>
    <line x1="210" y1="118" x2="210" y2="358"/>
    <line x1="250" y1="118" x2="250" y2="358"/>
    <line x1="290" y1="118" x2="290" y2="358"/>
    <line x1="330" y1="118" x2="330" y2="358"/>
    <line x1="370" y1="118" x2="370" y2="358"/>
    <line x1="410" y1="118" x2="410" y2="358"/>
  </g>

  <!-- 지목한 칸 (테두리만) -->
  <rect x="250" y="178" width="40" height="30" fill="none" stroke="#93c5fd" stroke-width="2"/>
  <rect x="130" y="268" width="40" height="30" fill="none" stroke="#a78bfa" stroke-width="2"/>
  <rect x="370" y="328" width="40" height="30" fill="none" stroke="#4ade80" stroke-width="2"/>

  <!-- 설명 패널 -->
  <rect x="450" y="160" width="12" height="12" fill="#93c5fd"/>
  <text x="472" y="171" fill="#e2e8f0" font-size="13">D(2, 4) = 2</text>
  <text x="472" y="189" fill="#94a3b8" font-size="10.5">ab 와 abcd 의 편집 거리</text>

  <rect x="450" y="230" width="12" height="12" fill="#a78bfa"/>
  <text x="472" y="241" fill="#e2e8f0" font-size="13">D(5, 1) = 4</text>
  <text x="472" y="259" fill="#94a3b8" font-size="10.5">abcab 와 a 의 편집 거리</text>

  <rect x="450" y="300" width="12" height="12" fill="#4ade80"/>
  <text x="472" y="311" fill="#e2e8f0" font-size="13">D(7, 7) = 2</text>
  <text x="472" y="329" fill="#94a3b8" font-size="10.5">두 문자열 전체의 거리, 곧 답</text>

  <text x="340" y="384" text-anchor="middle" fill="#64748b" font-size="10.5">S₁ = abcabcd (행) · S₂ = abcdabc (열)</text>
</svg>
```

- [ ] **Step 3: `recurrence.svg` 를 만든다**

```svg
<svg viewBox="0 0 700 420" width="1050" height="630" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="ed-arrow-in" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#3b82f6"/>
    </marker>
    <marker id="ed-arrow-out" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#64748b"/>
    </marker>
  </defs>

  <rect width="700" height="420" rx="10" fill="#0f1117"/>

  <text x="350" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">한 칸은 세 이웃만 보고, 다시 세 칸에 쓰인다</text>
  <text x="350" y="53" text-anchor="middle" fill="#64748b" font-size="11">실선은 이 칸을 계산하는 경로, 점선은 이 칸이 쓰이는 곳</text>

  <!-- 이웃 세 칸과 대상 칸 -->
  <rect x="170" y="110" width="120" height="54" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
  <text x="230" y="142" text-anchor="middle" fill="#cbd5e1" font-size="13">D(i−1, j−1)</text>

  <rect x="350" y="110" width="120" height="54" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
  <text x="410" y="142" text-anchor="middle" fill="#cbd5e1" font-size="13">D(i−1, j)</text>

  <rect x="170" y="220" width="120" height="54" rx="4" fill="#1e293b" stroke="#64748b" stroke-width="1.2"/>
  <text x="230" y="252" text-anchor="middle" fill="#cbd5e1" font-size="13">D(i, j−1)</text>

  <rect x="350" y="220" width="120" height="54" rx="4" fill="#1e293b" stroke="#fbbf24" stroke-width="2"/>
  <text x="410" y="252" text-anchor="middle" fill="#fbbf24" font-size="14" font-weight="700">D(i, j)</text>

  <!-- 재사용될 세 칸 -->
  <rect x="530" y="220" width="120" height="54" rx="4" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="590" y="252" text-anchor="middle" fill="#64748b" font-size="12">D(i, j+1)</text>

  <rect x="350" y="320" width="120" height="54" rx="4" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="410" y="352" text-anchor="middle" fill="#64748b" font-size="12">D(i+1, j)</text>

  <rect x="530" y="320" width="120" height="54" rx="4" fill="none" stroke="#475569" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="590" y="352" text-anchor="middle" fill="#64748b" font-size="12">D(i+1, j+1)</text>

  <!-- 들어오는 화살표 -->
  <path d="M 287,161 L 347,217" fill="none" stroke="#3b82f6" stroke-width="1.6" marker-end="url(#ed-arrow-in)"/>
  <text x="286" y="198" text-anchor="end" fill="#93c5fd" font-size="11">+ t(i, j)</text>

  <path d="M 410,164 L 410,216" fill="none" stroke="#3b82f6" stroke-width="1.6" marker-end="url(#ed-arrow-in)"/>
  <text x="422" y="196" fill="#93c5fd" font-size="11">+1 · S₁[i] 지우기</text>

  <path d="M 290,247 L 346,247" fill="none" stroke="#3b82f6" stroke-width="1.6" marker-end="url(#ed-arrow-in)"/>
  <text x="230" y="296" text-anchor="middle" fill="#93c5fd" font-size="11">+1 · S₂[j] 넣기</text>

  <!-- 나가는 화살표 -->
  <path d="M 470,247 L 526,247" fill="none" stroke="#64748b" stroke-width="1.4" stroke-dasharray="5 3" marker-end="url(#ed-arrow-out)"/>
  <path d="M 410,274 L 410,316" fill="none" stroke="#64748b" stroke-width="1.4" stroke-dasharray="5 3" marker-end="url(#ed-arrow-out)"/>
  <path d="M 467,271 L 527,317" fill="none" stroke="#64748b" stroke-width="1.4" stroke-dasharray="5 3" marker-end="url(#ed-arrow-out)"/>

  <text x="350" y="398" text-anchor="middle" fill="#94a3b8" font-size="11">t(i, j) 는 S₁[i] 와 S₂[j] 가 같으면 0, 다르면 1</text>
</svg>
```

- [ ] **Step 4: `table.svg` 를 만든다**

```svg
<svg viewBox="0 0 700 450" width="1050" height="675" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="700" height="450" rx="10" fill="#0f1117"/>

  <text x="350" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">표를 채우면 마지막 칸에 답이 남는다</text>
  <text x="350" y="53" text-anchor="middle" fill="#64748b" font-size="11">왼쪽·위·왼쪽 위 대각선만 보고 칸마다 한 번씩 채운다</text>

  <!-- 열 머리 -->
  <g font-size="12" text-anchor="middle" fill="#94a3b8">
    <text x="176" y="105">–</text>
    <text x="228" y="105">a</text>
    <text x="280" y="105">b</text>
    <text x="332" y="105">c</text>
    <text x="384" y="105">d</text>
    <text x="436" y="105">a</text>
    <text x="488" y="105">b</text>
    <text x="540" y="105">c</text>
  </g>

  <!-- 행 머리 -->
  <g font-size="12" text-anchor="end" fill="#94a3b8">
    <text x="138" y="143">–</text>
    <text x="138" y="177">a</text>
    <text x="138" y="211">b</text>
    <text x="138" y="245">c</text>
    <text x="138" y="279">a</text>
    <text x="138" y="313">b</text>
    <text x="138" y="347">c</text>
    <text x="138" y="381">d</text>
  </g>

  <!-- 격자 -->
  <g stroke="#475569" stroke-width="0.8">
    <line x1="150" y1="118" x2="566" y2="118"/>
    <line x1="150" y1="152" x2="566" y2="152"/>
    <line x1="150" y1="186" x2="566" y2="186"/>
    <line x1="150" y1="220" x2="566" y2="220"/>
    <line x1="150" y1="254" x2="566" y2="254"/>
    <line x1="150" y1="288" x2="566" y2="288"/>
    <line x1="150" y1="322" x2="566" y2="322"/>
    <line x1="150" y1="356" x2="566" y2="356"/>
    <line x1="150" y1="390" x2="566" y2="390"/>
    <line x1="150" y1="118" x2="150" y2="390"/>
    <line x1="202" y1="118" x2="202" y2="390"/>
    <line x1="254" y1="118" x2="254" y2="390"/>
    <line x1="306" y1="118" x2="306" y2="390"/>
    <line x1="358" y1="118" x2="358" y2="390"/>
    <line x1="410" y1="118" x2="410" y2="390"/>
    <line x1="462" y1="118" x2="462" y2="390"/>
    <line x1="514" y1="118" x2="514" y2="390"/>
    <line x1="566" y1="118" x2="566" y2="390"/>
  </g>

  <!-- 기저: 0행 -->
  <g font-size="13" text-anchor="middle" fill="#94a3b8">
    <text x="176" y="143">0</text>
    <text x="228" y="143">1</text>
    <text x="280" y="143">2</text>
    <text x="332" y="143">3</text>
    <text x="384" y="143">4</text>
    <text x="436" y="143">5</text>
    <text x="488" y="143">6</text>
    <text x="540" y="143">7</text>
  </g>
  <!-- 기저: 0열 -->
  <g font-size="13" text-anchor="middle" fill="#94a3b8">
    <text x="176" y="177">1</text>
    <text x="176" y="211">2</text>
    <text x="176" y="245">3</text>
    <text x="176" y="279">4</text>
    <text x="176" y="313">5</text>
    <text x="176" y="347">6</text>
    <text x="176" y="381">7</text>
  </g>

  <!-- 내부 값 -->
  <g font-size="13" text-anchor="middle" fill="#cbd5e1">
    <text x="228" y="177">0</text><text x="280" y="177">1</text><text x="332" y="177">2</text><text x="384" y="177">3</text><text x="436" y="177">4</text><text x="488" y="177">5</text><text x="540" y="177">6</text>
    <text x="228" y="211">1</text><text x="280" y="211">0</text><text x="332" y="211">1</text><text x="384" y="211">2</text><text x="436" y="211">3</text><text x="488" y="211">4</text><text x="540" y="211">5</text>
    <text x="228" y="245">2</text><text x="280" y="245">1</text><text x="332" y="245">0</text><text x="384" y="245">1</text><text x="436" y="245">2</text><text x="488" y="245">3</text><text x="540" y="245">4</text>
    <text x="228" y="279">3</text><text x="280" y="279">2</text><text x="332" y="279">1</text><text x="384" y="279">1</text><text x="436" y="279">1</text><text x="488" y="279">2</text><text x="540" y="279">3</text>
    <text x="228" y="313">4</text><text x="280" y="313">3</text><text x="332" y="313">2</text><text x="384" y="313">2</text><text x="436" y="313">2</text><text x="488" y="313">1</text><text x="540" y="313">2</text>
    <text x="228" y="347">5</text><text x="280" y="347">4</text><text x="332" y="347">3</text><text x="384" y="347">3</text><text x="436" y="347">3</text><text x="488" y="347">2</text><text x="540" y="347">1</text>
    <text x="228" y="381">6</text><text x="280" y="381">5</text><text x="332" y="381">4</text><text x="384" y="381">3</text><text x="436" y="381">4</text><text x="488" y="381">3</text>
  </g>

  <!-- 답 칸 -->
  <rect x="514" y="356" width="52" height="34" fill="none" stroke="#4ade80" stroke-width="2"/>
  <text x="540" y="381" text-anchor="middle" fill="#4ade80" font-size="14" font-weight="700">2</text>

  <text x="604" y="381" text-anchor="middle" fill="#4ade80" font-size="11">답</text>
  <text x="350" y="422" text-anchor="middle" fill="#94a3b8" font-size="11">회색 줄은 기저. 빈 문자열과의 거리는 남은 글자 수와 같다</text>
  <text x="350" y="440" text-anchor="middle" fill="#64748b" font-size="10.5">S₁ = abcabcd (행) · S₂ = abcdabc (열) · 편집 거리 2</text>
</svg>
```

- [ ] **Step 5: 팔레트 밖 색이 없는지 확인한다**

Run:
```bash
grep -ohE '#[0-9a-fA-F]{3,8}' public/images/edit-distance/*.svg | sort -u
```
Expected: 아래 목록의 부분집합만 나온다. 대문자나 8자리가 나오면 고친다.
`#0f1117 #1e293b #3b82f6 #475569 #4ade80 #64748b #93c5fd #94a3b8 #a78bfa #cbd5e1 #e2e8f0 #f87171 #fbbf24`

- [ ] **Step 6: 기존 테스트가 그대로 통과하는지 확인한다**

Run: `npm test`
Expected: 팔레트 검사를 포함해 전부 통과. 새 파일은 `-steps.svg` 가 아니므로 검사 3의 대상이 아니다.

- [ ] **Step 7: 커밋**

```bash
git add public/images/edit-distance
git commit -m "feat(edit-distance): 본편 도판 네 장을 그린다"
```

---

### Task 2: 본편 본문

**Files:**
- Create: `src/content/posts/edit-distance.md`
- Test: `npm run build`, `python .claude/review_post.py src/content/posts/edit-distance.md`

**Interfaces:**
- Consumes: Task 1의 네 SVG (`/images/edit-distance/align-shift.svg`, `subproblem.svg`, `recurrence.svg`, `table.svg`)
- Produces: 라우트 `/blog/edit-distance`. 추가 설명 편이 이 경로로 되돌아 링크한다. 기호 규약도 여기서 정한다: $S_1$, $S_2$, $n$, $m$, $D(i, j)$, $t(i, j)$, 정렬(alignment).

- [ ] **Step 1: 파일을 아래 내용 그대로 만든다**

`description` 은 결정적 검사의 40~220자 범위 안이어야 한다. 아래 문장은 그 범위이며 스펙에 적힌 초안을 두 문장으로 줄인 것이다.

````markdown
---
title: "편집 거리 — 비슷하다는 말을 수로 바꾸기"
date: 2026-08-26T09:00:00
description: "자리끼리만 맞추는 Hamming 거리는 글자 하나가 빠지면 뒤가 전부 밀려 무너진다. 빈 칸을 허용해 정의한 편집 거리를 표 하나로 채우고, O(NM)보다 빠를 수 없다는 말의 정확한 뜻까지 짚는다."
tags: ["Algorithm", "Edit Distance", "Approximate String Matching", "Dynamic Programming", "Hamming Distance"]
category: algorithm
difficulty: 중급
numbered: true
---

> 검색창에 `recieve` 를 치면 `receive` 를 권한다. 기계가 두 낱말이 비슷하다고 판단하려면 '비슷함'이 먼저 수여야 한다. 이 글은 그 수를 정의하고, 정의가 계산 방법까지 정해 주는 과정을 따라간다.

<div class="callout">
<div class="callout-title">이 포스트에서 다루는 내용</div>

- **거리 함수**: 자리끼리만 맞추는 Hamming 거리가 어디서 무너지는가
- **편집 거리**: 넣기·지우기·바꾸기의 최소 횟수
- **점화식**: 최적 정렬의 마지막 열이 세 모양뿐이라는 논증
- **표 채우기**: 기저 두 줄에서 시작해 세 이웃만 보고 채운다
- **비용**: $O(NM)$ 과 "이보다 빠를 수 없다"는 말의 정확한 뜻

</div>

---

## 비슷함을 재는 자

세 장면을 놓고 보자. 검색창의 오타를 고쳐 주는 일, 두 유전자 서열이 얼마나 닮았는지 판정하는 일, 제출된 두 과제가 서로 베낀 것인지 가늠하는 일이다. 하는 일은 다르지만 필요한 재료는 같다. 문자열 두 개를 받아 수 하나를 내놓는 함수, 곧 거리 함수다. 그 수가 작으면 비슷하고 크면 다르다.

거리 함수를 어떻게 정하느냐가 무엇을 '비슷하다'고 볼지 정한다. 정의가 알고리즘보다 먼저다.

---

## 자리끼리 맞추기

가장 단순한 정의는 같은 자리를 견주는 것이다. 길이가 같은 두 문자열에서 글자가 다른 자리의 개수를 세면 Hamming 거리가 된다. `sunny` 와 `funny` 는 첫 자리만 다르므로 1이고, `01101` 과 `00111` 은 두 자리가 다르므로 2다.

이 정의가 제자리를 찾는 곳이 있다. 고정 길이 블록을 네트워크로 주고받는 상황을 보자. 전송 중에 어떤 비트가 뒤집혀도 자리는 밀리지 않는다. 받은 블록과 보낸 블록의 Hamming 거리가 곧 오염된 비트 수다.

문제는 길이가 다를 때다. Hamming 거리는 길이가 같은 두 문자열에만 정의된다. 억지로 앞에서부터 자리를 맞춰 보자. $S_1 = $ `ababc` 와 $S_2 = $ `abbc` 는 앞의 두 자리가 같고, 셋째 자리에서 `a` 와 `b` 가 어긋나고, 넷째 자리에서 `b` 와 `c` 가 어긋나고, 다섯째 자리는 상대가 없다. 어긋남이 세 곳이다.

![위쪽은 ababc와 abbc를 자리끼리 맞춘 비교로 세 자리가 어긋난다. 아래쪽은 셋째 자리에 빈 칸을 허용한 비교로 어긋남이 한 곳이다.](/images/edit-distance/align-shift.svg)

실제로 두 문자열의 차이는 글자 하나다. `ababc` 에서 셋째 글자 `a` 를 지우면 `abbc` 다. 어긋남이 셋으로 부푼 이유는 지운 자리 뒤의 글자가 모두 한 칸씩 밀렸기 때문이다. 자리를 고정한 비교에는 이 밀림을 적을 방법이 없다.

---

## 밀림을 허용하기

밀림을 적으려면 비교하는 쪽에 빈 칸을 놓을 수 있어야 한다. 허용하는 연산을 셋으로 정하자.

- **넣기(insert)**: 글자 하나를 새로 끼워 넣는다
- **지우기(delete)**: 글자 하나를 없앤다
- **바꾸기(change)**: 글자 하나를 다른 글자로 고친다

**편집 거리**(edit distance)는 한 문자열을 다른 문자열로 만드는 데 필요한 이 연산의 최소 횟수다. `ababc` 와 `abbc` 의 편집 거리는 1이다. 지우기 한 번으로 끝난다. 위 그림의 아래쪽이 그 연산을 빈 칸으로 그린 것이다.

바꾸기의 비용을 글자 쌍마다 다르게 두면 **가중 편집 거리**(weighted edit distance)가 된다. 자판을 떠올리면 자연스럽다. `a` 와 `s` 는 한 칸 옆이라 잘못 누르기 쉽고, `a` 와 `p` 는 손이 반대편이라 그럴 일이 드물다. 오타 교정이라면 `a` → `s` 의 비용을 작게, `a` → `p` 의 비용을 크게 두는 편이 실제 오타 분포에 가깝다.

<div class="callout callout-simple">
<div class="callout-title">셋 다 잡지 못하는 것</div>

`abcdef` 와 `defabc` 는 앞의 세 글자와 뒤의 세 글자를 통째로 맞바꾼 관계다. 사람 눈에는 조각을 옮긴 것 하나지만 편집 거리는 6이고, 이는 여섯 글자를 전부 새로 쓰는 값과 같다. 옮기기(move)나 베끼기(copy)를 연산 목록에 넣지 않았으므로 이런 관계는 '완전히 다름'으로 판정된다. 가중치를 얹어도 달라지지 않는다.

</div>

---

## 부분 문제

이제 편집 거리를 계산해야 한다. $S_1$ 과 $S_2$ 의 길이를 각각 $n$, $m$ 이라 하자.

<div class="callout callout-key">
<div class="callout-title">부분 문제의 정의</div>

$D(i, j)$ = $S_1$ 의 앞 $i$ 글자와 $S_2$ 의 앞 $j$ 글자, 곧 두 **접두사** 사이의 편집 거리

</div>

찾는 답은 $D(n, m)$ 이다. $i$ 나 $j$ 가 0이면 빈 문자열과의 거리를 뜻한다.

$S_1 = $ `abcabcd`, $S_2 = $ `abcdabc` 로 보자. $D(2, 4)$ 는 `ab` 와 `abcd` 의 거리이고 값은 2다. `ab` 뒤에 `c` 와 `d` 를 넣으면 되므로 넣기 두 번이다. $D(5, 1)$ 은 `abcab` 와 `a` 의 거리이고 값은 4다. 앞의 `a` 를 짝지어 두고 남은 네 글자를 지우면 된다.

![abcabcd를 행, abcdabc를 열로 둔 격자에서 D(2,4), D(5,1), D(7,7) 세 칸이 각각 어느 접두사 쌍을 가리키는지 표시한 그림](/images/edit-distance/subproblem.svg)

$i$ 는 0부터 $n$, $j$ 는 0부터 $m$ 까지 움직이므로 칸은 $(n+1)(m+1)$ 개다.

---

## 마지막 열에서 무슨 일이 있었나

점화식을 세우기 전에 말을 하나 만들어 두자. 두 문자열의 글자를 위아래로 짝지어 늘어놓은 것을 **정렬**(alignment)이라 부른다. 열은 세 모양뿐이다.

- 위아래에 글자가 하나씩 있는 열. 두 글자가 같으면 비용 0, 다르면 바꾸기 한 번이므로 비용 1
- 위에만 글자가 있는 열. $S_1$ 의 글자를 지우므로 비용 1
- 아래에만 글자가 있는 열. $S_2$ 의 글자를 넣으므로 비용 1

정렬의 비용은 열 비용의 합이고, 편집 거리는 비용이 가장 작은 정렬의 비용이다. 앞 그림 아래쪽의 빈 칸 표기가 바로 정렬이다.

이제 $D(i, j)$ 를 내는 최적 정렬의 **마지막 열**만 본다.

<div class="thm">
<div class="thm-head">정리 1<span class="en">마지막 열의 세 모양</span></div>

$t(i, j)$ 를 $S_1[i] = S_2[j]$ 이면 0, 아니면 1이라 하자. $i \ge 1$, $j \ge 1$ 이면 다음이 성립한다.

$$
D(i, j) \;=\; \min\bigl\{\, D(i-1, j-1) + t(i, j),\;\; D(i-1, j) + 1,\;\; D(i, j-1) + 1 \,\bigr\}
$$

기저는 $D(i, 0) = i$, $D(0, j) = j$ 다.

</div>

<div class="proof">

<span class="proof-lead">증명.</span> 기저부터 보자. 한쪽이 빈 문자열이면 짝지을 글자가 없다. $S_1$ 의 앞 $i$ 글자를 모두 지우는 정렬만 가능하고 그 비용은 $i$ 다. 반대쪽도 같은 이유로 $j$ 다.

**좌변은 우변 이하다.** 우변의 세 값 각각에 대해 그 비용을 내는 정렬을 실제로 만들 수 있다. $D(i-1, j-1)$ 을 내는 정렬 뒤에 $S_1[i]$ 와 $S_2[j]$ 가 마주 보는 열을 붙이면 두 접두사 전체를 덮는 정렬이고 비용은 $D(i-1, j-1) + t(i, j)$ 다. $D(i-1, j)$ 를 내는 정렬 뒤에 $S_1[i]$ 만 있는 열을 붙이면 비용은 $D(i-1, j) + 1$ 이고, $D(i, j-1)$ 을 내는 정렬 뒤에 $S_2[j]$ 만 있는 열을 붙이면 비용은 $D(i, j-1) + 1$ 이다. 편집 거리는 가능한 정렬 중 최소 비용이므로 $D(i, j)$ 는 세 값 모두 이하이고, 따라서 최솟값 이하다.

**좌변은 우변 이상이다.** $D(i, j)$ 를 내는 최적 정렬 $A$ 를 하나 잡는다. $i \ge 1$ 이고 $j \ge 1$ 이므로 $A$ 에는 열이 하나 이상 있고, 마지막 열은 위에서 나눈 세 모양 중 하나다.

- 위아래에 글자가 있는 열이라면 그 두 글자는 각 접두사의 마지막 글자, 곧 $S_1[i]$ 와 $S_2[j]$ 다. 이 열을 떼면 남는 것은 $S_1$ 의 앞 $i-1$ 글자와 $S_2$ 의 앞 $j-1$ 글자를 덮는 정렬이고, 그 비용은 최소 비용인 $D(i-1, j-1)$ 이상이다. 뗀 열의 비용이 $t(i, j)$ 이므로 $A$ 의 비용은 $D(i-1, j-1) + t(i, j)$ 이상이다.
- 위에만 글자가 있는 열이라면 그 글자는 $S_1[i]$ 다. 같은 논리로 $A$ 의 비용은 $D(i-1, j) + 1$ 이상이다.
- 아래에만 글자가 있는 열이라면 그 글자는 $S_2[j]$ 다. $A$ 의 비용은 $D(i, j-1) + 1$ 이상이다.

세 모양이 경우 전체를 덮으므로 $A$ 의 비용은 우변의 세 값 중 적어도 하나 이상이고, 그 값은 최솟값 이상이다. $A$ 의 비용이 $D(i, j)$ 이므로 좌변은 우변 이상이다. 두 방향을 합치면 등호다. <span class="qed">∎</span>

</div>

이 정리가 답하는 물음이 하나 있다. 계산을 시작할 때 우리는 $S_1[i]$ 와 $S_2[j]$ 가 같은지 다른지 알아야 하는 것처럼 보이지만, 두 글자의 일치 여부는 $t(i, j)$ 한 항이 전부 흡수하고 나머지 구조는 그대로다. 맞추기(match)와 바꾸기를 따로 세면 갈래가 넷이고 열의 모양으로 세면 셋인 이유도 같다. 두 연산은 같은 모양의 열에서 비용만 갈린다.

![D(i,j) 칸으로 들어오는 세 화살표와, 그 칸이 다시 쓰이는 세 칸을 점선으로 표시한 그림](/images/edit-distance/recurrence.svg)

---

## 답이 연산의 열이라는 관점

같은 이야기를 다른 각도에서 적을 수도 있다. 답은 넣기·지우기·맞추기·바꾸기 네 기호를 늘어놓은 열이고, 편집 거리는 그중 비용이 가장 작은 열의 비용이다.

이렇게 적으면 순환처럼 들린다. 최선의 열을 정의하는 자리에 최선의 열이 다시 나온다. 순환이 아닌 이유는 참조의 방향이다. $(i, j)$ 의 답은 $(i-1, j-1)$, $(i-1, j)$, $(i, j-1)$ 세 곳만 본다. 어느 쪽으로 가든 $i + j$ 가 적어도 1 줄어든다. 줄어들기만 하는 참조는 유한 번에 $(0, 0)$ 에 닿고, 그 자리의 답은 빈 열이다. 순환 참조는 같은 크기의 문제를 다시 참조할 때 생기며, 여기에는 그런 참조가 없다.

표를 격자로 보면 대응이 더 분명해진다. 칸 $(i, j)$ 를 격자점으로 두면 연산의 열은 $(0, 0)$ 에서 $(n, m)$ 까지 가는 걸음의 열이다.

- 대각선으로 한 칸 = 맞추기 또는 바꾸기
- 아래로 한 칸 = $S_1$ 의 글자 지우기
- 오른쪽으로 한 칸 = $S_2$ 의 글자 넣기

걸음마다 비용이 붙고 편집 거리는 가장 싼 경로의 비용이다. 편집 거리를 구하는 일은 격자에서 최단 경로를 찾는 일과 같다. 이 대응은 [추가 설명](/blog/edit-distance-traceback)에서 다시 쓴다.

---

## 표 채우기

기저 두 줄부터 채운다. $D(i, 0) = i$, $D(0, j) = j$ 이므로 첫 열과 첫 행은 0, 1, 2, … 로 늘어난다.

내부 칸은 위·왼쪽·왼쪽 위 대각선을 본다. 세 이웃이 먼저 채워져 있어야 하므로 위에서 아래로, 각 행에서는 왼쪽에서 오른쪽으로 훑으면 된다.

작은 예를 손으로 채워 보자. $S_1 = $ `v`, $S_2 = $ `wr` 다. 기저는 $D(0, 0) = 0$, $D(0, 1) = 1$, $D(0, 2) = 2$, $D(1, 0) = 1$ 이다.

- $D(1, 1)$: `v` 와 `w` 가 다르므로 $t = 1$ 이다. 대각선 $0 + 1 = 1$, 위 $1 + 1 = 2$, 왼쪽 $1 + 1 = 2$ 중 최솟값은 1
- $D(1, 2)$: `v` 와 `r` 가 다르므로 $t = 1$ 이다. 대각선 $1 + 1 = 2$, 위 $2 + 1 = 3$, 왼쪽 $1 + 1 = 2$ 중 최솟값은 2

$D(1, 2) = 2$ 인데 최솟값을 이룬 이웃이 둘이다. 대각선에서 왔다면 `w` 를 넣고 `v` 를 `r` 로 바꾼 것이고, 왼쪽에서 왔다면 `v` 를 `w` 로 바꾸고 `r` 를 넣은 것이다. 두 정렬의 비용이 같다. 값은 하나지만 그 값을 내는 방법은 여럿일 수 있다.

앞의 예시로 돌아가 $S_1 = $ `abcabcd`, $S_2 = $ `abcdabc` 의 표를 끝까지 채우면 이렇다.

![abcabcd와 abcdabc의 완성된 편집 거리 표. 기저인 첫 행과 첫 열은 0부터 7까지 늘어나고 마지막 칸의 값은 2다.](/images/edit-distance/table.svg)

답은 2다. `abc` 뒤에 `d` 를 넣고 맨 끝의 `d` 를 지우면 `abcdabc` 가 된다.

---

## 비용

칸이 $(n+1)(m+1)$ 개이고, 칸마다 하는 일은 이웃 세 값을 견주고 $t$ 를 한 번 구하는 것이라 상수 시간이다. 전체는 $O(NM)$ 이다. 여기서 $N$, $M$ 은 두 문자열의 길이 $n$, $m$ 을 가리킨다.

표를 통째로 들고 있으면 공간도 $O(NM)$ 이다. 값만 필요하다면 훨씬 적게 쓸 수 있다. 한 행을 채우는 동안 참조하는 것은 바로 위 행과 지금 행뿐이므로 두 행만 남기면 되고, 짧은 쪽을 열로 두면 공간은 $O(\min(N, M))$ 이다.

재귀로 곧장 옮기면 사정이 다르다. 호출 하나가 갈래 셋으로 벌어지고 깊이는 최대 $n + m$ 이므로 호출 수가 $3^{n+m}$ 까지 간다. 같은 칸을 몇 번씩 다시 계산하기 때문이다. 표 내부의 칸 $D(i, j)$ 는 $D(i+1, j)$, $D(i, j+1)$, $D(i+1, j+1)$ 세 곳에서 쓰인다. 마지막 행과 열의 칸은 이보다 적게 쓰이고 $D(n, m)$ 은 쓰이지 않는다. 표는 그 칸을 한 번만 계산해 세 번 나눠 쓴다.

### 이보다 빠를 수 없다는 말

$O(NM)$ 을 두고 "이보다 빠른 방법은 없다"고 말할 때가 있다. 정확히 옮기면 조건이 붙는다.

무조건적인 하한은 알려져 있지 않다. 알려진 것은 다른 가설에 기댄 하한이다. Backurs와 Indyk는 SETH(강한 지수 시간 가설)가 참이라면 어떤 상수 $\varepsilon > 0$ 에 대해서도 $O(n^{2-\varepsilon})$ 시간 알고리즘이 존재하지 않음을 보였다. 근거가 SETH이므로 SETH가 거짓으로 밝혀지면 이 결론도 함께 무너진다.

조건을 좁히면 더 빠른 방법이 실제로 있다.

- 알파벳이 유한하면 Masek과 Paterson의 방법이 로그 인자만큼 빠르다. 작은 조각의 계산 결과를 미리 표로 만들어 두고 한꺼번에 가져다 쓰는 방식이다.
- 편집 거리가 $d$ 이하라고 미리 알고 있으면 Ukkonen의 방법이 $O(nd)$ 다. 최적 경로는 주대각선에서 $d$ 칸보다 멀리 벗어날 수 없다. 벗어난 만큼 되돌아와야 하고 그 왕복만으로 이미 비용이 $d$ 를 넘기 때문이다. 대각선 주변의 띠만 채우면 된다.

<div class="callout callout-simple">
<div class="callout-title">참고 문헌</div>

- R. A. Wagner, M. J. Fischer, "The String-to-String Correction Problem", *JACM* 21(1), 1974
- W. J. Masek, M. S. Paterson, "A faster algorithm computing string edit distances", *JCSS* 20(1), 1980
- E. Ukkonen, "Algorithms for approximate string matching", *Information and Control* 64, 1985
- A. Backurs, P. Indyk, "Edit Distance Cannot Be Computed in Strongly Subquadratic Time (unless SETH is false)", *STOC* 2015 ([arXiv:1412.0348](https://arxiv.org/abs/1412.0348))

</div>

---

## 코드

표를 그대로 옮기면 이렇다. 본문의 인덱스는 1부터 셌고 배열은 0부터 세므로 글자를 꺼낼 때 하나를 뺀다.

```cpp
// 단위 비용: 넣기·지우기·바꾸기가 모두 1
int editDistance(const string& s1, const string& s2) {
    int n = s1.size(), m = s2.size();
    vector<vector<int>> D(n + 1, vector<int>(m + 1));

    for (int i = 0; i <= n; i++) D[i][0] = i;   // 기저: 전부 지우기
    for (int j = 0; j <= m; j++) D[0][j] = j;   // 기저: 전부 넣기

    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) {
            int t = (s1[i-1] == s2[j-1]) ? 0 : 1;
            D[i][j] = min({ D[i-1][j-1] + t,    // 맞추기 또는 바꾸기
                            D[i-1][j] + 1,      // s1[i] 지우기
                            D[i][j-1] + 1 });   // s2[j] 넣기
        }
    return D[n][m];
}
```

값만 필요하면 두 행으로 줄인다. 단위 비용에서는 넣기와 지우기의 값이 같아 편집 거리가 대칭이므로, 두 문자열의 역할을 바꿔 짧은 쪽을 열에 두어도 답은 같다.

```cpp
int editDistanceTwoRows(const string& s1, const string& s2) {
    const string& a = s1.size() >= s2.size() ? s1 : s2;   // 긴 쪽을 행으로
    const string& b = s1.size() >= s2.size() ? s2 : s1;   // 짧은 쪽을 열로
    int n = a.size(), m = b.size();

    vector<int> prev(m + 1), cur(m + 1);
    for (int j = 0; j <= m; j++) prev[j] = j;

    for (int i = 1; i <= n; i++) {
        cur[0] = i;
        for (int j = 1; j <= m; j++) {
            int t = (a[i-1] == b[j-1]) ? 0 : 1;
            cur[j] = min({ prev[j-1] + t, prev[j] + 1, cur[j-1] + 1 });
        }
        swap(prev, cur);            // 방금 채운 행이 다음 반복의 '위 행'이 된다
    }
    return prev[m];
}
```

가중 편집 거리로 옮기려면 세 항의 `1` 과 `t` 를 비용 함수로 바꾸면 된다. 넣기와 지우기의 비용을 다르게 두는 순간 대칭이 깨지므로, 짧은 쪽을 열로 두는 위의 교체는 그때 쓸 수 없다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

편집 거리는 최소 비용 정렬의 비용이다. 최적 정렬의 마지막 열이 세 모양 중 하나라는 사실에서 점화식이 곧바로 나온다. 표는 칸마다 세 이웃만 보고 한 번씩 채우므로 $O(NM)$ 이며, 이보다 빠른 일반 알고리즘이 없다는 결론은 SETH 가정에 기대고 있다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>

표를 다 채웠지만 손에 남은 것은 수 하나다. 어떤 연산을 어디에 썼는지는 표에 적혀 있지 않고, `v` 와 `wr` 에서 봤듯 같은 값을 내는 정렬이 여럿일 수도 있다. 표를 거꾸로 읽어 연산을 복원하는 방법과, 최적 정렬이 여럿일 때 결과가 왜 길 하나가 아니라 표 위의 영역이 되는지는 [추가 설명 — 되짚기는 길 하나가 아니라 영역을 준다](/blog/edit-distance-traceback)에서 다룬다.

</div>

---

## 마치며

시작은 정의 문제였다. 자리를 고정한 비교는 밀림을 적지 못했고, 빈 칸을 허용하자 편집 거리가 나왔다. 정의를 바꾸자 계산 방법도 따라 바뀌었다. 최적 정렬의 마지막 열이 무엇이었는지 되묻는 것만으로 점화식이 나왔고, 표 하나가 그 점화식을 그대로 담았다.

무엇을 연산 목록에 넣느냐가 무엇을 '비슷하다'고 볼지 정한다. 옮기기를 넣지 않았기 때문에 `abcdef` 와 `defabc` 는 완전히 다른 문자열이다. 목록을 늘리면 잡아내는 관계도 늘지만 계산은 그만큼 어려워진다. [최대 부분배열](/blog/maximum-subarray)에서도 부분 문제를 어떻게 잡느냐가 알고리즘을 갈랐다. 여기서는 부분 문제를 접두사 쌍으로 잡은 한 줄이 표 하나를 만들었다.
````

- [ ] **Step 2: 결정적 검사를 돌린다**

Run: `python .claude/review_post.py src/content/posts/edit-distance.md`
Expected: `발견 사항 없음 ✅`. `description` 길이(40~220자), 줄표 임계치, `$$` 단독 줄, 이미지 존재 검사가 여기서 걸린다. 걸리면 문장을 고치고 다시 돌린다.

- [ ] **Step 3: 빌드로 스키마와 수식을 확인한다**

Run: `npm run build`
Expected: 오류 없이 `N page(s) built`. KaTeX 파싱 실패는 여기서 드러난다.

- [ ] **Step 4: 커밋**

```bash
git add src/content/posts/edit-distance.md
git commit -m "feat(edit-distance): 편집 거리 본편을 쓴다"
```

---

### Task 3: 추가 설명 도판 3장

**Files:**
- Create: `public/images/edit-distance-traceback/traceback-path.svg`
- Create: `public/images/edit-distance-traceback/region.svg`
- Create: `public/images/edit-distance-traceback/alignments.svg`
- Test: `npm test`, 팔레트 밖 hex `grep`

**Interfaces:**
- Consumes: 없음. 격자 좌표 규약(칸 54×34, 원점 (170, 112))은 두 표 도판이 공유한다.
- Produces: 위 세 경로. 추가 설명 본문이 `/images/edit-distance-traceback/<파일>` 로 참조한다.

세 도판 모두 `abcab`(행) × `abcba`(열) 표를 쓴다. 값은 다음과 같다.

```
      -  a  b  c  b  a
   -  0  1  2  3  4  5
   a  1  0  1  2  3  4
   b  2  1  0  1  2  3
   c  3  2  1  0  1  2
   a  4  3  2  1  1  1
   b  5  4  3  2  1  2
```

- [ ] **Step 1: `traceback-path.svg` 를 만든다**

```svg
<svg viewBox="0 0 680 400" width="1020" height="600" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="edt-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#4ade80"/>
    </marker>
    <marker id="edt-arrow-dim" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#64748b"/>
    </marker>
  </defs>

  <rect width="680" height="400" rx="10" fill="#0f1117"/>

  <text x="340" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">표를 거꾸로 읽으면 연산이 나온다</text>
  <text x="340" y="53" text-anchor="middle" fill="#64748b" font-size="11">칸마다 어느 이웃에서 왔는지 되묻는다</text>

  <!-- 열 머리 -->
  <g font-size="12" text-anchor="middle" fill="#94a3b8">
    <text x="197" y="104">–</text>
    <text x="251" y="104">a</text>
    <text x="305" y="104">b</text>
    <text x="359" y="104">c</text>
    <text x="413" y="104">b</text>
    <text x="467" y="104">a</text>
  </g>
  <!-- 행 머리 -->
  <g font-size="12" text-anchor="end" fill="#94a3b8">
    <text x="158" y="133">–</text>
    <text x="158" y="167">a</text>
    <text x="158" y="201">b</text>
    <text x="158" y="235">c</text>
    <text x="158" y="269">a</text>
    <text x="158" y="303">b</text>
  </g>

  <!-- 격자 -->
  <g stroke="#475569" stroke-width="0.8">
    <line x1="170" y1="112" x2="494" y2="112"/>
    <line x1="170" y1="146" x2="494" y2="146"/>
    <line x1="170" y1="180" x2="494" y2="180"/>
    <line x1="170" y1="214" x2="494" y2="214"/>
    <line x1="170" y1="248" x2="494" y2="248"/>
    <line x1="170" y1="282" x2="494" y2="282"/>
    <line x1="170" y1="316" x2="494" y2="316"/>
    <line x1="170" y1="112" x2="170" y2="316"/>
    <line x1="224" y1="112" x2="224" y2="316"/>
    <line x1="278" y1="112" x2="278" y2="316"/>
    <line x1="332" y1="112" x2="332" y2="316"/>
    <line x1="386" y1="112" x2="386" y2="316"/>
    <line x1="440" y1="112" x2="440" y2="316"/>
    <line x1="494" y1="112" x2="494" y2="316"/>
  </g>

  <!-- 되짚은 경로가 지나는 칸 -->
  <g fill="none" stroke="#4ade80" stroke-width="1.8">
    <rect x="170" y="112" width="54" height="34"/>
    <rect x="224" y="146" width="54" height="34"/>
    <rect x="278" y="180" width="54" height="34"/>
    <rect x="332" y="214" width="54" height="34"/>
    <rect x="386" y="248" width="54" height="34"/>
    <rect x="440" y="282" width="54" height="34"/>
  </g>

  <!-- 기저 값 -->
  <g font-size="13" text-anchor="middle" fill="#94a3b8">
    <text x="197" y="133">0</text>
    <text x="251" y="133">1</text>
    <text x="305" y="133">2</text>
    <text x="359" y="133">3</text>
    <text x="413" y="133">4</text>
    <text x="467" y="133">5</text>
    <text x="197" y="167">1</text>
    <text x="197" y="201">2</text>
    <text x="197" y="235">3</text>
    <text x="197" y="269">4</text>
    <text x="197" y="303">5</text>
  </g>

  <!-- 내부 값 -->
  <g font-size="13" text-anchor="middle" fill="#cbd5e1">
    <text x="251" y="167">0</text><text x="305" y="167">1</text><text x="359" y="167">2</text><text x="413" y="167">3</text><text x="467" y="167">4</text>
    <text x="251" y="201">1</text><text x="305" y="201">0</text><text x="359" y="201">1</text><text x="413" y="201">2</text><text x="467" y="201">3</text>
    <text x="251" y="235">2</text><text x="305" y="235">1</text><text x="359" y="235">0</text><text x="413" y="235">1</text><text x="467" y="235">2</text>
    <text x="251" y="269">3</text><text x="305" y="269">2</text><text x="359" y="269">1</text><text x="413" y="269">1</text><text x="467" y="269">1</text>
    <text x="251" y="303">4</text><text x="305" y="303">3</text><text x="359" y="303">2</text><text x="413" y="303">1</text><text x="467" y="303">2</text>
  </g>

  <!-- 되짚기 화살표 (칸 경계를 가로지른다) -->
  <g stroke="#4ade80" stroke-width="1.8" fill="none" marker-end="url(#edt-arrow)">
    <path d="M 456,294 L 424,270"/>
    <path d="M 398,256 L 374,240"/>
    <path d="M 344,222 L 320,206"/>
    <path d="M 290,188 L 266,172"/>
    <path d="M 236,154 L 212,138"/>
  </g>

  <!-- 고르지 않은 이웃 -->
  <g stroke="#64748b" stroke-width="1.4" fill="none" stroke-dasharray="4 3" marker-end="url(#edt-arrow-dim)">
    <path d="M 475,292 L 475,272"/>
    <path d="M 450,307 L 428,307"/>
  </g>

  <!-- 연산 라벨 -->
  <text x="506" y="303" fill="#fbbf24" font-size="11">바꾸기 b → a</text>
  <text x="506" y="269" fill="#fbbf24" font-size="11">바꾸기 a → b</text>
  <text x="506" y="235" fill="#94a3b8" font-size="11">맞추기 c</text>
  <text x="506" y="201" fill="#94a3b8" font-size="11">맞추기 b</text>
  <text x="506" y="167" fill="#94a3b8" font-size="11">맞추기 a</text>

  <text x="340" y="352" text-anchor="middle" fill="#94a3b8" font-size="11">점선은 고르지 않은 이웃이다. (5, 5)에서는 세 이웃 모두 등호가 성립한다</text>
  <text x="340" y="374" text-anchor="middle" fill="#64748b" font-size="10.5">S₁ = abcab (행) · S₂ = abcba (열) · 편집 거리 2</text>
</svg>
```

- [ ] **Step 2: `region.svg` 를 만든다**

```svg
<svg viewBox="0 0 680 460" width="1020" height="690" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <defs>
    <marker id="edt-r-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#4ade80"/>
    </marker>
    <marker id="edt-r-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#fbbf24"/>
    </marker>
    <marker id="edt-r-violet" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#a78bfa"/>
    </marker>
    <marker id="edt-r-soft" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#6ee7b7"/>
    </marker>
  </defs>

  <rect width="680" height="460" rx="10" fill="#0f1117"/>

  <text x="340" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">최적 경로가 여럿이면 결과는 영역이 된다</text>
  <text x="340" y="53" text-anchor="middle" fill="#64748b" font-size="11">세 경로가 함께 지나는 구간은 옅은 초록으로 한 번만 그렸다</text>

  <!-- 열 머리 -->
  <g font-size="12" text-anchor="middle" fill="#94a3b8">
    <text x="197" y="104">–</text>
    <text x="251" y="104">a</text>
    <text x="305" y="104">b</text>
    <text x="359" y="104">c</text>
    <text x="413" y="104">b</text>
    <text x="467" y="104">a</text>
  </g>
  <!-- 행 머리 -->
  <g font-size="12" text-anchor="end" fill="#94a3b8">
    <text x="158" y="133">–</text>
    <text x="158" y="167">a</text>
    <text x="158" y="201">b</text>
    <text x="158" y="235">c</text>
    <text x="158" y="269">a</text>
    <text x="158" y="303">b</text>
  </g>

  <!-- 격자 -->
  <g stroke="#475569" stroke-width="0.8">
    <line x1="170" y1="112" x2="494" y2="112"/>
    <line x1="170" y1="146" x2="494" y2="146"/>
    <line x1="170" y1="180" x2="494" y2="180"/>
    <line x1="170" y1="214" x2="494" y2="214"/>
    <line x1="170" y1="248" x2="494" y2="248"/>
    <line x1="170" y1="282" x2="494" y2="282"/>
    <line x1="170" y1="316" x2="494" y2="316"/>
    <line x1="170" y1="112" x2="170" y2="316"/>
    <line x1="224" y1="112" x2="224" y2="316"/>
    <line x1="278" y1="112" x2="278" y2="316"/>
    <line x1="332" y1="112" x2="332" y2="316"/>
    <line x1="386" y1="112" x2="386" y2="316"/>
    <line x1="440" y1="112" x2="440" y2="316"/>
    <line x1="494" y1="112" x2="494" y2="316"/>
  </g>

  <!-- 영역: 어떤 최적 경로가 지나는 칸 -->
  <g fill="none" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="5 3">
    <rect x="170" y="112" width="54" height="34"/>
    <rect x="224" y="146" width="54" height="34"/>
    <rect x="278" y="180" width="54" height="34"/>
    <rect x="332" y="214" width="54" height="34"/>
    <rect x="386" y="214" width="54" height="34"/>
    <rect x="332" y="248" width="54" height="34"/>
    <rect x="386" y="248" width="54" height="34"/>
    <rect x="440" y="248" width="54" height="34"/>
    <rect x="386" y="282" width="54" height="34"/>
    <rect x="440" y="282" width="54" height="34"/>
  </g>

  <!-- 기저 값 -->
  <g font-size="13" text-anchor="middle" fill="#94a3b8">
    <text x="197" y="133">0</text>
    <text x="251" y="133">1</text>
    <text x="305" y="133">2</text>
    <text x="359" y="133">3</text>
    <text x="413" y="133">4</text>
    <text x="467" y="133">5</text>
    <text x="197" y="167">1</text>
    <text x="197" y="201">2</text>
    <text x="197" y="235">3</text>
    <text x="197" y="269">4</text>
    <text x="197" y="303">5</text>
  </g>

  <!-- 내부 값 -->
  <g font-size="13" text-anchor="middle" fill="#cbd5e1">
    <text x="251" y="167">0</text><text x="305" y="167">1</text><text x="359" y="167">2</text><text x="413" y="167">3</text><text x="467" y="167">4</text>
    <text x="251" y="201">1</text><text x="305" y="201">0</text><text x="359" y="201">1</text><text x="413" y="201">2</text><text x="467" y="201">3</text>
    <text x="251" y="235">2</text><text x="305" y="235">1</text><text x="359" y="235">0</text><text x="413" y="235">1</text><text x="467" y="235">2</text>
    <text x="251" y="269">3</text><text x="305" y="269">2</text><text x="359" y="269">1</text><text x="413" y="269">1</text><text x="467" y="269">1</text>
    <text x="251" y="303">4</text><text x="305" y="303">3</text><text x="359" y="303">2</text><text x="413" y="303">1</text><text x="467" y="303">2</text>
  </g>

  <!-- 세 경로가 공유하는 구간 -->
  <g stroke="#6ee7b7" stroke-width="1.8" fill="none" marker-end="url(#edt-r-soft)">
    <path d="M 344,222 L 320,206"/>
    <path d="M 290,188 L 266,172"/>
    <path d="M 236,154 L 212,138"/>
  </g>

  <!-- 경로 1: 바꾸기 두 번 -->
  <g stroke="#4ade80" stroke-width="1.8" fill="none" marker-end="url(#edt-r-green)">
    <path d="M 456,294 L 424,270"/>
    <path d="M 398,256 L 374,240"/>
  </g>

  <!-- 경로 2: b 넣고 b 지우기 -->
  <g stroke="#fbbf24" stroke-width="1.8" fill="none" marker-end="url(#edt-r-amber)">
    <path d="M 475,292 L 475,272"/>
    <path d="M 452,258 L 428,238"/>
    <path d="M 398,224 L 376,224"/>
  </g>

  <!-- 경로 3: a 지우고 a 넣기 -->
  <g stroke="#a78bfa" stroke-width="1.8" fill="none" marker-end="url(#edt-r-violet)">
    <path d="M 450,307 L 428,307"/>
    <path d="M 398,292 L 374,272"/>
    <path d="M 347,258 L 347,238"/>
  </g>

  <!-- 범례 -->
  <rect x="120" y="344" width="12" height="4" fill="#4ade80"/>
  <text x="142" y="352" fill="#cbd5e1" font-size="11.5">경로 1 · 바꾸기 두 번</text>

  <rect x="120" y="366" width="12" height="4" fill="#fbbf24"/>
  <text x="142" y="374" fill="#cbd5e1" font-size="11.5">경로 2 · b 를 넣고 b 를 지운다</text>

  <rect x="120" y="388" width="12" height="4" fill="#a78bfa"/>
  <text x="142" y="396" fill="#cbd5e1" font-size="11.5">경로 3 · a 를 지우고 a 를 넣는다</text>

  <rect x="120" y="408" width="12" height="12" fill="none" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="4 3"/>
  <text x="142" y="418" fill="#cbd5e1" font-size="11.5">파선 칸 · 어떤 최적 경로가 지나는 칸, 곧 영역</text>

  <text x="340" y="444" text-anchor="middle" fill="#94a3b8" font-size="11">영역 안을 아무렇게나 걸어도 최적은 아니다. (3, 4)와 (4, 3)을 함께 쓰는 경로는 없다</text>
</svg>
```

- [ ] **Step 3: `alignments.svg` 를 만든다**

```svg
<svg viewBox="0 0 680 410" width="1020" height="615" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,-apple-system,sans-serif">
  <rect width="680" height="410" rx="10" fill="#0f1117"/>

  <text x="340" y="32" text-anchor="middle" fill="#e2e8f0" font-size="15" font-weight="600">같은 비용의 정렬이 셋이다</text>
  <text x="340" y="53" text-anchor="middle" fill="#64748b" font-size="11">위 줄이 S₁, 아래 줄이 S₂. – 는 빈 칸이다</text>

  <!-- ===== 정렬 1: 바꾸기 두 번 ===== -->
  <text x="188" y="112" text-anchor="end" fill="#cbd5e1" font-size="12">정렬 1</text>

  <g fill="#1e293b" stroke="#475569" stroke-width="1">
    <rect x="200" y="88" width="40" height="32" rx="3"/>
    <rect x="246" y="88" width="40" height="32" rx="3"/>
    <rect x="292" y="88" width="40" height="32" rx="3"/>
    <rect x="200" y="126" width="40" height="32" rx="3"/>
    <rect x="246" y="126" width="40" height="32" rx="3"/>
    <rect x="292" y="126" width="40" height="32" rx="3"/>
  </g>
  <g fill="#1e293b" stroke="#fbbf24" stroke-width="1.6">
    <rect x="338" y="88" width="40" height="32" rx="3"/>
    <rect x="384" y="88" width="40" height="32" rx="3"/>
    <rect x="338" y="126" width="40" height="32" rx="3"/>
    <rect x="384" y="126" width="40" height="32" rx="3"/>
  </g>
  <g font-size="14" text-anchor="middle" fill="#94a3b8">
    <text x="220" y="109">a</text><text x="266" y="109">b</text><text x="312" y="109">c</text>
    <text x="220" y="147">a</text><text x="266" y="147">b</text><text x="312" y="147">c</text>
  </g>
  <g font-size="14" text-anchor="middle" fill="#fbbf24">
    <text x="358" y="109">a</text><text x="404" y="109">b</text>
    <text x="358" y="147">b</text><text x="404" y="147">a</text>
  </g>
  <text x="450" y="128" fill="#cbd5e1" font-size="11.5">바꾸기 두 번</text>

  <!-- ===== 정렬 2: b 를 넣고 b 를 지운다 ===== -->
  <text x="188" y="210" text-anchor="end" fill="#cbd5e1" font-size="12">정렬 2</text>

  <g fill="#1e293b" stroke="#475569" stroke-width="1">
    <rect x="200" y="186" width="40" height="32" rx="3"/>
    <rect x="246" y="186" width="40" height="32" rx="3"/>
    <rect x="292" y="186" width="40" height="32" rx="3"/>
    <rect x="384" y="186" width="40" height="32" rx="3"/>
    <rect x="200" y="224" width="40" height="32" rx="3"/>
    <rect x="246" y="224" width="40" height="32" rx="3"/>
    <rect x="292" y="224" width="40" height="32" rx="3"/>
    <rect x="384" y="224" width="40" height="32" rx="3"/>
  </g>
  <rect x="338" y="186" width="40" height="32" rx="3" fill="none" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="4 3"/>
  <rect x="338" y="224" width="40" height="32" rx="3" fill="#1e293b" stroke="#93c5fd" stroke-width="1.6"/>
  <rect x="430" y="186" width="40" height="32" rx="3" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="430" y="224" width="40" height="32" rx="3" fill="none" stroke="#f87171" stroke-width="1.6" stroke-dasharray="4 3"/>

  <g font-size="14" text-anchor="middle" fill="#94a3b8">
    <text x="220" y="207">a</text><text x="266" y="207">b</text><text x="312" y="207">c</text><text x="404" y="207">a</text>
    <text x="220" y="245">a</text><text x="266" y="245">b</text><text x="312" y="245">c</text><text x="404" y="245">a</text>
  </g>
  <text x="358" y="207" text-anchor="middle" fill="#93c5fd" font-size="14">–</text>
  <text x="358" y="245" text-anchor="middle" fill="#93c5fd" font-size="14">b</text>
  <text x="450" y="207" text-anchor="middle" fill="#f87171" font-size="14">b</text>
  <text x="450" y="245" text-anchor="middle" fill="#f87171" font-size="14">–</text>
  <text x="496" y="226" fill="#cbd5e1" font-size="11.5">넣기 1 + 지우기 1</text>

  <!-- ===== 정렬 3: a 를 지우고 a 를 넣는다 ===== -->
  <text x="188" y="308" text-anchor="end" fill="#cbd5e1" font-size="12">정렬 3</text>

  <g fill="#1e293b" stroke="#475569" stroke-width="1">
    <rect x="200" y="284" width="40" height="32" rx="3"/>
    <rect x="246" y="284" width="40" height="32" rx="3"/>
    <rect x="292" y="284" width="40" height="32" rx="3"/>
    <rect x="384" y="284" width="40" height="32" rx="3"/>
    <rect x="200" y="322" width="40" height="32" rx="3"/>
    <rect x="246" y="322" width="40" height="32" rx="3"/>
    <rect x="292" y="322" width="40" height="32" rx="3"/>
    <rect x="384" y="322" width="40" height="32" rx="3"/>
  </g>
  <rect x="338" y="284" width="40" height="32" rx="3" fill="#1e293b" stroke="#f87171" stroke-width="1.6"/>
  <rect x="338" y="322" width="40" height="32" rx="3" fill="none" stroke="#f87171" stroke-width="1.6" stroke-dasharray="4 3"/>
  <rect x="430" y="284" width="40" height="32" rx="3" fill="none" stroke="#93c5fd" stroke-width="1.6" stroke-dasharray="4 3"/>
  <rect x="430" y="322" width="40" height="32" rx="3" fill="#1e293b" stroke="#93c5fd" stroke-width="1.6"/>

  <g font-size="14" text-anchor="middle" fill="#94a3b8">
    <text x="220" y="305">a</text><text x="266" y="305">b</text><text x="312" y="305">c</text><text x="404" y="305">b</text>
    <text x="220" y="343">a</text><text x="266" y="343">b</text><text x="312" y="343">c</text><text x="404" y="343">b</text>
  </g>
  <text x="358" y="305" text-anchor="middle" fill="#f87171" font-size="14">a</text>
  <text x="358" y="343" text-anchor="middle" fill="#f87171" font-size="14">–</text>
  <text x="450" y="305" text-anchor="middle" fill="#93c5fd" font-size="14">–</text>
  <text x="450" y="343" text-anchor="middle" fill="#93c5fd" font-size="14">a</text>
  <text x="496" y="324" fill="#cbd5e1" font-size="11.5">지우기 1 + 넣기 1</text>

  <!-- 범례 -->
  <rect x="176" y="370" width="10" height="10" fill="none" stroke="#fbbf24" stroke-width="1.6"/>
  <text x="192" y="379" fill="#94a3b8" font-size="11">바꾸기</text>
  <rect x="256" y="370" width="10" height="10" fill="none" stroke="#93c5fd" stroke-width="1.6"/>
  <text x="272" y="379" fill="#94a3b8" font-size="11">넣기</text>
  <rect x="326" y="370" width="10" height="10" fill="none" stroke="#f87171" stroke-width="1.6"/>
  <text x="342" y="379" fill="#94a3b8" font-size="11">지우기</text>
  <rect x="406" y="370" width="10" height="10" fill="none" stroke="#475569" stroke-width="1.6"/>
  <text x="422" y="379" fill="#94a3b8" font-size="11">맞추기</text>

  <text x="340" y="398" text-anchor="middle" fill="#64748b" font-size="10.5">S₁ = abcab · S₂ = abcba · 세 정렬 모두 비용 2</text>
</svg>
```

- [ ] **Step 4: 팔레트 밖 색이 없는지 확인한다**

Run:
```bash
grep -ohE '#[0-9a-fA-F]{3,8}' public/images/edit-distance-traceback/*.svg | sort -u
```
Expected: `#0f1117 #1e293b #475569 #4ade80 #64748b #6ee7b7 #93c5fd #94a3b8 #a78bfa #cbd5e1 #e2e8f0 #f87171 #fbbf24` 의 부분집합.

- [ ] **Step 5: SVG가 well-formed인지 확인한다**

Run:
```bash
python -c "from xml.dom import minidom; import glob; [minidom.parse(p) for p in glob.glob('public/images/edit-distance*/*.svg')]; print('ok')"
```
Expected: `ok`. 리뷰 스크립트의 자산 검사가 같은 파서를 쓴다.

- [ ] **Step 6: 커밋**

```bash
git add public/images/edit-distance-traceback
git commit -m "feat(edit-distance): 되짚기와 영역 도판 세 장을 그린다"
```

---

### Task 4: 추가 설명 본문

**Files:**
- Create: `src/content/posts/edit-distance-traceback.md`
- Test: `npm run build`, `python .claude/review_post.py src/content/posts/edit-distance-traceback.md`

**Interfaces:**
- Consumes: Task 2가 정한 기호 규약($S_1$, $S_2$, $D(i, j)$, $t(i, j)$, 정렬, 격자 경로)과 라우트 `/blog/edit-distance`. Task 3의 세 SVG.
- Produces: 라우트 `/blog/edit-distance-traceback`. 본편이 이 경로를 두 곳에서 참조한다(격자 대응 절, 이어지는 글 callout).

- [ ] **Step 1: 파일을 아래 내용 그대로 만든다**

````markdown
---
title: "추가 설명 — 되짚기는 길 하나가 아니라 영역을 준다"
date: 2026-08-26T10:00:00
description: "편집 거리의 표는 최솟값만 담는다. 표를 거꾸로 읽어 연산을 복원하면 최선의 길이 여럿일 수 있고, 그래서 결과는 길 하나가 아니라 표 위의 영역이 된다."
tags: ["Algorithm", "Edit Distance", "Traceback", "Dynamic Programming", "추가 설명"]
category: algorithm
difficulty: 고급
numbered: true
---

> [편집 거리](/blog/edit-distance)의 표는 마지막 칸에 수 하나를 남긴다. 두 번 고치면 된다는 사실은 알려 주지만 무엇을 어떻게 고치는지는 말하지 않는다. 되짚어 보면 답이 하나가 아닐 수도 있다는 사실까지 드러난다.

<div class="callout">
<div class="callout-title">이 글에서 다루는 내용</div>

- 표가 담는 것은 **값**이고, 어떤 연산을 썼는지는 별개다
- 칸마다 어느 이웃에서 왔는지 되묻는 **되짚기** 규칙
- `abcab` 와 `abcba` 의 최적 정렬이 셋이라는 것을 직접 세기
- 최적 경로 전체가 표 위에 만드는 **영역**의 정확한 뜻
- 경로 개수를 세는 표, 그리고 그 수가 지수로 커지는 예

</div>

---

## 값과 연산은 다르다

본편의 표는 칸마다 최솟값 하나를 적었다. 그 최솟값이 어떤 정렬에서 나왔는지는 적지 않았다. 값을 구하는 데 필요하지 않았기 때문이다.

**되짚기**(traceback)는 채운 표를 거꾸로 읽어 그 정렬을 복원한다. 채울 때는 세 이웃 중 최솟값을 골랐으니, 되짚을 때는 그 최솟값을 이룬 이웃이 누구였는지 되묻는다.

---

## 거꾸로 읽는 규칙

칸 $(i, j)$ 에서 다음 세 등식을 검사한다.

- $D(i, j) = D(i-1, j-1) + t(i, j)$ 이면 대각선에서 왔다. $t(i, j) = 0$ 이면 맞추기, 1이면 바꾸기다
- $D(i, j) = D(i-1, j) + 1$ 이면 위에서 왔다. $S_1[i]$ 를 지우는 연산이다
- $D(i, j) = D(i, j-1) + 1$ 이면 왼쪽에서 왔다. $S_2[j]$ 를 넣는 연산이다

$i = 0$ 이면 왼쪽으로만, $j = 0$ 이면 위로만 갈 수 있다. $(0, 0)$ 에 닿으면 끝이고, 거꾸로 모은 연산을 뒤집으면 정렬이 된다.

예시를 바꾸자. $S_1 = $ `abcab`, $S_2 = $ `abcba` 이고 편집 거리는 2다.

![abcab와 abcba의 표에서 (5,5)부터 대각선을 따라 (0,0)까지 되짚어 올라가는 경로](/images/edit-distance-traceback/traceback-path.svg)

$(5, 5)$ 에서 시작한다. 값은 2다. 대각선 이웃 $(4, 4)$ 는 1이고 `b` 와 `a` 가 다르므로 $1 + 1 = 2$ 로 등식이 성립한다. 대각선을 따라 $(4, 4)$ 로 간다. 여기서도 `a` 와 `b` 가 달라 바꾸기 한 번이다. $(3, 3)$ 부터는 `abc` 가 그대로 맞으므로 대각선을 세 번 더 타고 $(0, 0)$ 에 닿는다. 복원한 정렬은 바꾸기 두 번이다.

---

## 동점이면 갈래가 갈린다

$(5, 5)$ 에서 성립한 등식은 대각선 하나가 아니었다. 위 이웃 $(4, 5)$ 도 1이라 $1 + 1 = 2$ 이고, 왼쪽 이웃 $(5, 4)$ 도 1이라 $1 + 1 = 2$ 다. 세 등식이 모두 성립한다. 되짚기는 어느 쪽으로도 갈 수 있고, 어느 쪽을 골라도 비용 2인 정렬이 나온다.

세 갈래를 끝까지 따라가면 정렬이 셋이다.

![abcab와 abcba의 최적 정렬 세 개. 첫째는 바꾸기 두 번, 둘째는 넣기와 지우기, 셋째는 지우기와 넣기로 이루어진다.](/images/edit-distance-traceback/alignments.svg)

- **정렬 1**: `abc` 를 맞추고 `a` 를 `b` 로, `b` 를 `a` 로 두 번 바꾼다
- **정렬 2**: `abc` 를 맞추고 `b` 를 넣은 뒤 `a` 를 맞추고 마지막 `b` 를 지운다
- **정렬 3**: `abc` 를 맞추고 `a` 를 지운 뒤 `b` 를 맞추고 `a` 를 넣는다

셋 다 비용 2다. 편집 거리는 이 셋을 구별하지 않는다.

---

## 그래서 영역이다

최적 정렬이 여럿이면 되짚기의 결과를 길 하나로 적을 수 없다. 최적 경로 전체를 겹쳐 놓으면 남는 것은 칸의 집합이다.

<div class="callout callout-key">
<div class="callout-title">영역의 정의</div>

최적 경로 하나 이상이 지나는 칸을 모두 모은 것

</div>

`abcab` 와 `abcba` 의 영역은 공통 접두사 `abc` 를 따라가는 대각선과, $(3, 3)$ 에서 벌어져 $(5, 5)$ 에서 다시 모이는 마름모다.

![세 최적 경로를 색으로 구분해 겹쳐 그리고, 그 경로들이 지나는 칸을 파선으로 표시한 그림](/images/edit-distance-traceback/region.svg)

영역의 모양이 정보를 준다. 대각선 한 줄로 좁으면 최적 정렬이 사실상 하나이고 어느 글자를 어디에 맞출지 여지가 없다. 넓게 벌어지면 같은 비용의 정렬이 여럿이며, 그중 무엇을 고를지는 편집 거리가 정해 주지 않는다.

한 가지는 조심해야 한다. 영역은 최적 경로들의 합집합일 뿐, 영역 안을 아무렇게나 걸어도 최적이라는 뜻이 아니다. 위 그림에서 $(3, 4)$ 와 $(4, 3)$ 은 둘 다 영역 안이지만 두 칸을 함께 지나는 경로는 없다. 경로는 오른쪽과 아래로만 움직이므로 $(3, 4)$ 를 지난 뒤에는 열 번호가 4보다 작은 칸으로 갈 수 없다.

<div class="callout callout-simple">
<div class="callout-title">영역을 구하는 값싼 방법</div>

칸 하나가 영역에 드는지 판정하려면 그 칸을 지나는 최적 경로가 있는지 물으면 된다. 채워 둔 표 $D$ 는 $(0, 0)$ 에서 $(i, j)$ 까지의 최소 비용이다. 두 문자열을 각각 뒤집어 같은 표를 한 번 더 채우면 $(i, j)$ 에서 $(n, m)$ 까지의 최소 비용 $D'(i, j)$ 를 얻는다. $(i, j)$ 를 지나는 경로의 최소 비용이 $D(i, j) + D'(i, j)$ 이므로, 칸이 영역에 드는 조건은 $D(i, j) + D'(i, j) = D(n, m)$ 이다. 표 두 개를 채우는 비용이라 여전히 $O(NM)$ 이다.

</div>

---

## 경로가 몇 개인지 세기

경로를 일일이 따라가지 않고도 개수를 셀 수 있다. 표를 한 번 더 채우면 된다.

$C(i, j)$ 를 $(0, 0)$ 에서 $(i, j)$ 까지 가는 최적 경로의 개수라 하자. $C(0, 0) = 1$ 이고, 나머지 칸에서는 되짚기 등식이 성립하는 이웃의 $C$ 를 더한다.

```cpp
// D는 본편의 방식으로 이미 채워져 있다고 가정한다
long long countOptimalPaths(const string& s1, const string& s2,
                            const vector<vector<int>>& D) {
    int n = s1.size(), m = s2.size();
    vector<vector<long long>> C(n + 1, vector<long long>(m + 1, 0));
    C[0][0] = 1;

    for (int i = 0; i <= n; i++)
        for (int j = 0; j <= m; j++) {
            if (i == 0 && j == 0) continue;
            long long c = 0;
            if (i && j) {
                int t = (s1[i-1] == s2[j-1]) ? 0 : 1;
                if (D[i][j] == D[i-1][j-1] + t) c += C[i-1][j-1];
            }
            if (i && D[i][j] == D[i-1][j] + 1) c += C[i-1][j];
            if (j && D[i][j] == D[i][j-1] + 1) c += C[i][j-1];
            C[i][j] = c;
        }
    return C[n][m];
}
```

`abcab` 와 `abcba` 에 돌리면 3이 나온다. 본편의 예시 `abcabcd` 와 `abcdabc` 에 돌리면 1이다. 편집 거리는 양쪽 모두 2인데 한쪽은 정렬이 셋이고 다른 쪽은 하나다.

개수는 아주 빨리 커진다. `aaaa` 와 `aa` 를 보자. 편집 거리는 2이고, 네 개의 `a` 중 어느 둘을 지워도 비용이 2다. 경로는 $\binom{4}{2} = 6$ 개다. 일반적으로 `a` 를 $2k$ 개 늘어놓은 문자열과 $k$ 개 늘어놓은 문자열 사이의 최적 경로는 $\binom{2k}{k}$ 개이고, 이 값은 $k$ 에 대해 지수로 늘어난다.

이 사실이 결과를 영역으로 적는 이유를 설명한다. 최적 정렬을 전부 나열하려면 출력 자체가 지수 크기일 수 있다. 영역은 표의 칸을 넘지 않으므로 언제나 $(n+1)(m+1)$ 안에 담긴다.

---

## 어느 정렬을 고를 것인가

되짚기 코드에서 세 등식을 검사하는 순서가 그대로 정책이 된다. 대각선을 먼저 검사하면 빈 칸을 되도록 늦게 만들고, 위쪽을 먼저 검사하면 지우기를 앞으로 몰아 놓는다. 비용은 어느 쪽이든 같으므로 알고리즘은 아무 말도 해 주지 않는다.

선택은 응용이 한다. 유전자 서열 정렬에서는 빈 칸이 흩어지기보다 한군데 뭉치는 편이 그럴듯하므로, 빈 칸을 여는 비용과 늘리는 비용을 따로 두는 모델을 쓴다. 오타 교정에서는 본편의 가중 편집 거리처럼 자판 거리를 비용에 반영한다. 두 경우의 공통점은 정렬을 고르는 기준을 비용 함수 안으로 들여온다는 것이다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

표는 값을 담고, 되짚기는 그 값을 낸 연산을 복원한다. 동점이 있으면 최적 정렬이 여럿이므로 결과는 길 하나가 아니라 최적 경로가 지나는 칸의 집합, 곧 영역이다. 경로의 개수는 지수로 커질 수 있지만 영역은 표 크기 안에 담긴다.

</div>

<div class="callout">
<div class="callout-title">돌아가는 글</div>

편집 거리의 정의와 점화식, 표를 채우는 방법과 $O(NM)$ 의 정확한 의미는 [편집 거리 — 비슷하다는 말을 수로 바꾸기](/blog/edit-distance)에 있다.

</div>

---

## 마치며

표를 채우는 일과 되짚는 일은 방향만 다르다. 채울 때는 세 이웃에서 최선을 골랐고, 되짚을 때는 그 최선이 누구였는지 물었다. 물음의 답이 하나가 아닐 수 있다는 것, 그래서 결과가 길 하나가 아니라 영역이 된다는 것이 되짚기가 값 계산과 갈리는 지점이다.
````

- [ ] **Step 2: 결정적 검사를 돌린다**

Run: `python .claude/review_post.py src/content/posts/edit-distance-traceback.md`
Expected: `발견 사항 없음 ✅`

- [ ] **Step 3: 빌드로 확인한다**

Run: `npm run build`
Expected: 오류 없이 완료. 두 편의 상호 링크가 실제 라우트를 가리키는지도 이 시점에 확인된다.

- [ ] **Step 4: 커밋**

```bash
git add src/content/posts/edit-distance-traceback.md
git commit -m "feat(edit-distance): 되짚기와 영역을 다루는 추가 설명을 쓴다"
```

---

### Task 5: 검증과 리뷰 반영

**Files:**
- Create: `docs/reviews/2026-08-26-edit-distance.md`
- Modify: `src/content/posts/edit-distance.md`, `src/content/posts/edit-distance-traceback.md` (리뷰 지적 반영 시)

**Interfaces:**
- Consumes: Task 1~4의 산출물 전체
- Produces: 리뷰 리포트. PR 본문이 이 파일을 근거로 참조한다.

- [ ] **Step 1: 두 편의 결정적 검사를 한꺼번에 돌린다**

Run: `python .claude/review_post.py src/content/posts/edit-distance.md src/content/posts/edit-distance-traceback.md`
Expected: 두 파일 모두 `발견 사항 없음 ✅`

- [ ] **Step 2: 전체 테스트와 빌드**

Run: `npm test`
Expected: 전부 통과.

Run: `npm run build`
Expected: 오류 없이 완료.

- [ ] **Step 3: `/review-post` 로 L1~L7 비평을 받아 리포트를 쓴다**

`/review-post edit-distance` 와 `/review-post edit-distance-traceback` 을 돌리고 결과를 `docs/reviews/2026-08-26-edit-distance.md` 한 파일에 모은다. L7(논증·복잡도)에서 반드시 다시 확인할 항목은 다음과 같다.

- `abcabcd`/`abcdabc` 표의 64개 값과 답 2, 그리고 `D(2,4)=2`·`D(5,1)=4`
- `abcab`/`abcba` 표의 36개 값, 최적 정렬 3개, 영역 칸 10개
- $\binom{2k}{k}$ 주장: `aaaa`/`aa` 의 경로 6개
- `abcdef`/`defabc` 의 편집 거리 6
- 정리 1 증명의 양방향과 경우 분할이 전체를 덮는지
- 하한 서술이 "무조건 불가"로 읽히지 않는지

- [ ] **Step 4: 지적을 반영하고 재검증한다**

반영 후 Run: `python .claude/review_post.py src/content/posts/edit-distance.md src/content/posts/edit-distance-traceback.md`
Expected: `발견 사항 없음 ✅`

Run: `npm run build`
Expected: 오류 없이 완료.

리포트 끝에 「반영 결과」 절을 추가해 무엇을 고쳤는지 적는다.

- [ ] **Step 5: 커밋**

```bash
git add docs/reviews/2026-08-26-edit-distance.md src/content/posts
git commit -m "docs(review): 편집 거리 두 편의 리뷰 리포트와 반영 결과를 기록한다"
```

- [ ] **Step 6: PR을 연다**

```bash
git push -u origin feat/post-edit-distance
```

PR 제목: `feat(edit-distance): 편집 거리와 되짚기 두 편을 쓴다`

본문 구성:
- **Why**: 거리 함수를 정의하지 않으면 근사 문자열 매칭이 시작되지 않는다는 문제, 자리 고정 비교가 무너지는 지점, 점화식이 왜 그렇게 생겼는지를 서술로 때우지 않고 논증으로 닫아야 하는 이유, "O(NM)보다 빠를 수 없다"를 조건 없이 옮기면 독자가 잘못 배운다는 위험까지 길게 쓴다.
- **How**: 방법론 중심으로 쓴다. 파일 경로나 `file:line` 을 쓰지 않는다. 실패의 사슬로 거리 함수를 엮은 구성, 최적 정렬의 마지막 열로 경우를 분할해 점화식을 유도한 방식, 값과 구성을 두 편으로 나눈 경계, 조건부 하한으로 주장의 강도를 낮춘 판단, 예시를 계산으로 검증한 절차를 적는다.
- **참조 코드 위치**: 본편·추가 설명·도판·리뷰 리포트 경로를 여기에만 모아 적는다.
- 마지막 줄: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

---

## Self-Review

**스펙 커버리지.** 스펙의 각 절이 어느 과제로 들어갔는지 확인했다.

| 스펙 항목 | 구현 위치 |
|---|---|
| 원문 줄기 1~8 | Task 2 본문 전체 (거리 함수 → 부분 문제 → 점화식 → 표 → 비용), Task 4 (되짚기·영역) |
| 정정 1 (Hamming 예시) | Task 2 「자리끼리 맞추기」 절과 `align-shift.svg` |
| 정정 2 (하한) | Task 2 「이보다 빠를 수 없다는 말」 절 + 참고 문헌 callout |
| 정정 3 (3번 재사용) | Task 2 「비용」 절의 내부 칸 조건 |
| 정정 4 (재귀 지수) | Task 2 「비용」 절의 $3^{n+m}$ |
| 정정 5 (예시 값 보강) | Task 2 「부분 문제」·「표 채우기」 절, `table.svg` |
| 원문 요청 1 (점화식 상세) | Task 2 정리 1과 증명 |
| 원문 요청 2 (순환처럼 보임) | Task 2 「답이 연산의 열이라는 관점」 절 |
| 원문 요청 3 (하한 참고 자료) | Task 2 참고 문헌 callout |
| 원문 요청 4 (영역) | Task 4 「그래서 영역이다」 절과 `region.svg` |
| 확장: 두 행 공간 | Task 2 코드 두 번째 블록 |
| 확장: 경로 개수 세기 | Task 4 `countOptimalPaths` |
| 도판 7장 | Task 1, Task 3 |
| 기술 검증 | Task 2·4의 검사 단계, Task 5 |

**플레이스홀더 점검.** 본문·SVG·코드가 모두 완전한 형태로 들어가 있고 `TBD`·`나중에`·`비슷하게` 류의 지시가 없다. 확인했다.

**기호 일관성.** 본문 기호는 $S_1$, $S_2$, $n$, $m$, $D(i, j)$, $t(i, j)$, $D'(i, j)$, $C(i, j)$ 이고 두 편에서 같은 뜻으로 쓴다. 코드 이름은 `editDistance`, `editDistanceTwoRows`, `countOptimalPaths` 세 개이며 겹치거나 갈리는 이름이 없다. SVG의 격자 좌표 규약(칸 54×34, 원점 (170, 112))은 `traceback-path.svg` 와 `region.svg` 가 공유한다.

**스펙과 달라진 점.** 스펙의 `description` 초안이 세 문장이었는데 결정적 검사의 220자 상한과 두 문장 관례에 맞춰 줄였다. 내용은 같다.

