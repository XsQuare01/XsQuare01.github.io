# 블로그 방문자 수 표시 (포스트 설계)

- 날짜: 2026-07-13
- 상태: 승인됨 (사용자 확인)
- 대상: 정적 Astro 사이트, GitHub Pages 배포(`XsQuare01.github.io`)

## 목표

블로그 페이지에서 **방문자 수를 눈으로 볼 수 있게** 한다. 지표는 **순 방문자 수(unique visitor, UV)**, 성향은 **가입 없이 가장 간단하게**.

## 배경 / 제약

- 사이트는 순수 정적(Astro `output: static`, 서버·DB 없음) → 방문 수를 세고 보관하려면 외부 서비스가 필요하다.
- `src/layouts/BaseLayout.astro`에 이미 Google Analytics(gtag)와 GTM이 있으나, 이는 대시보드 수집용이라 **페이지에 숫자를 직접 노출하지 않는다.** 본 기능은 별개이며 충돌하지 않는다.
- 표시 위치로 쓸 기존 요소: `.site-footer`(본문 하단, 모든 페이지 공통).

## 스코프 결정 (브레인스토밍 확정)

- **방식**: Busuanzi 호환 클라이언트 스크립트. 엔드포인트는 **Vercount**(`vercount.one`) 사용 — Busuanzi와 같은 `<span>` id를 쓰는 드롭인 호환이며 원조보다 안정적이고 **가입 불필요**.
- **표시 지표/범위**: **사이트 전체 순 방문자 수(UV)** 하나. Busuanzi 계열은 글별 UV(per-post unique)를 지원하지 않으므로(글별은 PV만), '순 방문자' 지표에 맞춰 사이트 전체 UV로 한다.
- YAGNI: 글별 조회수(PV), PV 총합 등은 이번 범위에서 제외(추후 쉬운 확장으로 남김).

## 구현 개요

- **파일**: `src/layouts/BaseLayout.astro` 한 곳만 수정.
- **스크립트**: Vercount 스크립트를 `</body>` 직전(또는 head, `defer`/`async`)에 1줄 추가. 모든 페이지에서 로드되어 사이트 UV가 집계된다.
  - 예: `<script defer src="https://cn.vercount.one/js"></script>` (Vercount 공식 JS. Busuanzi 호환 span id 자동 채움)
- **표시**: `.site-footer`에 순 방문자 수 노출.
  - 예: `<span class="visit-count">👁 방문자 <span id="busuanzi_value_site_uv">–</span>명</span>`
  - 초기 텍스트 `–`(플레이스홀더)는 스크립트가 값을 채우면 대체된다.
- **스타일**: 기존 `.site-footer` 톤에 맞춰 옅은 각주색(전역 CSS의 footer 색 상속). 필요한 최소 스타일만.

## 실패/엣지 처리

- 외부 서비스가 느리거나 죽으면 숫자 자리에 플레이스홀더(`–`)가 남는다. 레이아웃은 깨지지 않는다.
- 로컬 `npm run dev`/빌드 산출물에서는 실서비스 호출 전이라 숫자가 비어 있을 수 있다. 라벨과 플레이스홀더가 보이면 정상.
- 스크립트 로드는 async/defer로 페이지 렌더링을 막지 않는다.

## 프라이버시 메모

- Vercount(제3자)로 방문 요청이 전송된다. 사이트가 이미 GA/GTM을 쓰고 있어 분석 도구 존재라는 전제는 동일하다. 추가 계정·개인정보 수집 설정은 없다.

## 작업 절차 / 제약

- 모든 작업은 `feat/visit-counter` 브랜치에서. main 직접 커밋 금지.
- `npm run build`로 빌드 통과 확인.
- `npm run dev`로 푸터에 라벨/플레이스홀더가 뜨는지 시각 확인.
- 리뷰 반영 후 PR(Why 충분히, How 방법론 중심).

## 성공 기준

- 모든 페이지 하단(.site-footer)에 사이트 전체 순 방문자 수 표시 자리가 나타난다.
- 배포 후 실제 방문에 따라 숫자가 증가한다(순 방문자 기준).
- 가입·서버·DB 추가 없이 동작한다.
- 빌드가 깨지지 않고, 서비스 장애 시에도 레이아웃이 유지된다.
