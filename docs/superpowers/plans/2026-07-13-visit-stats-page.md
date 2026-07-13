# 방문 통계 페이지 `/stats` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 사이드바 "통계" 탭 → `/stats`에서 GA4 기반 최근 30일 일별 방문자 꺾은선 + 최근 30일 순 방문자 수를 Chart.js로 보여준다. 데이터는 CI에서 GA4 Data API로 빌드 시 구워지고, 없거나 실패하면 샘플 배너와 함께 우아하게 degrade한다.

**Architecture:** CI가 서비스 계정으로 GA4 Data API를 2회 조회(일별 + 기간 전체 순 방문자)해 `src/data/visit-stats.json`을 생성 → Astro가 빌드 시 그 JSON을 `/stats`에 임베드(SSR 총계/라벨) → 클라이언트에서 Chart.js(이 페이지에서만 번들)가 꺾은선을 렌더. 사이드바/푸터 카운터 표시를 재정리한다.

**Tech Stack:** Astro 6, Chart.js(npm), `@google-analytics/data`(CI devDep), GitHub Actions, GitHub Pages.

## Global Constraints

- 브랜치 `feat/visit-counter`에서 이어 작업. main 직접 커밋 금지. 커밋 메시지는 **저장소 커밋 정책을 따른다**(플랜에 특정 co-author를 고정하지 않는다).
- GA4 지표 `activeUsers`. 기간 `30daysAgo`~`yesterday`(부분 집계 오늘 제외). `rangeDays: 30`.
- 데이터 경로: **`src/data/visit-stats.json`**(빌드 시 import). CI 성공 시 덮어씀, 실패/미연결 시 커밋된 샘플 유지.
- JSON 스키마: `{ source:"GA4"|"sample", sample?:true, rangeDays:30, generatedAt:string|null, daily:[{date:"YYYY-MM-DD", visitors:number}], total:number }`.
- **`total`은 일별 합이 아니라** 기간 전체를 date 차원 없이 조회한 **30일 순 방문자**(중복 제거). fetch는 쿼리 2개.
- Secret: `GA_SERVICE_ACCOUNT_KEY`(JSON 전체), `GA_PROPERTY_ID`(숫자). 없으면 fetch는 **비치명적** 스킵(exit 0).
- Chart.js는 `/stats` 클라이언트 스크립트에서만 import(전역 번들 금지).
- 사이드바 숫자 두 줄 제거, 푸터는 canonical `vercount_value_site_uv` 유지(미러 제거).
- 검증은 **크로스플랫폼**으로: `grep/sort/uniq/wc` 대신 `node scripts/check-stats-build.mjs`와 `node -e` 사용(Windows PowerShell 호환).

---

### Task 1: 사이드바/푸터 정리 (BaseLayout)

**Files:**
- Modify: `src/layouts/BaseLayout.astro`

**Interfaces:**
- Produces: 사이드바 "통계" 탭(`/stats`), 푸터 canonical `#vercount_value_site_uv`.

- [ ] **Step 1: 사이드바 메뉴에 "통계" 탭 추가**

`.sidebar-nav`에서 태그 링크 뒤에 추가:

```astro
      <a href="/tags" class={currentPath.startsWith('/tags') ? 'active' : ''}>태그</a>
      <a href="/stats" class={currentPath.startsWith('/stats') ? 'active' : ''}>통계</a>
    </nav>
```

- [ ] **Step 2: 사이드바 숫자 두 줄 블록 제거**

다음 블록을 통째로 삭제:

```astro
      <div class="sidebar-visits" style="margin-top:0.4rem;font-size:0.8rem;line-height:1.6;opacity:0.85;">
        <div>총 방문자 <span id="vercount_value_site_uv">–</span>명</div>
        <div>총 방문수 <span id="vercount_value_site_pv">–</span>회</div>
      </div>
```

- [ ] **Step 3: 푸터를 canonical로 되돌리기**

찾기 → 바꾸기:

```astro
          <span class="visit-count"> · 방문자 <span id="footer-visit-uv">–</span>명</span>
```
```astro
          <span class="visit-count"> · 방문자 <span id="vercount_value_site_uv">–</span>명</span>
```

- [ ] **Step 4: 미러 스크립트 제거**

다음 블록을 통째로 삭제(PROD 전용 Vercount 외부 스크립트 블록은 유지):

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

- [ ] **Step 5: 빌드 + id 유일성 검증(Node)**

Run: `npm run build`
Expected: 성공.

Run: `node -e "const h=require('fs').readFileSync('dist/index.html','utf8');const n=(h.match(/id=\"vercount_value_site_uv\"/g)||[]).length;const m=h.includes('footer-visit-uv')||h.includes('sidebar-visits');console.log('uv:',n,'legacy:',m);process.exit(n===1&&!m?0:1)"`
Expected: `uv: 1 legacy: false`, exit 0. (푸터 canonical 1개, 구 미러/사이드바 블록 없음.)

- [ ] **Step 6: 커밋** (저장소 커밋 정책에 따라 메시지 작성)

```bash
git add src/layouts/BaseLayout.astro
git commit -m "refactor(visit-counter): 사이드바 숫자 제거·통계 탭 추가, 푸터 canonical 복귀"
```

---

### Task 2: 샘플 데이터 + `/stats` 페이지 + Chart.js + 검증 스크립트

**Files:**
- Create: `src/data/visit-stats.json`
- Create: `src/pages/stats.astro`
- Create: `scripts/check-stats-build.mjs` (크로스플랫폼 검증 헬퍼)
- Modify: `package.json`, `package-lock.json` (chart.js)

**Interfaces:**
- Consumes: Task 1의 "통계" 탭 → `/stats`.
- Produces: `/stats`. `src/data/visit-stats.json` 계약(Global Constraints).

- [ ] **Step 1: Chart.js 설치**

Run: `npm install chart.js`
Expected: `package.json` dependencies + `package-lock.json` 갱신.

- [ ] **Step 2: 샘플 데이터(`sample:true`, 0 방문일 포함) 생성**

Create `src/data/visit-stats.json`:

```json
{
  "source": "sample",
  "sample": true,
  "rangeDays": 30,
  "generatedAt": null,
  "daily": [
    { "date": "2026-07-07", "visitors": 8 },
    { "date": "2026-07-08", "visitors": 12 },
    { "date": "2026-07-09", "visitors": 0 },
    { "date": "2026-07-10", "visitors": 15 },
    { "date": "2026-07-11", "visitors": 9 },
    { "date": "2026-07-12", "visitors": 14 },
    { "date": "2026-07-13", "visitors": 11 }
  ],
  "total": 54
}
```

- [ ] **Step 3: `/stats` 페이지 생성 (SSR 총계·배너·마지막 갱신 + 방어적 클라이언트)**

Create `src/pages/stats.astro`:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import stats from '../data/visit-stats.json';

const hasData = stats && Array.isArray(stats.daily) && stats.daily.length > 0;
const isSample = !!stats?.sample;
const updated = stats?.generatedAt
  ? new Date(stats.generatedAt).toISOString().slice(0, 16).replace('T', ' ')
  : '—';
---

<BaseLayout title="통계">
  <h1 class="page-title">방문 통계</h1>
  <p class="stats-source">GA4 · 최근 {stats?.rangeDays ?? 30}일 · 마지막 갱신: {updated}</p>

  {isSample && (
    <p class="stats-banner">샘플 데이터입니다 (GA 연결 전 또는 갱신 실패). 실제 수치가 아닙니다.</p>
  )}

  {hasData ? (
    <>
      <div class="stats-total">
        최근 {stats.rangeDays}일 순 방문자 <strong>{stats.total.toLocaleString()}</strong>명
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
    let data: any;
    try {
      data = JSON.parse(el.textContent || '{}');
    } catch {
      data = null;
    }
    if (data && Array.isArray(data.daily) && data.daily.length) {
      const root = document.documentElement;
      const colors = () => {
        const cs = getComputedStyle(root);
        return {
          accent: cs.getPropertyValue('--accent').trim() || '#3b82f6',
          grid: cs.getPropertyValue('--border').trim() || 'rgba(148,163,184,0.2)',
          tick: cs.getPropertyValue('--text-muted').trim() || '#94a3b8',
        };
      };
      const c0 = colors();
      const chart = new Chart(canvas, {
        type: 'line',
        data: {
          labels: data.daily.map((d: any) => d.date),
          datasets: [{
            label: '일별 방문자',
            data: data.daily.map((d: any) => Number(d.visitors) || 0),
            borderColor: c0.accent,
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
            x: { ticks: { maxTicksLimit: 8, color: c0.tick }, grid: { color: c0.grid } },
            y: { beginAtZero: true, ticks: { precision: 0, color: c0.tick }, grid: { color: c0.grid } },
          },
        },
      });
      // 다크/라이트 전환 시 색 갱신
      new MutationObserver(() => {
        const c = colors();
        chart.data.datasets[0].borderColor = c.accent;
        chart.options.scales!.x!.ticks!.color = c.tick;
        chart.options.scales!.y!.ticks!.color = c.tick;
        (chart.options.scales!.x!.grid as any).color = c.grid;
        (chart.options.scales!.y!.grid as any).color = c.grid;
        chart.update();
      }).observe(root, { attributes: true, attributeFilter: ['class'] });
    }
  }
</script>

<style>
  .stats-source { color: var(--text-muted); font-size: 0.9rem; margin-top: 0.25rem; }
  .stats-banner {
    margin-top: 0.75rem; padding: 0.6rem 0.9rem;
    background: color-mix(in srgb, var(--accent) 12%, transparent);
    border: 1px solid var(--border); border-radius: 8px;
    color: var(--text-muted); font-size: 0.85rem;
  }
  .stats-total { margin: 1.25rem 0; font-size: 1.1rem; color: var(--text); }
  .stats-total strong { font-size: 1.6rem; color: var(--accent); font-family: var(--font-mono); }
  .chart-wrap {
    position: relative; height: 320px;
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 10px; padding: 1rem;
  }
  .stats-empty { margin-top: 1.5rem; color: var(--text-muted); }
  @media (max-width: 640px) { .chart-wrap { height: 260px; } }
</style>
```

- [ ] **Step 4: 크로스플랫폼 검증 스크립트 생성**

Create `scripts/check-stats-build.mjs`:

```js
import { readFileSync, readdirSync, existsSync } from 'node:fs';

let fail = 0;
const must = (cond, msg) => { console.log(`${cond ? 'OK ' : 'FAIL'}  ${msg}`); if (!cond) fail++; };

// 1) /stats 생성
must(existsSync('dist/stats/index.html'), '/stats 페이지 생성됨');
const statsHtml = existsSync('dist/stats/index.html') ? readFileSync('dist/stats/index.html', 'utf8') : '';
const indexHtml = existsSync('dist/index.html') ? readFileSync('dist/index.html', 'utf8') : '';

// 2) SSR 총계/라벨/샘플 배너
must(statsHtml.includes('순 방문자'), 'SSR 총계 문구 존재');
must(statsHtml.includes('마지막 갱신'), '마지막 갱신 표기 존재');
must(statsHtml.includes('샘플 데이터'), '샘플 배너 존재(샘플 데이터 기준)');

// 3) Chart.js 청크 격리: 청크 파일 중 Chart 포함본을 찾아 stats만 참조
const astroDir = 'dist/_astro';
const chunks = existsSync(astroDir) ? readdirSync(astroDir).filter((f) => f.endsWith('.js')) : [];
const chartChunks = chunks.filter((f) => /chart|Chart/.test(readFileSync(`${astroDir}/${f}`, 'utf8')));
must(chartChunks.length > 0, 'Chart.js 청크 존재');
const refs = (html, f) => html.includes(f);
const statsRefsChart = chartChunks.some((f) => refs(statsHtml, f));
const indexRefsChart = chartChunks.some((f) => refs(indexHtml, f));
must(statsRefsChart, '/stats가 Chart 청크 로드');
must(!indexRefsChart, '홈(index)은 Chart 청크 미로드(청크 격리)');

// 4) 푸터 canonical 유일 + 구 미러/사이드바 제거
const uv = (indexHtml.match(/id="vercount_value_site_uv"/g) || []).length;
must(uv === 1, `푸터 canonical vercount_value_site_uv 1개 (실제 ${uv})`);
must(!indexHtml.includes('footer-visit-uv') && !indexHtml.includes('sidebar-visits'), '구 미러/사이드바 블록 제거됨');

console.log(fail === 0 ? '\nALL PASS' : `\n${fail} FAIL`);
process.exit(fail === 0 ? 0 : 1);
```

- [ ] **Step 5: 빌드 + 검증 스크립트 실행**

Run: `npm run build`
Expected: 성공, `/stats` 생성.

Run: `node scripts/check-stats-build.mjs`
Expected: 모든 항목 `OK`, `ALL PASS`, exit 0.

- [ ] **Step 6: 로컬 렌더 확인 (수동, 시나리오 5·6·7·8)**

Run: `npm run dev` → `http://localhost:4321/stats`
확인:
- 꺾은선(샘플 7일, 7/9는 0 방문일 → y=0 정상), "최근 30일 순 방문자 54명", "GA4 · 최근 30일 · 마지막 갱신: —", **샘플 배너** 표시.
- 사이드바 "통계" 탭 active.
- 창을 모바일 너비로 줄여 차트/사이드바 안 깨짐 확인.
- 사이드바 테마 토글로 다크↔라이트 전환 시 그래프 색 갱신 확인.
- (선택) 브라우저 JS 비활성 시 총계/라벨/배너는 보이고 캔버스만 빈지 확인.
확인 후 Ctrl+C.

- [ ] **Step 7: 커밋**

```bash
git add src/data/visit-stats.json src/pages/stats.astro scripts/check-stats-build.mjs package.json package-lock.json
git commit -m "feat(stats): /stats 페이지 + Chart.js 그래프 + 샘플 데이터 + 빌드 검증 스크립트"
```

---

### Task 3: GA4 fetch 스크립트 + 배포 워크플로

**Files:**
- Create: `scripts/fetch-ga-stats.mjs`
- Modify: `package.json`, `package-lock.json` (`@google-analytics/data` devDependency)
- Modify: `.github/workflows/deploy.yml`

**Interfaces:**
- Consumes: env `GA_PROPERTY_ID`, `GA_SERVICE_ACCOUNT_KEY`.
- Produces: `src/data/visit-stats.json`(계약 스키마)을 실데이터로 덮어씀. `total`은 별도 쿼리의 30일 순 방문자. 실패 시 미변경.

- [ ] **Step 1: GA4 클라이언트 설치(devDependency)**

Run: `npm install --save-dev @google-analytics/data`
Expected: devDependencies + `package-lock.json` 갱신.

- [ ] **Step 2: fetch 스크립트 작성 (쿼리 2개: 일별 + 기간 순 방문자)**

Create `scripts/fetch-ga-stats.mjs`:

```js
import { BetaAnalyticsDataClient } from '@google-analytics/data';
import { writeFileSync } from 'node:fs';

const OUT = 'src/data/visit-stats.json';
const propertyId = process.env.GA_PROPERTY_ID;
const keyJson = process.env.GA_SERVICE_ACCOUNT_KEY;

if (!propertyId || !keyJson) {
  console.warn('[ga-stats] GA_PROPERTY_ID/GA_SERVICE_ACCOUNT_KEY 미설정 — 샘플 유지, 스킵');
  process.exit(0); // 비치명적
}

try {
  const credentials = JSON.parse(keyJson);
  const client = new BetaAnalyticsDataClient({ credentials });
  const property = `properties/${propertyId}`;
  const dateRanges = [{ startDate: '30daysAgo', endDate: 'yesterday' }];

  // (1) 일별 순 방문자 — 꺾은선용
  const [dailyResp] = await client.runReport({
    property,
    dateRanges,
    dimensions: [{ name: 'date' }],
    metrics: [{ name: 'activeUsers' }],
    orderBys: [{ dimension: { dimensionName: 'date' } }],
  });
  const daily = (dailyResp.rows ?? []).map((r) => {
    const d = r.dimensionValues[0].value; // YYYYMMDD
    return {
      date: `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`,
      visitors: Number(r.metricValues[0].value),
    };
  });

  // (2) 기간 전체 순 방문자(중복 제거) — 일별 합이 아님
  const [totalResp] = await client.runReport({
    property,
    dateRanges,
    metrics: [{ name: 'activeUsers' }],
  });
  const total = Number(totalResp.rows?.[0]?.metricValues?.[0]?.value ?? 0);

  const out = {
    source: 'GA4',
    rangeDays: 30,
    generatedAt: new Date().toISOString(),
    daily,
    total,
  };
  writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(`[ga-stats] ${daily.length}일, 30일 순 방문자 ${total} 기록`);
} catch (e) {
  console.warn('[ga-stats] 조회 실패 — 기존 파일 유지:', e.message);
  process.exit(0); // 비치명적: 배포 계속
}
```

- [ ] **Step 3: 스모크 테스트(시크릿 없이 스킵)**

Run: `node scripts/fetch-ga-stats.mjs`
Expected: `[ga-stats] ... 미설정 — 샘플 유지, 스킵`, exit 0.

Run: `node -e "console.log(require('./src/data/visit-stats.json').sample===true?'sample-kept':'CHANGED')"`
Expected: `sample-kept` (스킵이라 샘플 파일 불변).

- [ ] **Step 4: 배포 워크플로 수정 (cron + fetch 단계)**

`.github/workflows/deploy.yml`의 트리거에 cron 추가:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '17 18 * * *'
  workflow_dispatch:
```

build job의 install/build 사이에 fetch 단계 추가:

```yaml
      - run: npm install
      - run: node scripts/fetch-ga-stats.mjs
        env:
          GA_PROPERTY_ID: ${{ secrets.GA_PROPERTY_ID }}
          GA_SERVICE_ACCOUNT_KEY: ${{ secrets.GA_SERVICE_ACCOUNT_KEY }}
      - run: npm run build
```

- [ ] **Step 5: 빌드 재검증**

Run: `npm run build && node scripts/check-stats-build.mjs`
Expected: 빌드 성공(로컬은 시크릿 없어 샘플 유지), 검증 `ALL PASS`.

- [ ] **Step 6: 커밋**

```bash
git add scripts/fetch-ga-stats.mjs package.json package-lock.json .github/workflows/deploy.yml
git commit -m "feat(stats): CI GA4 fetch(쿼리 2개) + 매일 cron 배포"
```

---

### 후속 작업 (구현 태스크 아님)

- 사용자 GA4 설정 4단계 안내(속성 ID, 서비스 계정+키, GA4 뷰어 추가, Secret `GA_SERVICE_ACCOUNT_KEY`/`GA_PROPERTY_ID` 등록).
- PR 생성(Why 충분히, How 방법론 중심, 참조 코드 위치). 이슈 #33(B 확장) 링크.
- 배포 후 운영 확인: 실데이터로 `total`(30일 순 방문자)·`daily` 채워지고 샘플 배너 사라지는지.

## Self-Review

**1. Spec coverage:**
- 데이터 계약(경로 `src/data`, 스키마, `total`=30일 순 방문자, 30일 범위 `..yesterday`, `generatedAt`) → Global Constraints, Task 2 Step 2·3, Task 3 Step 2 ✓
- fallback(샘플 `sample:true` + 배너, 빈 daily degrade, 비치명적 스킵) → Task 2 Step 2·3, Task 3 Step 2 ✓
- 사이드바/푸터 정리 → Task 1 ✓
- Chart.js `/stats`만 번들 + 청크 격리 검증 → Task 2 Step 1·3·4·5 ✓
- 검증 시나리오 1~9 → Task 2 Step 5(자동: 빈 daily/스키마 가드/청크 격리/canonical), Step 6(수동: 0방문일/JS off/모바일/테마) ✓
- 마지막 갱신 표시 → Task 2 Step 3 ✓
- B 확장 분리 → 이슈 #33 ✓

**2. Placeholder scan:** 실제 코드/명령. GA property는 env 주입(하드코딩 자리표시자 없음). 검증은 Node(크로스플랫폼). co-author 고정 문구 제거.

**3. Type consistency:** 스키마 필드(`source/sample/rangeDays/generatedAt/daily[].date,visitors/total`)가 fetch 출력·샘플·`stats.astro` 소비·검증 스크립트에서 동일. `total` 의미(30일 순 방문자, 별도 쿼리) 일관. `#stats-data`/`#visit-chart` id 일치. `vercount_value_site_uv`는 Task 1 이후 푸터 1곳.
