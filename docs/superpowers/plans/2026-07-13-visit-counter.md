# 방문자 수 표시 (Vercount) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 모든 페이지 하단(.site-footer)에 사이트 전체 방문자 근삿값(Vercount site UV)을 가입 없이 표시한다.

**Architecture:** 정적 Astro 사이트라 서버가 없으므로, 외부 서비스 Vercount의 클라이언트 스크립트를 `BaseLayout.astro`에 넣는다. 스크립트는 배포(`import.meta.env.PROD`)에서만 로드하고, 푸터의 `<span id="vercount_value_site_uv">`에 값을 채운다. 별도 모듈·추상화 없이 레이아웃 한 파일만 수정한다.

**Tech Stack:** Astro 6, Vercount(`events.vercount.one`), GitHub Pages.

## Global Constraints

- 브랜치: `feat/visit-counter`에서만 작업. main 직접 커밋 금지.
- 엔드포인트: `https://events.vercount.one/js` (공식 canonical). 다른 미러 사용 금지.
- 표시 ID: Vercount 전용 `vercount_value_site_uv` (busuanzi 호환 ID 사용 금지).
- 외부 스크립트는 `import.meta.env.PROD`일 때만 렌더링. 개발 환경에서 외부 호출 금지.
- 스크립트는 `is:inline defer` (Astro 번들/호이스트 방지 + 렌더 비차단).
- 라벨은 이모지 없이 텍스트 전용("방문자 … 명"). 초기 플레이스홀더 `–`.
- 단일 파일(`src/layouts/BaseLayout.astro`)만 수정. 신규 파일·CSS 파일 변경 없음(색은 .site-footer 상속, 간격은 인라인 구분자).

---

### Task 1: BaseLayout에 방문자 수 표시 + PROD 전용 Vercount 스크립트

**Files:**
- Modify: `src/layouts/BaseLayout.astro` (`.site-footer` 블록, `</body>` 직전)

**Interfaces:**
- Consumes: 없음(외부 서비스 Vercount).
- Produces: 모든 페이지 푸터의 `#vercount_value_site_uv` 요소와, 배포 빌드에만 포함되는 Vercount 스크립트.

- [ ] **Step 1: 사이드바(canonical) + 푸터(미러) 표시 추가**

(A) 사이드바 `.sidebar-footer`의 © 줄을 찾는다:

```astro
      <div style="margin-top:0.5rem;">© {new Date().getFullYear()} XsQuare01</div>
```

그 아래에 canonical 두 줄을 추가한다:

```astro
      <div style="margin-top:0.5rem;">© {new Date().getFullYear()} XsQuare01</div>
      <div class="sidebar-visits" style="margin-top:0.4rem;font-size:0.8rem;line-height:1.6;opacity:0.85;">
        <div>총 방문자 <span id="vercount_value_site_uv">–</span>명</div>
        <div>총 방문수 <span id="vercount_value_site_pv">–</span>회</div>
      </div>
```

(B) 푸터 `.site-footer`는 미러용 id(`footer-visit-uv`)로 둔다:

```astro
        <footer class="site-footer">
          <span>© {new Date().getFullYear()} XsQuare01. Powered by GitHub Pages.</span>
          <span class="visit-count"> · 방문자 <span id="footer-visit-uv">–</span>명</span>
        </footer>
```

- [ ] **Step 2: 배포 전용 Vercount 스크립트 + 미러 스크립트 추가**

같은 파일에서 검색 모달이 닫히고 `</body>`가 나오는 부분을 찾는다:

```astro
      <div id="search-results"></div>
    </div>
  </div>
</body>
```

`</body>` 직전에 배포 전용 Vercount 스크립트와 (항상 렌더되는) 미러 스크립트를 추가한다:

```astro
      <div id="search-results"></div>
    </div>
  </div>

  {import.meta.env.PROD && (
    <script is:inline defer src="https://events.vercount.one/js"></script>
  )}
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
</body>
```

미러 스크립트는 PROD 조건으로 감싸지 않는다(내용에 `{}`가 있어 JSX 표현식 래핑 시 파싱 충돌 위험). 개발 환경에선 `–`를 복사할 뿐 무해하다.

- [ ] **Step 3: 배포 빌드 검증 (스크립트·표시 포함 확인)**

Run: `npm run build`
Expected: 빌드 성공("N page(s) built"). 오류 없음.

이어서 산출물 확인:

Run: `grep -rl "events.vercount.one/js" dist/ | head -1`
Expected: HTML 파일 경로 출력.

Run: `grep -o "vercount_value_site_uv\|vercount_value_site_pv\|footer-visit-uv" dist/index.html | sort -u`
Expected: 세 문자열 모두 출력(사이드바 UV·PV canonical + 푸터 미러 id).

- [ ] **Step 4: 개발 환경 비호출 확인 (수동)**

Run: `npm run dev`
그다음 브라우저로 `http://localhost:4321/` 접속 후:
- 푸터에 `· 방문자 – 명`이 보이는지 확인(숫자는 `–` 유지가 정상).
- 개발자도구 Network 탭에 `events.vercount.one` 요청이 **없는지** 확인.
확인 후 dev 서버 종료(Ctrl+C).

(근거: `import.meta.env.PROD`는 `astro dev`에서 false라 스크립트가 렌더되지 않는다.)

- [ ] **Step 5: 커밋**

```bash
git add src/layouts/BaseLayout.astro
git commit -m "feat(visit-counter): 푸터에 Vercount 방문자 수 표시 (배포 전용 로드)"
```

---

### Task 2: 리뷰·PR (플랜 외 후속)

- 빌드/표시 확인 후, 필요하면 배포된 페이지에서 `–`가 정수로 바뀌는지(성공 기준 3), Vercount 차단 시 `–` 유지·레이아웃 유지(성공 기준 4), 데스크톱·모바일 푸터 깨짐 없음(성공 기준 5)을 운영 확인한다.
- PR 생성(Why 충분히, How 방법론 중심, 참조 코드 위치 섹션).

## Self-Review

**1. Spec coverage:**
- 엔드포인트 `events.vercount.one/js` 명시 → Global Constraints + Task1 Step2 ✓
- Vercount 전용 ID `vercount_value_site_uv` → Task1 Step1 ✓
- PROD 전용 로드(개발 비호출) → Task1 Step2 + Step4 ✓
- 텍스트 전용 라벨/플레이스홀더 `–` → Task1 Step1 ✓
- 단일 파일·과설계 회피 → Files/Constraints ✓
- 실패 시 `–` 유지·레이아웃 유지 → Task2 성공 기준 4 ✓
- 검증 가능한 성공 기준(빌드/산출물/배포/차단/반응형) → Task1 Step3~4, Task2 ✓
- 프라이버시/롤백: 스펙에 기록된 내용으로, 코드 변경 사항은 없음(롤백=Step1·2 역적용). 계획엔 별도 태스크 불필요.

**2. Placeholder scan:** 모든 코드/명령이 실제 값으로 기재됨. `–`는 스펙이 정의한 의도적 표시 플레이스홀더(코드 자리표시 아님). "TBD/적절히" 없음.

**3. Type consistency:** span id `vercount_value_site_uv`가 스펙·Global Constraints·Task1 Step1에서 동일. 엔드포인트 URL 동일. grep 검증 문자열이 삽입 코드와 정확히 일치.
