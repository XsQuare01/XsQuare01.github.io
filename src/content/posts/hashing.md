---
title: "Cryptographic Hashing — 암호화 해시 함수"
date: 2026-03-31T10:00:00
description: "SHA의 내부 구조(Merkle-Damgård), 일방향성·충돌 저항성의 수학, Birthday Paradox가 해시 길이에 미치는 영향, MD5·SHA-1이 왜 더 이상 안전하지 않은지, 그리고 HMAC과 패스워드 해시까지 — 암호화 해시 함수의 전체를 다룬다."
tags: ["Computer Science", "Cryptography"]
category: cryptography
---

> 전자 서명에서 SHA로 메시지를 압축해 서명 크기를 줄인다고 했다. 그런데 SHA는 어떻게 동작하는가? 왜 역산이 불가능한가? 그리고 MD5나 SHA-1은 왜 더 이상 믿을 수 없는가? 이 글은 그 질문들에 답한다.

<div class="callout">
<div class="callout-title">이 글의 주요 개념</div>
<ul>
<li><strong>해시 함수의 3대 보안 성질</strong>: 일방향성(2ⁿ), 2차 역상 저항(2ⁿ), 충돌 저항성(2^(n/2))</li>
<li><strong>Merkle-Damgård 구조</strong>: SHA-256의 내부 — 패딩, 블록 분할, 64라운드 압축 반복</li>
<li><strong>Birthday Paradox</strong>: 충돌 공격이 역상 공격보다 √N 배 쉬운 이유</li>
<li><strong>MD5·SHA-1 폐기</strong>: 실제 충돌 사례와 현재 권장 기준</li>
<li><strong>HMAC·패스워드 해시</strong>: 해시 함수의 올바른 응용</li>
</ul>
</div>

## 해시 함수의 3대 보안 성질

암호화 해시 함수 $H$는 임의 길이의 메시지 $m$을 고정 크기의 해시값 $h$로 변환한다.

$$
h = H(m)
$$

단순히 데이터를 압축하는 것만으로는 부족하다. 암호 목적으로 안전하려면 세 가지 성질이 필요하다.

![암호화 해시 함수의 3대 보안 성질과 Checksum 비교](/images/hashing/hash-properties.svg)

**일방향성(Pre-image Resistance)**: $h$가 주어져도 $H(m) = h$인 $m$을 찾을 수 없다. 평균 $2^n$번의 시도가 필요하다. 서명 위조를 위해 특정 해시값을 갖는 메시지를 조작하는 것이 불가능해야 한다.

**2차 역상 저항(Second Pre-image Resistance)**: $m_1$이 주어졌을 때 $H(m_2) = H(m_1)$인 $m_2 \neq m_1$을 찾을 수 없다. 평균 $2^n$번이 필요하다. 기존 문서와 같은 해시를 갖는 위조 문서를 만들 수 없어야 한다.

**충돌 저항성(Collision Resistance)**: $H(m_1) = H(m_2)$인 임의의 쌍 $(m_1, m_2)$를 찾을 수 없다. Birthday Paradox에 의해 $2^{n/2}$번이면 충분하다. 이것이 세 성질 중 가장 약하므로 해시 길이를 결정하는 기준이 된다.

이 세 성질을 Checksum(체크섬)과 비교하면 차이가 명확해진다. 체크섬은 $A+1, B-1$ 변조에도 값이 변하지 않아 의도적 변조를 막지 못한다. 반면 암호화 해시는 1비트 변경에도 해시값이 완전히 달라진다 — 눈사태 효과(Avalanche Effect).

## Merkle-Damgård 구조

SHA-256의 내부는 **Merkle-Damgård(MD) 구조** 를 따른다. 고정 크기 입력만 처리할 수 있는 압축 함수 $f$를 이용해 임의 길이 입력을 처리하는 방법이다.

![Merkle-Damgård 구조 — SHA-256 내부 동작](/images/hashing/merkle-damgard.svg)

**① 패딩**: 메시지 뒤에 `1` 비트를 붙이고, 512 비트 블록 경계에 맞게 `0`으로 채운 뒤 끝에 64 비트 원본 길이를 붙인다. 이로써 입력이 512 비트의 배수가 된다.

**② 블록 분할 및 순차 압축**: 512 비트 블록으로 나눈 뒤, 초기값(IV)부터 시작해 각 블록을 차례로 압축한다.

$$
h_i = f(h_{i-1},\ m_i)
$$

**③ 압축 함수 내부**: 8개의 32비트 상태 레지스터(A–H)를 64라운드 반복 갱신한다. 각 라운드에서 Ch(선택 함수), Maj(다수결 함수), 두 종류의 회전 함수(Σ, σ), 메시지 스케줄 $W_i$, 라운드 상수 $K_i$가 사용된다. Davies-Meyer 구조에 따라 출력에 입력 상태를 XOR로 더한다.

$$
h_i = f(h_{i-1}, m_i) \oplus h_{i-1}
$$

이 피드백이 역산을 어렵게 만든다. $h_i$에서 $f$의 출력을 빼려면 $h_{i-1}$을 알아야 하고, $h_{i-1}$을 찾으려면 또 이전 값이 필요하다.

### Length Extension 취약점

MD 구조에는 한 가지 취약점이 있다. $H(m)$만 알면 $H(m \| \text{padding} \| m')$을 비밀 없이 계산할 수 있다. 마지막 블록의 출력 상태가 그대로 다음 입력 상태가 되기 때문이다.

이 때문에 MAC(메시지 인증 코드)을 만들 때 $H(\text{key} \| m)$ 형태로 직접 사용하면 안 된다. 대신 **HMAC** 을 사용한다.

$$
\text{HMAC}(k, m) = H\bigl((k \oplus \text{opad}) \| H((k \oplus \text{ipad}) \| m)\bigr)
$$

SHA-3(Keccak)는 스펀지 구조(Sponge Construction)를 사용해 이 취약점을 근본적으로 해소했다.

## Birthday Paradox와 해시 길이

왜 충돌 저항성이 $2^n$이 아니라 $2^{n/2}$인가?

> 365일 중 생일이 같은 **두 사람** 을 찾으려면 23명이면 충분하다 ($\approx \sqrt{365}$). 반면 **특정인** 과 생일이 같은 사람을 찾으려면 253명이 필요하다.

해시에서도 마찬가지다. 특정 $h$와 충돌하는 $m$을 찾으려면 $2^n$번이 필요하지만, **임의의 충돌 쌍** $(m_1, m_2)$를 찾으려면 $\approx 2^{n/2}$번이면 된다.

![Birthday Paradox와 해시 충돌 — MD5·SHA-1 폐기 이유](/images/hashing/birthday-collision.svg)

확률 공식은 다음과 같다.

$$
P(\text{충돌}) \approx 1 - e^{-k^2 / 2N}
$$

50% 확률로 충돌이 발생하는 시도 횟수 $k \approx 1.18\sqrt{N}$이다. $n$비트 해시에서 $N = 2^n$이므로 $k \approx 2^{n/2}$이다.

따라서:

| 해시 | 크기 | 이론적 충돌 복잡도 | 실제 공격 복잡도 | 상태 |
|------|------|-----------------|------|------|
| MD5 | 128 bit | $2^{64}$ | $2^{40}$ (Wang et al. 2004) | **폐기** — 수 초 내 충돌 생성 가능 |
| SHA-1 | 160 bit | $2^{80}$ | $\approx 2^{63}$ (SHAttered 2017) | **폐기** — 주요 CA·브라우저 거부 |
| SHA-256 | 256 bit | $2^{128}$ | 알려진 실용적 공격 없음 | 현재 표준 |
| SHA-512 | 512 bit | $2^{256}$ | 알려진 실용적 공격 없음 | 초장기 안전 |

양자 컴퓨터 환경에서는 Grover 알고리즘으로 역상 공격이 $2^{n/2}$로, 충돌 공격이 $2^{n/3}$으로 줄어든다. 양자 내성을 고려하면 SHA-384 이상을 권장한다.

## MD5와 SHA-1이 폐기된 이유

이론적 취약점 발견으로 끝나지 않았다. 실제 공격이 현실화됐다.

**MD5**: 2004년 Wang 등이 $2^{40}$ 연산으로 충돌을 만들어냈다. 이후 가정용 PC로 수 초 내에 충돌 쌍을 생성할 수 있게 됐다. 2012년 Flame 악성코드는 MD5 충돌을 이용해 Microsoft 코드 서명 인증서를 위조했다.

**SHA-1**: 2005년 $2^{63}$ 이론 공격에 이어, 2017년 Google 연구팀이 동일한 SHA-1 해시값을 갖는 두 PDF 파일을 실제로 공개했다(SHAttered). 비용은 약 $45,000(2019년 GPU 기준). Chrome, Firefox, 모든 주요 CA는 2017년부터 SHA-1 인증서를 거부한다.

## 올바른 해시 함수 응용

해시 함수는 올바르게 사용해야 한다. 잘못된 사용이 취약점을 만든다.

**패스워드 저장**: SHA-256(password)를 그대로 저장하면 안 된다. 레인보우 테이블 공격과 사전 공격에 취약하다. 의도적으로 느리게 설계된 **bcrypt, scrypt, Argon2** 를 사용해야 한다. 이들은 연산 비용이 높아 대규모 병렬 공격을 어렵게 만든다.

**메시지 인증(MAC)**: 위에서 언급했듯 $H(\text{key} \| m)$ 형태는 Length Extension 취약점이 있다. **HMAC-SHA256** 을 사용한다.

**무결성 검사**: 파일 다운로드 후 SHA-256 해시를 확인하는 것은 전송 오류나 우발적 변조를 감지하는 데 적합하다. 단, 해시값 자체가 변조되지 않았다는 전제가 필요하다 — 전자 서명이나 HTTPS로 해시값의 출처를 보증해야 한다.

**전자 서명**: [이전 글](/blog/signature)에서 다뤘듯, SHA-256(m)에 서명하면 서명 크기가 메시지 크기와 무관해진다. 충돌 저항성이 Not Convertible을 보장한다.

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>
<ul>
<li>해시 함수의 3대 성질: 일방향성(2ⁿ), 2차 역상 저항(2ⁿ), 충돌 저항성(2^(n/2)). 충돌 저항성이 가장 약하므로 해시 길이를 결정한다.</li>
<li>SHA-256은 Merkle-Damgård 구조: 패딩 → 블록 분할 → IV에서 시작해 압축 함수 f를 블록마다 적용 → 최종 256 bit 해시 출력.</li>
<li>Birthday Paradox: n비트 해시의 충돌 공격 복잡도는 2^(n/2). SHA-256의 실질 충돌 저항성은 2¹²⁸.</li>
<li>MD5·SHA-1은 실제 충돌이 발생했다. 서명·인증서에 사용 금지. 현재 표준은 SHA-256 이상.</li>
<li>MAC에는 HMAC을 사용(Length Extension 방지). 패스워드에는 bcrypt/Argon2를 사용(느린 해시).</li>
</ul>
</div>

<div class="callout">
<div class="callout-title">다음 포스트</div>
<p><strong>Zero Knowledge Proof — 전달 없이 입증하기</strong> — Shamir의 비밀 공유, 그래프 동형 영지식 증명, 시뮬레이션 논증을 통한 No Transfer 증명, 그리고 RSA 기반 실용적 대안까지 다룬다.</p>
</div>
