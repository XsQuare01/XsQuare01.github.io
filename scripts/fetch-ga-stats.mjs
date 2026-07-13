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

  // (3) 유입 경로 — 구체적 소스 상위 8 (방문자 기준)
  const [srcResp] = await client.runReport({
    property,
    dateRanges,
    dimensions: [{ name: 'sessionSource' }],
    metrics: [{ name: 'activeUsers' }],
    orderBys: [{ metric: { metricName: 'activeUsers' }, desc: true }],
    limit: 8,
  });
  const sources = (srcResp.rows ?? []).map((r) => ({
    source: r.dimensionValues[0].value,
    visitors: Number(r.metricValues[0].value),
  }));

  const out = {
    source: 'GA4',
    rangeDays: 30,
    generatedAt: new Date().toISOString(),
    daily,
    total,
    sources,
  };
  writeFileSync(OUT, JSON.stringify(out, null, 2));
  console.log(`[ga-stats] ${daily.length}일, 30일 순 방문자 ${total}, 유입 소스 ${sources.length}개 기록`);
} catch (e) {
  console.warn('[ga-stats] 조회 실패 — 기존 파일 유지:', e.message);
  process.exit(0); // 비치명적: 배포 계속
}
