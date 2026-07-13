# 블로그 방문자 수 표시 (포스트 설계)

- 날짜: 2026-07-13
- 상태: 승인됨 (사용자 스펙 리뷰 반영 v2)
- 대상: 정적 Astro 사이트, GitHub Pages 배포(`XsQuare01.github.io`)

## 목표

블로그 페이지에서 **방문자 수를 눈으로 볼 수 있게** 한다. 지표는 **사이트 방문자 근삿값(site UV)**, 성향은 **가입 없이 가장 간단하게**.

> UV의 정확한 의미(중요): Vercount의 site UV는 **브라우저 Cookie로 동일 브라우저·동일 호스트의 재방문을 제거한 근삿값**이다. 실제 개인 수를 정확히 세는 지표가 아니다. 다음 경우 같은 사람이 여러 UV로 집계될 수 있다 — 다른 브라우저/기기 사용, Cookie 삭제, 시크릿 모드, 호스트 변경. 목표·표시 문구를 이 한계에 맞춰 "정확한 사람 수"로 오인하지 않게 쓴다.

## 배경 / 제약

- 사이트는 순수 정적(Astro `output: static`, 서버·DB 없음) → 방문 수를 세고 보관하려면 외부 서비스가 필요하다.
- `src/layouts/BaseLayout.astro`에 이미 Google Analytics(gtag)와 GTM이 있으나, 이는 대시보드 수집용이라 **페이지에 숫자를 직접 노출하지 않는다.** 본 기능은 별개이며 충돌하지 않는다. (기존 GA 사용이 새 제3자 서비스 도입을 자동으로 정당화하지는 않는다 — 프라이버시 항목에서 별도로 판단한다.)
- 표시 위치로 쓸 기존 요소: `.site-footer`(본문 하단, 모든 페이지 공통).

## 스코프 결정 (브레인스토밍 + 스펙 리뷰 확정)

- **방식**: Vercount(`vercount.one`) 클라이언트 스크립트. 가입·서버·DB 불필요.
- **엔드포인트(명시적 선택)**: **`https://events.vercount.one/js`** 를 사용한다.
  - 근거: Vercount 공식 문서의 현재 canonical 기본 예시가 `events.vercount.one`이다. 구 `cn.vercount.one/js`도 동작할 수 있으나, 공식 canonical 주소를 따르는 편이 유지보수·문서 정합성에 유리하다.
- **표시 ID(Vercount 전용)**: 호환 계층(`busuanzi_value_*`) 대신 **Vercount 전용 `vercount_value_site_uv`** 를 쓴다. 신규 설치이므로 호환 계층에 의존할 이유가 없다.
- **표시 지표/범위(v3 확장)**:
  - 사이드바 하단(`.sidebar-footer`): **총 방문자(site UV)** + **총 방문수(site PV)** 두 줄.
  - 푸터(`.site-footer`): **총 방문자(UV)** 한 줄 유지.
- **"오늘" 지표 제외(불가)**: Vercount는 누적 3지표(site_uv, site_pv, page_pv)만 제공하고 일별/오늘 통계가 없다. 정적 사이트라 어제 값을 저장할 백엔드도 없어 "오늘 방문자"는 이 방식(가입0)으로 구현 불가. 이번 범위에서 제외한다.
- **Vercount id 유일성 제약 + 미러 방식**: Vercount 스크립트는 `document.getElementById`로 각 지표를 채우므로, 같은 id는 페이지에 하나만 있어야 한다(중복 시 첫 요소만 채워짐). 총 방문자(UV)를 사이드바·푸터 두 곳에 띄우기 위해:
  - **canonical**(Vercount가 채우는 실제 id `vercount_value_site_uv`, `vercount_value_site_pv`)는 **사이드바**에 둔다.
  - **푸터**는 미러용 비-Vercount id(`footer-visit-uv`)를 쓰고, 사이드바 UV 값을 작은 스크립트로 복사한다.
- YAGNI: 글별 조회수(page PV) 등은 이번 범위에서 제외(추후 쉬운 확장으로 남김).

## 구현 개요

- **파일**: `src/layouts/BaseLayout.astro` 한 곳만 수정. 별도 로컬 모듈/추상 인터페이스는 만들지 않는다(외부 adapter 하나뿐이라 과설계 회피).
- **스크립트 로드(개발/배포 분기)**: 외부 `<script>`를 그대로 두면 `npm run dev`에서도 Vercount에 요청을 보내 로컬 방문이 집계되고 Cookie가 생성된다. 이를 피하기 위해 **`import.meta.env.PROD`일 때만** 외부 스크립트를 렌더링한다.
  - 배포: `<script is:inline defer src="https://events.vercount.one/js"></script>`
  - 위치: `</body>` 직전(본문 렌더링을 막지 않도록 `defer`). Astro가 번들·호이스트하지 않도록 `is:inline`을 붙인다.
  - 개발: 외부 스크립트를 로드하지 않고 라벨과 플레이스홀더(`–`)만 렌더링한다.
- **표시(사이드바, canonical)**: `.sidebar-footer`의 © 줄 아래에 두 줄 추가.
  - `총 방문자 <span id="vercount_value_site_uv">–</span>명`
  - `총 방문수 <span id="vercount_value_site_pv">–</span>회`
- **표시(푸터, 미러)**: `.site-footer`에 `· 방문자 <span id="footer-visit-uv">–</span>명`.
- **미러 스크립트(`is:inline`, 항상 렌더)**: `MutationObserver`로 사이드바의 `#vercount_value_site_uv` 텍스트 변화를 감지해 `#footer-visit-uv`에 복사. 개발 환경에선 둘 다 `–`라 복사도 무해. Astro 번들 방지를 위해 `is:inline`.
  ```html
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
- **스타일**: 기존 톤에 맞춰 옅은 색 상속, 이모지 없이 텍스트 전용 라벨. 사이드바 두 줄은 인라인 스타일(작은 글자·행간)로 최소 처리, 별도 CSS 파일 변경 없음.

## 실패/엣지 처리

- 외부 서비스가 느리거나 죽으면 숫자 자리에 플레이스홀더(`–`)가 남는다. 레이아웃은 깨지지 않는다.
- 개발 환경에서는 외부 호출 자체가 없으므로 항상 `–`가 보인다(정상).
- 스크립트 로드는 `defer`로 페이지 렌더링을 막지 않는다.

## 프라이버시 / 롤백

- **데이터 흐름**: 배포 페이지 로드 시 `events.vercount.one`으로 방문 요청이 전송된다.
- **Cookie**: UV 중복 제거를 위해 Vercount가 Cookie를 사용한다.
- **외부 실행**: 제3자 스크립트가 페이지에서 실행된다.
- **고지 여부(결정 필요)**: 개인정보 처리방침/Cookie 고지 페이지가 생기면 Vercount 항목을 추가할지 판단한다. (현재 사이트에 별도 고지 페이지는 없음 — GA/GTM도 미고지 상태이나, 이는 본 기능의 고지 필요성을 면제하지 않는다.)
- **CSP**: 현재 사이트에 CSP 없음. 추후 CSP 도입 시 `script-src`/`connect-src`에 `https://events.vercount.one` 를 허용해야 한다.
- **롤백**: 서비스 제거 시 `BaseLayout.astro`의 (1) 외부 `<script>` 한 줄과 (2) `.site-footer`의 `visit-count` 표시 블록을 함께 삭제하면 원상 복구된다.

## 작업 절차 / 제약

- 모든 작업은 `feat/visit-counter` 브랜치에서. main 직접 커밋 금지.
- `npm run build`로 빌드 통과 확인.
- `npm run dev`로 개발 환경에서 라벨/플레이스홀더가 뜨고 외부 호출이 없는지 확인.

## 성공 기준 (검증 가능 항목)

구현 완료의 결정적 기준:

1. `npm run build` 성공.
2. production 빌드 산출물(`dist/`)에 푸터 표시 블록과 `events.vercount.one/js` 스크립트가 출력된다. dev 빌드에는 스크립트가 없고 라벨/`–`만 있다.
3. 실제 배포 페이지에서 `–`가 정수로 교체된다.
4. Vercount 요청을 차단한 상태에서도 `–`가 남고 레이아웃이 유지된다.
5. 데스크톱·모바일 너비에서 푸터가 깨지지 않는다.

수동 운영 확인(결정적 기준에서 제외): 실제 방문 누적에 따른 숫자 증가는 중복 제거·외부 서비스 상태에 좌우되므로, 단순 새로고침으로 검증하지 않고 배포 후 운영 관찰로 둔다.
