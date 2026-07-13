# 방문 통계 페이지 `/stats` (설계)

- 날짜: 2026-07-13
- 상태: 승인됨 (grilling으로 설계 확정)
- 선행: `2026-07-13-visit-counter-design.md`(Vercount 누적 카운터). 본 문서는 그 위에 통계 페이지를 얹고, 사이드바/푸터 표시를 재정리한다.
- 관련 이슈: #33 (B 확장 — 인기 글 top 5)

## 목표

사이드바의 **"통계" 탭**을 누르면 열리는 전용 페이지 `/stats`에서, **최근 30일 일별 방문자** 그래프와 **30일 방문자 합계**를 보여준다. 데이터는 이미 설치된 **GA4**에서 빌드 시 받아 온다.

## 확정된 설계 (grilling)

### 데이터 파이프라인
- **출처**: 기존 GA4(측정 ID `G-35YPC8K6Y2`). 지표는 **일별 `activeUsers`(순 방문자)**, 기간 **최근 30일**.
- **인증**: **서비스 계정 키 + GitHub Secret**(`GA_SERVICE_ACCOUNT_KEY`). 서비스 계정을 GA4 속성에 **뷰어(최소 권한)** 로 추가. GA4 **숫자 속성 ID**는 Secret 또는 워크플로 env(`GA_PROPERTY_ID`)로 주입. (초기 미확정 시 자리표시자 `GA4_PROPERTY_ID_TBD`)
- **빌드 시 fetch**: CI에서 Node 스크립트가 GA4 Data API를 호출해 `public/visit-stats.json`을 생성.
  - JSON 형태: `{ "source": "GA4", "rangeDays": 30, "generatedAt": "<ISO>", "daily": [{ "date": "2026-06-14", "visitors": 12 }, ...], "total": 320 }`
- **갱신 주기**: **매일 예약(cron) + 배포 시**. 워크플로에 `schedule`(하루 1회) 추가.
- **실패 처리(비치명적)**: GA 호출 실패해도 빌드/배포는 계속. 직전에 커밋된 샘플/이전 JSON을 유지. 데이터가 비면 페이지가 안내 문구로 degrade.
- **로컬/샘플**: 저장소에 샘플 `public/visit-stats.json`(소량 더미)을 커밋 → 로컬 `npm run dev`와 CI 실패 시에도 페이지가 렌더된다.

### 화면
- **사이드바**: 앞서 넣은 **숫자 두 줄 블록(총 방문자/총 방문수)은 제거**한다. 대신 메뉴(홈·글 목록·카테고리·태그) 아래에 **"통계" 탭**(`/stats` 링크)을 추가한다.
- **푸터**: Vercount 누적 방문자(`· 방문자 N명`) **유지**. 사이드바 canonical이 사라지므로 **푸터를 다시 canonical `vercount_value_site_uv`로 되돌리고 미러 스크립트는 제거**한다.
- **`/stats` 페이지**:
  - Chart.js로 **최근 30일 일별 방문자 꺾은선** 1개.
  - 상단에 **"최근 30일 방문자 합계"** 큰 숫자.
  - **출처·기간 명시**: "GA4 · 최근 30일" 라벨로 Vercount 누적과 다른 데이터임을 못박아 혼동 방지.
  - 데이터 없음/실패 시: 그래프 대신 **"통계를 불러올 수 없습니다"** 안내.
  - BaseLayout 사용, 다른 페이지와 동일한 레이아웃/사이드바.

### 차트
- **Chart.js를 npm 의존성으로 설치**해 Astro가 번들. **`/stats` 페이지에서만 로드**(사이트 전역 번들 아님).
- 다크/라이트 팔레트는 기존 사이트 색과 맞춘다.

## 컴포넌트 경계

- `scripts/fetch-ga-stats.mjs` — CI 전용. GA4 Data API 호출 → `public/visit-stats.json` 기록. 실패 시 비치명적 종료(기존 JSON 유지). devDependency `@google-analytics/data` 사용.
- `.github/workflows/deploy.yml` — 빌드 전에 위 스크립트 실행 단계 추가 + `schedule`(cron) 트리거 추가. Secret 주입.
- `src/pages/stats.astro` — `/stats` 페이지. `visit-stats.json`을 읽어 Chart.js로 렌더. 데이터 유무 분기.
- `src/layouts/BaseLayout.astro` — 사이드바 두 줄 제거 + "통계" 탭 추가, 푸터 canonical 복귀(미러 제거).
- `public/visit-stats.json` — 샘플 커밋(로컬·실패 대비). CI에서 실데이터로 덮어씀.

## 사용자 1회성 작업 (코드 외)

1. GA4 **숫자 속성 ID** 확인.
2. GCP 서비스 계정 생성 + GA4 Data API 사용 설정 + JSON 키 발급.
3. 서비스 계정을 GA4 속성에 **뷰어**로 추가.
4. JSON 키를 GitHub Secret `GA_SERVICE_ACCOUNT_KEY`로, 속성 ID를 `GA_PROPERTY_ID`(Secret 또는 변수)로 등록.

## 확장 포인트 (이번 범위 밖 — 이슈 #33)

- **B: 인기 글 top 5 막대차트**. fetch 스크립트에 GA 호출 1개 추가(`topPosts`), `/stats`에 막대차트 블록 1개 추가. Chart.js 재사용. 데이터 출처·인증·갱신은 A와 동일.

## 작업 절차 / 제약

- 브랜치 `feat/visit-counter`에서 이어서 작업(카운터 미머지 상태이고 사이드바/푸터를 함께 정리하므로 한 기능으로 묶음). main 직접 커밋 금지.
- Secret이 필요 없는 부분(사이드바 정리·`/stats`·Chart.js·fetch 스크립트·워크플로·샘플 JSON)을 먼저 구현·검증. 실제 GA 연결은 사용자 설정 후 배포에서 확인.
- `npm run build` 통과. `npm run dev`로 `/stats`가 샘플 데이터로 렌더되고, 사이드바 "통계" 탭·푸터 카운터가 정상인지 확인.

## 성공 기준 (검증 가능)

1. `npm run build` 성공.
2. `/stats` 페이지가 생성되고, 샘플 `visit-stats.json`으로 꺾은선·30일 합계·출처 라벨이 렌더된다.
3. 사이드바에 "통계" 탭이 있고 `/stats`로 이동한다. 사이드바 숫자 두 줄 블록은 사라졌다.
4. 푸터에 Vercount 누적 방문자가 canonical(`vercount_value_site_uv`)로 그대로 뜬다(미러 없음, id 중복 없음).
5. `visit-stats.json`이 비었거나 없을 때 "통계를 불러올 수 없습니다"로 degrade하고 레이아웃이 유지된다.
6. Chart.js 번들은 `/stats`에서만 로드된다(다른 페이지 번들 비대화 없음).
7. (배포 후 운영 확인) CI가 GA4에서 실데이터를 구워 `/stats` 숫자가 채워진다 — 사용자 설정 완료 후.
