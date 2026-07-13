# 방문 통계 페이지 `/stats` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 사이드바 "통계" 탭 → `/stats` 페이지에서 GA4 기반 최근 30일 일별 방문자 꺾은선 + 30일 합계를 Chart.js로 보여준다. 데이터는 CI에서 GA4 Data API로 빌드 시 구워지고, 없을 땐 우아하게 degrade한다.

**Architecture:** CI(GitHub Actions)가 서비스 계정으로 GA4 Data API를 호출해 `src/data/visit-stats.json`을 생성 → Astro가 빌드 시 그 JSON을 `/stats` 페이지에 임베드 → 클라이언트에서 Chart.js(이 페이지에서만 번들)가 렌더. 사이드바/푸터 카운터 표시를 재정리한다.

**Tech Stack:** Astro 6, Chart.js(npm), `@google-analytics/data`(CI devDep), GitHub Actions, GitHub Pages.

## Global Constraints

- 브랜치 `feat/visit-counter`에서 이어 작업. main 직접 커밋 금지.
- GA4 지표: 일별 `activeUsers`, 기간 `30daysAgo`~`today`.
- 데이터 파일 경로: `src/data/visit-stats.json` (빌드 시 import). CI가 덮어씀, 샘플은 저장소 커밋.
- JSON 스키마: `{ source, rangeDays, generatedAt, daily: [{date:"YYYY-MM-DD", visitors:number}], total:number }`.
- Secret: `GA_SERVICE_ACCOUNT_KEY`(JSON 전체), `GA_PROPERTY_ID`(숫자). 없으면 fetch는 **비치명적**으로 스킵(exit 0).
- Chart.js는 `/stats` 클라이언트 스크립트에서만 import(전역 번들 금지).
- 사이드바 숫자 두 줄 블록 제거, 푸터는 canonical `vercount_value_site_uv` 유지(미러 제거).
- 커밋 트레일러: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

---

### Task 1: 사이드바/푸터 정리 (BaseLayout)

**Files:**
- Modify: `src/layouts/BaseLayout.astro`

**Interfaces:**
- Produces: 사이드바 "통계" 탭(`/stats` 링크), 푸터 canonical `#vercount_value_site_uv`.

- [ ] **Step 1: 사이드바 메뉴에 "통계" 탭 추가**

`.sidebar-nav`를 찾는다:

```astro
      <a href="/tags" class={currentPath.startsWith('/tags') ? 'active' : ''}>태그</a>
    </nav>
```

`통계` 링크를 추가한다:

```astro
      <a href="/tags" class={currentPath.startsWith('/tags') ? 'active' : ''}>태그</a>
      <a href="/stats" class={currentPath.startsWith('/stats') ? 'active' : ''}>통계</a>
    </nav>
```

- [ ] **Step 2: 사이드바 숫자 두 줄 블록 제거**

다음 블록을 찾아 통째로 삭제한다:

```astro
      <div class="sidebar-visits" style="margin-top:0.4rem;font-size:0.8rem;line-height:1.6;opacity:0.85;">
        <div>총 방문자 <span id="vercount_value_site_uv">–</span>명</div>
        <div>총 방문수 <span id="vercount_value_site_pv">–</span>회</div>
      </div>
```

삭제 후 남는 형태:

```astro
      <div style="margin-top:0.5rem;">© {new Date().getFullYear()} XsQuare01</div>
    </div>
  </aside>
```

- [ ] **Step 3: 푸터를 canonical로 되돌리기**

찾기:

```astro
          <span class="visit-count"> · 방문자 <span id="footer-visit-uv">–</span>명</span>
```

바꾸기(미러 id → canonical):

```astro
          <span class="visit-count"> · 방문자 <span id="vercount_value_site_uv">–</span>명</span>
```

- [ ] **Step 4: 미러 스크립트 제거**

다음 블록을 찾아 통째로 삭제한다:

```astro
  <script is:inline>
    (function () {
      var src = document.getElementById('vercount_value_site_uv');
      var dst = document.getElementById('footer-visit-uv');
      if (!src || !dst) return;
      var sync = function () { dst.textContent = src.textContent; };
      new MutationObserver(sync).observe(src, { childList: true, characterData: true, subtree: true });
      sync();
    })();
  </script>
```

(PROD 전용 Vercount 외부 스크립트 블록은 그대로 둔다 — 푸터 canonical을 채운다.)

- [ ] **Step 5: 빌드 검증**

Run: `npm run build`
Expected: 성공. 이어서 id 중복 없음 확인:

Run: `grep -o "vercount_value_site_uv\|footer-visit-uv\|sidebar-visits" dist/index.html | sort | uniq -c`
Expected: `vercount_value_site_uv` 1개만 출력(푸터 canonical). `footer-visit-uv`·`sidebar-visits` 없음.

- [ ] **Step 6: 커밋**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "refactor(visit-counter): 사이드바 숫자 제거·통계 탭 추가, 푸터 canonical 복귀"
```

---

### Task 2: 샘플 데이터 + `/stats` 페이지 + Chart.js

**Files:**
- Create: `src/data/visit-stats.json`
- Create: `src/pages/stats.astro`
- Modify: `package.json` (chart.js 의존성)

**Interfaces:**
- Consumes: Task 1의 "통계" 탭이 `/stats`로 링크.
- Produces: `/stats` 페이지. `src/data/visit-stats.json` 스키마(위 Global Constraints).

- [ ] **Step 1: Chart.js 설치**

Run: `npm install chart.js`
Expected: `package.json` dependencies에 `chart.js` 추가, 성공.

- [ ] **Step 2: 샘플 데이터 파일 생성**

Create `src/data/visit-stats.json` (더미 7일 — 로컬/실패 대비 렌더용):

```json
{
  "source": "GA4",
  "rangeDays": 30,
  "generatedAt": "2026-07-13T00:00:00.000Z",
  "daily": [
    { "date": "2026-07-07", "visitors": 8 },
    { "date": "2026-07-08", "visitors": 12 },
    { "date": "2026-07-09", "visitors": 10 },
    { "date": "2026-07-10", "visitors": 15 },
    { "date": "2026-07-11", "visitors": 9 },
    { "date": "2026-07-12", "visitors": 14 },
    { "date": "2026-07-13", "visitors": 11 }
  ],
  "total": 79
}
```

- [ ] **Step 3: `/stats` 페이지 생성**

Create `src/pages/stats.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import stats from '../data/visit-stats.json';

const hasData = stats && Array.isArray(stats.daily) && stats.daily.length > 0;
---

<BaseLayout title="통계">
  <h1 class="page-title">방문 통계</h1>
  <p class="stats-source">GA4 · 최근 {stats?.rangeDays ?? 30}일</p>

  {hasData ? (
    <>
      <div class="stats-total">
        최근 {stats.rangeDays}일 방문자 <strong>{stats.total.toLocaleString()}</strong>명
      </div>
      <div class="chart-wrap">
        <canvas id="visit-chart" aria-label="최근 방문자 꺾은선 그래프" role="img"></canvas>
      </div>
      <script type="application/json" id="stats-data" set:html={JSON.stringify(stats)}></script>
    </>
  ) : (
    <p class="stats-empty">통계를 불러올 수 없습니다.</p>
  )}
</BaseLayout>

<script>
  import Chart from 'chart.js/auto';

  const el = document.getElementById('stats-data');
  const canvas = document.getElementById('visit-chart') as HTMLCanvasElement | null;
  if (el && canvas) {
    const data = JSON.parse(el.textContent || '{}');
    const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#3b82f6';
    new Chart(canvas, {
      type: 'line',
      data: {
        labels: (data.daily || []).map((d: any) => d.date),
        datasets: [{
          label: '일별 방문자',
          data: (data.daily || []).map((d: any) => d.visitors),
          borderColor: accent,
          backgroundColor: 'rgba(59,130,246,0.15)',
          fill: true,
          tension: 0.3,
          pointRadius: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { maxTicksLimit: 8 } },
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }
</script>

<style>
  .stats-source {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-top: 0.25rem;
  }
  .stats-total {
    margin: 1.25rem 0;
    font-size: 1.1rem;
    color: var(--text);
  }
  .stats-total strong {
    font-size: 1.6rem;
    color: var(--accent);
    font-family: var(--font-mono);
  }
  .chart-wrap {
    position: relative;
    height: 320px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
  }
  .stats-empty {
    margin-top: 1.5rem;
    color: var(--text-muted);
  }
</style>
```

- [ ] **Step 4: 빌드·번들 검증**

Run: `npm run build`
Expected: 성공, `/stats` 페이지 생성.

Run: `ls dist/stats/index.html && grep -c "방문 통계" dist/stats/index.html`
Expected: 파일 존재, `방문 통계` 1회 이상.

Chart.js가 `/stats`에서만 로드되는지(전역 번들 아님) 확인 — `/stats`의 스크립트 청크만 chart를 참조:

Run: `grep -rl "chart" dist/_astro/*.js | wc -l`
Expected: 청크가 존재하되, 홈/블로그 페이지 HTML은 그 청크를 로드하지 않는다(수동: `dist/index.html`에는 chart 청크 script가 없고, `dist/stats/index.html`에는 있다).

- [ ] **Step 5: 로컬 렌더 확인 (수동)**

Run: `npm run dev` → `http://localhost:4321/stats` 접속.
Expected: 꺾은선 그래프(샘플 7일), "최근 30일 방문자 79명", "GA4 · 최근 30일" 라벨 표시. 사이드바 "통계" 탭 active. 확인 후 Ctrl+C.

- [ ] **Step 6: 커밋**

```bash
git add src/data/visit-stats.json src/pages/stats.astro package.json package-lock.json
git commit -m "feat(stats): /stats 페이지 + Chart.js 방문자 그래프 + 샘플 데이터"
```

---

### Task 3: GA4 fetch 스크립트 + 배포 워크플로

**Files:**
- Create: `scripts/fetch-ga-stats.mjs`
- Modify: `package.json` (`@google-analytics/data` devDependency)
- Modify: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: env `GA_PROPERTY_ID`, `GA_SERVICE_ACCOUNT_KEY`.
- Produces: `src/data/visit-stats.json`(스키마는 Task 2와 동일)을 실데이터로 덮어씀. 실패 시 미변경.

- [ ] **Step 1: GA4 클라이언트 설치(devDependency)**

Run: `npm install --save-dev @google-analytics/data`
Expected: `package.json` devDependencies에 추가.

- [ ] **Step 2: fetch 스크립트 작성**

Create `scripts/fetch-ga-stats.mjs`:

```js
import { BetaAnalyticsDataClient } from '@google-analytics/data';
import { writeFileSync } from 'node:fs';

const OUT = 'src/data/visit-stats.json';
const propertyId = process.env.GA_PROPERTY_ID;
const keyJson = process.env.GA_SERVICE_ACCOUNT_KEY;

if (!propertyId || !keyJson) {
  console.warn('[ga-stats] GA_PROPERTY_ID/GA_SERVICE_ACCOUNT_KEY 미설정 — 기존 JSON 유지, 스킵');
  process.exit(0); // 비치명적
}

try {
  const credentials = JSON.parse(keyJson);
  const client = new BetaAnalyticsDataClient({ credentials });
  const [resp] = await client.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
    dimensions: [{ name: 'date' }],
    metrics: [{ name: 'activeUsers' }],
    orderBys: [{ dimension: { dimensionName: 'date' } }],
  });

  const daily = (resp.rows ?? []).map((r) => {
    const d = r.dimensionValues[0].value; // YYYYMMDD
    return {
      date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`,
      visitors: Number(r.metricValues[0].value),
    };
  });
  const total = daily.reduce((s, d) => s + d.visitors, 0);

  const out = {
    source: 'GA4',
    rangeDays: 30,
    generatedAt: new Date().toISOString(),
    daily,
    total,
  };
  writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(`[ga-stats] ${daily.length}일 기록, 30일 합계 ${total}`);
} catch (e) {
  console.warn('[ga-stats] 조회 실패 — 기존 JSON 유지:', e.message);
  process.exit(0); // 비치명적: 배포는 계속
}
```

- [ ] **Step 3: 스크립트 로컬 스모크 테스트(시크릿 없이 스킵되는지)**

Run: `node scripts/fetch-ga-stats.mjs`
Expected: `[ga-stats] ... 미설정 — ... 스킵` 출력, exit 0. `src/data/visit-stats.json`은 변경되지 않음(git status로 확인).

- [ ] **Step 4: 배포 워크플로 수정 (cron + fetch 단계)**

`.github/workflows/deploy.yml`의 트리거를 찾는다:

```yaml
on:
  push:
    branches: [main]
  workflow_dispatch:
```

cron을 추가한다(매일 1회, UTC 18:17 ≈ KST 03:17):

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '17 18 * * *'
  workflow_dispatch:
```

이어서 build job의 빌드 단계를 찾는다:

```yaml
      - run: npm install
      - run: npm run build
```

fetch 단계를 build 앞에 넣는다(env 주입):

```yaml
      - run: npm install
      - run: node scripts/fetch-ga-stats.mjs
        env:
          GA_PROPERTY_ID: ${{ secrets.GA_PROPERTY_ID }}
          GA_SERVICE_ACCOUNT_KEY: ${{ secrets.GA_SERVICE_ACCOUNT_KEY }}
      - run: npm run build
```

- [ ] **Step 5: 빌드 재검증**

Run: `npm run build`
Expected: 성공(로컬은 시크릿 없어 fetch 스킵, 샘플 JSON으로 `/stats` 렌더).

- [ ] **Step 6: 커밋**

```bash
git add scripts/fetch-ga-stats.mjs package.json package-lock.json .github/workflows/deploy.yml
git commit -m "feat(stats): CI GA4 fetch 스크립트 + 매일 cron 배포"
```

---

### Task 4: 사용자 설정 안내 + 마무리 (플랜 외 후속)

- 사용자에게 GA4 설정 4단계 안내(속성 ID, 서비스 계정+키, GA4 뷰어 추가, GitHub Secret `GA_SERVICE_ACCOUNT_KEY`/`GA_PROPERTY_ID` 등록).
- PR 생성(Why 충분히, How 방법론 중심, 참조 코드 위치). 이슈 #33(B 확장) 링크.
- 배포 후: `/stats` 숫자가 샘플에서 실데이터로 바뀌는지 운영 확인.

## Self-Review

**1. Spec coverage:**
- 데이터 파이프라인(GA4·activeUsers·30일·서비스계정·cron·비치명적·샘플) → Task 3 + Task 2 Step 2 ✓
- 사이드바 두 줄 제거·통계 탭·푸터 canonical·미러 제거 → Task 1 ✓
- `/stats`(Chart.js·30일 꺾은선·30일 합계·출처 라벨·degrade) → Task 2 ✓
- Chart.js `/stats`에서만 번들 → Task 2 Step 1·3·4 ✓
- 성공 기준(빌드·페이지·탭·푸터 canonical·degrade·번들) → Task 1 Step 5, Task 2 Step 4·5 ✓
- B 확장은 이슈 #33 + 스펙 확장 포인트로 분리(이번 범위 밖) ✓

**2. Placeholder scan:** 모든 코드/명령 실제 값. GA property는 런타임 env(`GA_PROPERTY_ID`)로 주입, 코드 내 하드코딩 자리표시자 없음. `–`/샘플은 의도된 데이터.

**3. Type consistency:** JSON 스키마(`daily[].date/visitors`, `total`, `rangeDays`)가 fetch 스크립트 출력·샘플 파일·`stats.astro` 소비에서 동일. `#stats-data`/`#visit-chart` id가 페이지·클라이언트 스크립트에서 일치. `vercount_value_site_uv`는 Task 1 이후 푸터 1곳만.
