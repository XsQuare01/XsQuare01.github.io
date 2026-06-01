# Homepage Positioning Alignment (A안)

**Date:** 2026-05-21
**Status:** Approved

## Summary

홈 화면 카피·태그를 실제 글 콘텐츠(계산 이론·암호학·알고리즘)와 일치시킨다. 기존 Unity/C#/UI 설계 강조 문구는 실제 글 28편 중 거의 0편과 매칭되어 정체성 불일치를 만들고 있었다. 헤드라인은 유지하고 설명 문구와 태그 영역만 정렬한다.

---

## Decisions

| # | 항목 | 결정 |
|---|---|---|
| 1 | 헤드라인 | "배운 것을 정리하는 개발자" **유지** (능동형 후보도 검토했으나 기본안 선택) |
| 2 | 설명 문구 | **학자 톤** 채택: "계산 이론·암호학·알고리즘을 풀어 쓰며 정리하는 노트입니다. / 정답보다 이해의 과정을 우선합니다." |
| 3 | 태그 구성 | accent 3개(계산 이론·암호학·알고리즘) + 일반 3개(정수론·복잡도·자료구조). TypeScript는 빌드 도구라 글 주제와 어색해 제외 |
| 4 | 0건 카테고리 | `categories.ts`의 `unity`, `web-dev`는 **건드리지 않음** (0건이라 자동 필터됨) |
| 5 | BaseLayout 기본 description | OG/SEO fallback도 정체성과 일치하도록 갱신 |

---

## Changes

### `src/pages/index.astro`

**설명 문구 교체 (36–38행):**

```diff
- Unity 클라이언트 개발, CS 이론, UI/UX 구현 과정을 기록합니다.<br />
- 결과보다 과정과 이유를 남기는 것을 중요하게 생각합니다.
+ 계산 이론·암호학·알고리즘을 풀어 쓰며 정리하는 노트입니다.<br />
+ 정답보다 이해의 과정을 우선합니다.
```

**태그 목록 교체 (42–48행):**

```diff
- <span class="tag tag--accent">Unity</span>
- <span class="tag tag--accent">C#</span>
- <span class="tag tag--accent">UI 설계</span>
- <span class="tag">TypeScript</span>
- <span class="tag">C++</span>
- <span class="tag">알고리즘</span>
- <span class="tag">CS 이론</span>
+ <span class="tag tag--accent">계산 이론</span>
+ <span class="tag tag--accent">암호학</span>
+ <span class="tag tag--accent">알고리즘</span>
+ <span class="tag">정수론</span>
+ <span class="tag">복잡도</span>
+ <span class="tag">자료구조</span>
```

**유지:** 헤드라인, featured 글(rsa, algo-orientation), 카테고리 탭 로직, 최근 글 피드, 바 차트, 모든 CSS.

### `src/layouts/BaseLayout.astro`

**기본 description 갱신 (14행):**

```diff
- description = 'XsQuare01의 기술 블로그',
+ description = '계산 이론·암호학·알고리즘을 정리하는 학습 노트 — XsQuare01',
```

페이지가 description을 명시하지 않을 때 사용되는 OG/Twitter 메타 fallback이라 정체성과 정렬한다. 사이드바 bio "정리하고 기록하는 개발자"(118행)는 이미 중립적이라 유지.

### `src/data/categories.ts`

**변경 없음.** `unity`·`web-dev`는 글 0건이라 `index.astro:20`과 `BaseLayout.astro:36`에서 자동 필터되므로 사용자 노출은 없음. 향후 해당 분야 글을 쓸 가능성을 닫지 않기 위해 코드에 남겨둔다.

---

## Out of Scope

다음은 의도적으로 이 spec에 포함하지 않는다:

- **Start Here / 학습 경로 페이지** — 별도 spec에서 다룬다 (초기 평가에서 제안한 2순위 작업)
- **글 상단 prerequisite 박스** — 별도 spec에서 다룬다 (3순위)
- **수식 접근성 / 출처 보강** — 글 단위 작업이라 별도 (4순위)
- **추천 글 변경** — 최근 커밋(`b06eb2f`)에서 사용자가 직접 정한 값이라 존중
- **`alice-bob.md`, `before-physics.md` 등 카테고리 분류** — 콘텐츠 작업이라 범위 밖

---

## Verification

1. `npm run dev`로 로컬 서버 띄우기
2. **홈 화면**:
   - 헤드라인이 그대로인지 (`배운 것을 정리하는 개발자`)
   - 설명 두 줄이 학자 톤으로 교체됐는지
   - accent 태그 3개가 계산 이론·암호학·알고리즘인지
   - 일반 태그 3개가 정수론·복잡도·자료구조인지
3. **다크/라이트 모드** 전환 시 accent 강조가 양쪽 다 자연스러운지
4. **모바일 뷰포트 (480px 이하)**: 태그 줄바꿈, 헤드라인 폰트 사이즈
5. **메타 description 확인**: 홈(`/`)은 `index.astro:28`에서 `<BaseLayout title="홈">`만 호출해 description prop을 안 넘기므로 새 BaseLayout fallback이 그대로 노출되는지 확인. 다른 페이지(`/blog` 등)도 마찬가지로 fallback 사용 시 새 문구가 보이는지 페이지 소스에서 `<meta name="description">`와 `<meta property="og:description">` 양쪽 확인

---

## Brainstorming History

Visual companion으로 v1·v2를 거치며 결정. 주요 흐름:

1. v1 (Before/After 2분할) → 사용자: "좀 더 다듬어줘"
2. v2: 헤드라인 후보 3개 + 설명 후보 4개 + 풀 페이지 미리보기 + 실시간 갱신 스크립트
3. 사용자 클릭 이력: 설명은 학자→미니멀→솔직→**학자** (회귀), 헤드라인은 능동형→**기본** (회귀). 두 항목 모두 변형을 검토 후 원안 또는 한 단계만 다듬은 안으로 수렴.

세션 디렉토리: `.superpowers/brainstorm/966-1779336476/` (gitignore됨)
