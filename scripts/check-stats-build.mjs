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
const statsRefsChart = chartChunks.some((f) => statsHtml.includes(f));
const indexRefsChart = chartChunks.some((f) => indexHtml.includes(f));
must(statsRefsChart, '/stats가 Chart 청크 로드');
must(!indexRefsChart, '홈(index)은 Chart 청크 미로드(청크 격리)');

// 4) 푸터 canonical 유일 + 구 미러/사이드바 제거
const uv = (indexHtml.match(/id="vercount_value_site_uv"/g) || []).length;
must(uv === 1, `푸터 canonical vercount_value_site_uv 1개 (실제 ${uv})`);
must(!indexHtml.includes('footer-visit-uv') && !indexHtml.includes('sidebar-visits'), '구 미러/사이드바 블록 제거됨');

console.log(fail === 0 ? '\nALL PASS' : `\n${fail} FAIL`);
process.exit(fail === 0 ? 0 : 1);
