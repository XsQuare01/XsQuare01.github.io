---
title: "추가 설명 — 왜 하필 5개로 나누는가"
date: 2026-06-29T09:02:00
description: "median of medians가 그룹을 5개로 나누는 이유. 그룹 크기 g를 일반화해 두 부분문제 비율의 합이 1보다 작아야 선형임을 보인다. g=3은 합이 1이라 깨지고, g=5는 0.9로 성립하며, g=7은 되지만 그룹 정렬 비용만 는다."
tags: ["Algorithm", "Selection", "Median of Medians", "추가 설명"]
category: algorithm
difficulty: 고급
---

> [선택 문제](/blog/selection)의 median of medians는 하필 5개씩 나눴다. 4도 6도 아닌 5인 이유를 따진다.

<div class="callout">
<div class="callout-title">이 글에서 다루는 내용</div>

- 그룹 크기 $g$를 변수로 놓아 보장 원소 수를 일반식으로 유도
- 두 부분문제 $S(n/g) + S(\text{나머지})$의 **비율 합 < 1**이어야 선형이 되는 이유
- $g=3$이 실패하는 구체 수치, $g=5$가 성공하는 이유, $g=7$ 이상이 이득 없는 이유
- 그룹 크기가 홀수여야 하는 이유

</div>

---

## 그룹 크기 g로 일반화

[메인 글](/blog/selection)은 5개씩 묶는 이유를 짧게 예고만 하고 넘어갔다. 여기서는 그 이유를 처음부터 따진다.

$n$개의 원소를 **$g$개씩 묶는다**고 하자. 그러면 그룹이 $n/g$개 생긴다(편의상 $n$이 $g$의 배수라 가정한다). 각 그룹을 정렬해 그룹 중앙값 $X_i$를 구하고, 그 중앙값들의 중앙값 $X'$를 재귀로 찾는다.

**$X'$ 이하임이 보장되는 원소가 몇 개인가?**

$X'$는 $n/g$개의 그룹 중앙값 중 중앙값이므로, 그룹 중앙값의 절반—약 $\dfrac{n}{2g}$개—이 $X'$ 이하다. 이 그룹들은 각자 $\lceil g/2 \rceil$개씩 $X'$ 이하인 원소를 갖는다(그룹이 오름차순 정렬되어 있어, 중앙값 이하 원소가 정확히 $\lceil g/2 \rceil$개). 따라서:

$$
\text{보장 원소 수} \approx \frac{n}{2g} \cdot \left\lceil \frac{g}{2} \right\rceil \approx \frac{n}{2g} \cdot \frac{g+1}{2} = \frac{n(g+1)}{4g}
$$

$g$가 크면 $\dfrac{g+1}{4g} \to \dfrac{1}{4}$으로 수렴한다 — 아무리 그룹을 크게 묶어도 보장은 $n/4$ 근처를 넘지 않는다.

| $g$ | $\lceil g/2 \rceil$ | 보장 수식 | 근사 |
|:---:|:---:|:---:|:---:|
| 3 | 2 | $\frac{n}{6} \cdot 2$ | $\approx 0.33n$ |
| 5 | 3 | $\frac{n}{10} \cdot 3$ | $= 0.3n$ |
| 7 | 4 | $\frac{n}{14} \cdot 4$ | $\approx 0.29n$ |

---

## 선형이 되는 조건

보장 원소가 $\beta_0 n$개라면, $X'$를 pivot으로 쓸 때 재귀하는 쪽의 크기 상한은 $(1 - \beta_0)n$이다. 선택 알고리즘의 점화식은:

$$
S(n) = \underbrace{S(n/g)}_{\text{중앙값 재귀}} + \underbrace{S\!\bigl((1-\beta_0)n\bigr)}_{\text{partition 후 재귀}} + O(n)
$$

$S(n) \le cn$이라는 선형 상한이 닫히려면 **두 재귀 인수의 비율 합이 1 미만**이어야 한다. 이를 $\alpha$, $\beta$로 표기하면:

$$
\alpha + \beta < 1 \qquad \text{여기서 } \alpha = \frac{1}{g},\; \beta = 1 - \beta_0
$$

왜 합이 1 미만이어야 하는지 대입법으로 확인하자. $S(n) \le cn$을 가정하고 점화식에 넣으면:

$$
S(n) \le 2n + \alpha cn + \beta cn = 2n + (\alpha + \beta)cn
$$

이 우변이 다시 $cn$ 이하가 되려면 $2n + (\alpha+\beta)cn \le cn$, 즉 $2 \le (1-\alpha-\beta)c$여야 한다. $\alpha+\beta < 1$이면 $(1-\alpha-\beta)$가 양수이므로 충분히 큰 유한한 $c$를 잡을 수 있다. $\alpha+\beta = 1$이면 불가능하다.

---

### g=5일 때

메인 글의 분석 그대로다. 그룹이 $n/5$개이므로 $\alpha = 1/5 = 0.2$. 보장 원소는 $\frac{n}{10} \times 3 = 0.3n$이므로 $\beta = 1 - 0.3 = 0.7$.

$$
S(n) = 2n + S(0.2n) + S(0.7n), \quad \alpha + \beta = 0.2 + 0.7 = 0.9 < 1 \quad \checkmark
$$

$(1 - 0.9)c \ge 2$를 풀면 $c \ge 20$. 즉 $S(n) \le 20n = O(n)$.

---

### g=3일 때

그룹이 $n/3$개이므로 $\alpha = 1/3$. 보장 원소는 $\frac{n}{6} \times 2 = \frac{n}{3}$이므로 나머지는 $n - n/3 = \frac{2n}{3}$, 즉 $\beta = 2/3$.

$$
S(n) = 2n + S\!\left(\frac{n}{3}\right) + S\!\left(\frac{2n}{3}\right), \quad \alpha + \beta = \frac{1}{3} + \frac{2}{3} = 1 \quad \times
$$

비율 합이 정확히 1이다. 대입법은 $2n \le 0 \cdot cn$을 요구하므로 어떤 $c$도 맞지 않는다. 실제로 이 점화식은 $S(n) = \Theta(n \log n)$으로 풀린다.

---

### g=7일 때

그룹이 $n/7$개이므로 $\alpha = 1/7$. 보장 원소는 $\frac{n}{14} \times 4 = \frac{2n}{7}$이므로 $\beta = 1 - 2/7 = 5/7$.

$$
\alpha + \beta = \frac{1}{7} + \frac{5}{7} = \frac{6}{7} \approx 0.857 < 1 \quad \checkmark
$$

선형은 성립한다. 그런데 그룹 정렬 비용이 $g=5$보다 크고, 보장 비율($2/7 \approx 28.6\%$)도 $g=5$($30\%$)보다 오히려 작다. 더 많이 묶어도 보장은 늘지 않고 비용만 는다.

![g=3 vs g=5 보장 영역 비교 — 그룹 3은 비율 합 1/3+2/3=1로 선형 조건 불충족, 그룹 5는 0.2+0.7=0.9로 성립. 하단 요약 테이블에 g=7 비교도 포함](/images/selection-why-five/group-size-compare.svg)

---

## 홀수여야 하는 이유

그룹 크기가 **짝수**이면 중앙값이 두 개가 되어 "그룹 중앙값"이 모호해진다. 둘 중 하나를 임의로 고르면 보장 계산에서 한 칸 손실이 생긴다. 홀수이면 정가운데 원소 하나가 명확히 중앙값이 된다.

$g=4$는 짝수라 배제된다. 남은 후보는 홀수 중 비율 합 $< 1$을 만족하는 가장 작은 값이다.

- $g=1$: 그룹 정렬이 없고, 그룹 중앙값 = 원소 자체. 중앙값 재귀가 $S(n)$이 되어 진전 없음.
- $g=3$: 비율 합 = 1, 선형 불가.
- $g=5$: 비율 합 = 0.9, **선형 성립. 조건을 만족하는 가장 작은 홀수.**

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

- 그룹 크기 $g$로 묶으면 두 부분문제 $S(n/g)$와 $S((1-\beta_0)n)$이 생긴다.
- 선형 보장의 필요충분 조건: **비율 합 $\alpha + \beta = \tfrac{1}{g} + (1-\beta_0) < 1$**.
- $g=3$: $\frac{1}{3} + \frac{2}{3} = 1$ — 등식이라 선형 깨짐 ($\Theta(n \log n)$).
- $g=5$: $0.2 + 0.7 = 0.9 < 1$ — 성립. $c=20$으로 $S(n) \le 20n$.
- $g=7$ 이상: 합 $< 1$이지만 보장 비율이 오히려 줄고 그룹 정렬 비용만 늘어 이득 없음.
- 그룹 크기는 홀수여야 중앙값이 하나로 명확하므로, **5는 조건을 만족하는 가장 작은 실용적 홀수**다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>이 글의 바탕이 되는 전체 분석은 <a href="/blog/selection">선택 문제 본문</a>에 있다. Quickselect 평균이 $O(n)$인 이유는 <a href="/blog/selection-average">quickselect 평균 O(n) 유도</a>에서 기댓값으로 따진다.</p>
</div>
