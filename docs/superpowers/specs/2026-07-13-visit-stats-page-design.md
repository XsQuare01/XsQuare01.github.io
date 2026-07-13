# 방문 통계 페이지 `/stats` (설계)

- 날짜: 2026-07-13
- 상태: 승인됨 (grilling + 계획 리뷰 v2 반영)
- 선행: `2026-07-13-visit-counter-design.md`(Vercount 누적 카운터). 본 문서는 그 위에 통계 페이지를 얹고, 사이드바/푸터 표시를 재정리한다.
- 관련 이슈: #33 (B 확장 — 인기 글 top 5)

## 목표

사이드바의 **"통계" 탭**을 누르면 열리는 전용 페이지 `/stats`에서, **최근 30일 일별 방문자** 그래프와 **최근 30일 순 방문자 수**를 보여준다. 데이터는 이미 설치된 **GA4**에서 빌드 시 받아 온다.

## 데이터 계약 (핵심 — 리뷰 반영)

### 파일 경로
- **단일 경로: `src/data/visit-stats.json`**. Astro가 빌드 시 import해 페이지에 임베드한다(런타임 fetch 없음). `public/`이 아니라 `src/data/`로 통일한다.

### 스키마
```json
{
  "source": "GA4" | "sample",
  "sample": true,            // 샘플/미연결 상태일 때만 true (실데이터엔 없음/false)
  "rangeDays": 30,
  "generatedAt": "<ISO>" | null,
  "daily": [{ "date": "YYYY-MM-DD", "visitors": <number> }],
  "total": <number>          // 아래 '합계 의미' 참고
}
```

### 합계 의미 (리뷰 지적 — 반드시 준수)
- **`daily[].visitors`**: 그 날짜의 `activeUsers`(일별 순 방문자).
- **`total`**: **일별 값의 단순 합이 아니다.** 일별 합은 여러 날 방문한 사람을 중복 계산한 "연인원"이라 순 방문자가 아니다. `total`은 **기간 전체(30일)에 대해 date 차원 없이 조회한 `activeUsers`** — 즉 30일 동안의 **중복 제거된 순 방문자 수**다. → fetch 스크립트가 **별도 쿼리 2개**(일별용 + 기간 전체용)를 돌린다.
- 화면 문구도 "합계"가 아니라 **"최근 30일 순 방문자 N명"** 으로 표기한다.

### 30일 범위 (리뷰 지적)
- `startDate: '30daysAgo'`, `endDate: 'yesterday'`. **부분 집계된 오늘(today)은 제외**해 30일 완전한 날짜만 쓴다. `rangeDays`는 30으로 고정, 라벨과 일치시킨다.

### 갱신 시각 표기 (리뷰 지적)
- `generatedAt`을 화면에 **"마지막 갱신: YYYY-MM-DD HH:mm"** 로 표시해 데이터 신선도를 드러낸다. `null`이면 "—".

## 데이터 파이프라인

- **출처/지표/기간**: GA4(측정 ID `G-35YPC8K6Y2`), 지표 `activeUsers`, 기간 30일(위 계약).
- **인증**: 서비스 계정 키 + GitHub Secret(`GA_SERVICE_ACCOUNT_KEY`), 속성 ID `GA_PROPERTY_ID`. 서비스 계정은 GA4 속성에 **뷰어(최소 권한)**.
- **빌드 시 fetch**: CI에서 `scripts/fetch-ga-stats.mjs`가 위 2개 쿼리로 `src/data/visit-stats.json`을 실데이터로 덮어쓴다.
- **갱신 주기**: 매일 예약(cron) + 배포 시.
- **실패/미연결 fallback (리뷰 지적 — 정직한 계약)**:
  - 저장소에 커밋되는 기본 `src/data/visit-stats.json`은 **`"sample": true`인 샘플**이다.
  - fetch가 **성공**하면 실데이터(`source:"GA4"`, `sample` 없음)로 덮어쓴다.
  - fetch가 **인증정보 없음/요청 실패**면 **비치명적**으로 스킵(exit 0) → 커밋된 샘플이 남는다.
  - 이때 `/stats`는 데이터를 그리되 **"샘플 데이터 (GA 연결 전/갱신 실패)" 배너**를 눈에 띄게 표시한다. → **가짜 숫자를 실데이터처럼 보이게 하지 않는다.**
  - `daily`가 **빈 배열**이면 그래프 대신 **"통계를 불러올 수 없습니다"** 로 degrade.

## 화면

- **사이드바**: 앞서 넣은 숫자 두 줄 블록 **제거**. 메뉴 아래에 **"통계" 탭**(`/stats`) 추가.
- **푸터**: Vercount 누적 방문자 유지. 사이드바 canonical이 사라지므로 **푸터를 canonical `vercount_value_site_uv`로 되돌리고 미러 스크립트 제거**.
- **`/stats` 페이지**:
  - 상단: **"최근 30일 순 방문자 N명"**(= `total`), "GA4 · 최근 30일" 출처 라벨, **"마지막 갱신: …"**, 샘플이면 배너.
  - **제목·총계·라벨·배너·마지막 갱신은 서버 렌더(SSR)** — JS가 막혀도 숫자와 문구는 보인다(그래프만 빈 캔버스).
  - 그래프: Chart.js **꺾은선**(일별 방문자). 데이터 없음 → 안내 문구.
  - 다크/라이트 전환 시 그래프 색이 따라오도록, `documentElement`의 `.light` 클래스 변화를 감지해 차트 색을 갱신한다.
  - 클라이언트 스크립트는 `#stats-data`(JSON) 파싱을 **try/catch**로 방어(잘못된 데이터에도 페이지가 죽지 않음).

## 차트

- **Chart.js를 npm 의존성으로 설치**, `/stats` 클라이언트 스크립트에서만 import → 그 페이지 청크에만 번들. **다른 페이지 HTML은 이 청크를 로드하지 않는다.**

## 컴포넌트 경계

- `scripts/fetch-ga-stats.mjs` — CI 전용. GA4 2쿼리 → `src/data/visit-stats.json`. 실패 비치명적. devDep `@google-analytics/data`.
- `.github/workflows/deploy.yml` — build 전에 fetch 단계 + `schedule`(cron). Secret 주입.
- `src/pages/stats.astro` — `/stats`. `src/data/visit-stats.json` import → SSR 총계/라벨/배너 + Chart.js 렌더. 데이터 유무·샘플 분기.
- `src/layouts/BaseLayout.astro` — 사이드바 두 줄 제거 + "통계" 탭, 푸터 canonical 복귀(미러 제거).
- `src/data/visit-stats.json` — 샘플(`sample:true`) 커밋. CI 성공 시 실데이터로 덮어씀.

## 검증 시나리오 (happy path 외 — 리뷰 반영)

구현 후 아래를 모두 확인한다(가능한 한 **크로스플랫폼 Node 검사**로. `grep/sort/uniq/wc`는 PowerShell에서 보장 안 되므로 `node -e` 또는 Grep 도구 사용):

1. **빈 daily** → "통계를 불러올 수 없습니다" degrade, 레이아웃 유지.
2. **잘못된 스키마/파싱 실패** → 페이지가 죽지 않고 degrade(클라이언트 try/catch, SSR 가드).
3. **GA 인증정보 없음** → fetch 스킵(exit 0), 샘플 유지 + 샘플 배너.
4. **GA 요청 실패** → fetch 스킵(exit 0), 기존 파일 유지 + 샘플/이전 데이터.
5. **방문자 0인 날짜** → y축 0부터, 0 값 정상 렌더.
6. **Chart.js 실행 차단(JS off)** → SSR 총계·라벨·마지막 갱신·배너 표시, 캔버스만 빈 채로 레이아웃 유지.
7. **모바일 너비** → 차트/사이드바 탭 안 깨짐(반응형).
8. **다크/라이트 전환** → 차트 색이 테마 따라 갱신.
9. **청크 격리** → `dist/index.html`(및 블로그 페이지)은 Chart.js 청크 스크립트를 로드하지 않고, `dist/stats/index.html`만 로드.

## 사용자 1회성 작업 (코드 외)

1. GA4 숫자 속성 ID 확인.
2. GCP 서비스 계정 생성 + GA4 Data API 사용 설정 + JSON 키 발급.
3. 서비스 계정을 GA4 속성에 **뷰어**로 추가.
4. GitHub Secret `GA_SERVICE_ACCOUNT_KEY`(키 JSON 전체), `GA_PROPERTY_ID`(숫자) 등록.

## 확장 (구현됨)

- **유입 경로(구체적 소스)**: fetch에 GA 쿼리 1개 추가 — 차원 `sessionSource`, 지표 `activeUsers`, 최근 30일 상위 8. JSON에 `sources:[{source,visitors}]` 추가. `/stats`에 "유입 경로" 섹션(소스명 + CSS 비율 막대 + 방문자 수, 순수 SSR). 데이터 없으면 섹션 숨김. (2026-07-13 추가)

## 확장 포인트 (이번 범위 밖 — 이슈 #33)

- **B: 인기 글 top 5 막대차트**. fetch에 GA 호출 1개(`topPosts`) 추가, `/stats`에 막대차트 블록 추가(Chart.js 재사용). 출처·인증·갱신은 A와 동일.

## 작업 절차 / 제약

- 브랜치 `feat/visit-counter`에서 이어 작업. main 직접 커밋 금지. 커밋 메시지는 **저장소 커밋 정책을 따른다**(플랜 문서에 특정 co-author를 고정하지 않는다).
- Secret 없이도 구현·검증(샘플로 렌더, fetch 스킵). 실제 GA 연결은 사용자 설정 후 배포에서 확인.

## 성공 기준 (검증 가능)

1. `npm run build` 성공, `/stats` 생성.
2. 샘플 데이터로 꺾은선·"최근 30일 순 방문자"·출처 라벨·마지막 갱신·**샘플 배너**가 렌더.
3. 사이드바 "통계" 탭이 `/stats`로 이동, 숫자 두 줄 블록은 제거됨.
4. 푸터 Vercount 누적이 canonical(`vercount_value_site_uv`) 단독(미러 없음, id 중복 없음).
5. 위 "검증 시나리오" 1~9 통과.
6. Chart.js 청크가 `/stats`에서만 로드.
7. (배포 후 운영) 사용자 GA 설정 완료 시 실데이터로 `total`(30일 순 방문자)·`daily`가 채워지고 샘플 배너가 사라진다.
