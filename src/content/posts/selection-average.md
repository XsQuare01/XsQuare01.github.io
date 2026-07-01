---
title: "추가 설명 — quickselect는 왜 평균 O(n)인가"
date: 2026-06-29T09:01:00
description: "선택 문제 본문이 '대부분 O(n)'으로 넘어간 quickselect의 평균 시간을 기댓값 점화식으로 엄밀히 따진다. 퀵 정렬과 달리 한쪽으로만 재귀하기 때문에 E(n)에 max 항이 생기고, 이를 상계로 풀면 E(n) ≤ 4n = O(n)이다."
tags: ["Algorithm", "Selection", "Quickselect", "Expected Value", "추가 설명"]
category: algorithm
difficulty: 고급
---

[선택 문제](/blog/selection) 본문은 quickselect를 소개하면서 "대부분 $O(n)$"이라는 말로 평균을 넘어갔다. 최선·최악은 간단히 보였지만, **평균이 정말 $O(n)$인지**는 기댓값 점화식을 세우고 직접 풀어야 확인할 수 있다. 이 글이 그 빈칸을 채운다.

---

## 한쪽만 재귀한다는 차이

[퀵 정렬 평균 분석](/blog/quicksort)부터 떠올려 보자. pivot의 등수를 $k$라 하면, 퀵 정렬은 왼쪽 $k-1$개와 오른쪽 $n-k$개 **양쪽 모두**를 재귀해야 한다. 그래서 점화식에 $E(k-1) + E(n-k)$가 더해진다. 두 비용을 **합산**하기 때문에 결국 $\Theta(n \log n)$이 나온다.

quickselect는 다르다. 분할 후 $k$번째 원소가 어느 쪽에 있는지 pivot 등수와 비교해 알 수 있으므로, **관계없는 쪽은 버리고 한쪽만 재귀**한다. 그 비용은 $E(k-1)$ 또는 $E(n-k)$ **둘 중 하나**다.

최악의 경우를 상계로 잡으면, 어느 쪽으로 재귀하더라도 비용은 $\max\!\bigl(E(k-1),\,E(n-k)\bigr)$ 이하다. 이것이 퀵 정렬 점화식과 quickselect 점화식의 결정적 차이다.

---

## 기댓값 점화식

pivot의 등수 $k$가 $1$부터 $n$까지 각각 확률 $\frac{1}{n}$로 나온다고 가정한다. 분할 자체는 배열을 한 번 훑으므로 $n$이다. 재귀 비용의 상계를 $\max$ 항으로 잡으면 점화식이 선다.

$$
E(n) \le n + \frac{1}{n}\sum_{i=1}^{n}\max\!\bigl(E(i-1),\,E(n-i)\bigr)
$$

이 합을 더 단순하게 만들 수 있다. $\max\!\bigl(E(i-1),\,E(n-i)\bigr)$는 항상 둘 중 **큰** 쪽에서 나온다. $i$가 $n/2$를 넘으면 $E(i-1)$이 더 크고, $n/2$ 이하면 $E(n-i)$가 더 크다(등호 경우 양쪽 같음). 대칭성에 의해 두 반쪽을 합산하면 $E(\lfloor n/2 \rfloor), E(\lfloor n/2 \rfloor+1), \ldots, E(n-1)$이 각각 **두 번씩** 나타난다. 따라서 합을 절반 구간으로 줄일 수 있다.

$$
E(n) \le n + \frac{2}{n}\sum_{i=\lfloor n/2 \rfloor}^{n-1} E(i)
$$

이것이 풀어야 할 점화식이다.

---

## 상계 풀이 — $E(n) \le 4n$

**수학적 귀납법**으로 $E(n) \le 4n$을 보인다.

**기저 사례.** $n = 1$이면 비교 없이 바로 반환하므로 $E(1) \le 4$. 성립한다.

**귀납 가정.** $i < n$인 모든 $i$에 대해 $E(i) \le 4i$라고 가정한다.

**귀납 단계.** 가정을 점화식에 대입한다.

$$
E(n) \le n + \frac{2}{n}\sum_{i=\lfloor n/2 \rfloor}^{n-1} 4i
= n + \frac{8}{n}\sum_{i=\lfloor n/2 \rfloor}^{n-1} i
$$

합 $\displaystyle\sum_{i=\lfloor n/2 \rfloor}^{n-1} i$의 상한을 등차수열 공식으로 구한다. 항의 개수는 $n - \lfloor n/2 \rfloor = \lceil n/2 \rceil$개이고, 첫 항과 끝 항은 각각 $\lfloor n/2 \rfloor$와 $n-1$이다. 따라서:

$$
\sum_{i=\lfloor n/2 \rfloor}^{n-1} i = \frac{\lceil n/2 \rceil\,\bigl(\lfloor n/2 \rfloor + (n-1)\bigr)}{2} \;\le\; \frac{3n^2}{8}
$$

마지막 부등식은 $n$이 짝수든 홀수든 직접 대입해 확인된다. 홀수 $n$에서는 항의 개수 $\lceil n/2 \rceil$이 $n/2$를 조금 넘지만, 그만큼 첫 항 $\lfloor n/2 \rfloor$이 작아져 곱이 $\tfrac{3n^2}{8}$을 넘지 않는다. 이를 대입하면:

$$
E(n) \le n + \frac{8}{n} \cdot \frac{3n^2}{8} = n + 3n = 4n
$$

귀납 가정이 $n$에서도 성립한다. 따라서 모든 $n$에 대해 $E(n) \le 4n = O(n)$.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

**Quickselect의 평균 시간은 $E(n) \le 4n = O(n)$이다.**

퀵 정렬이 $\Theta(n \log n)$인 이유는 **양쪽 재귀**의 비용 $E(k-1) + E(n-k)$를 합산하기 때문이다. 합산된 비용들을 텔레스코핑하면 조화수 $H_n \approx \ln n$이 나타나 $n \log n$ 항이 생긴다.

Quickselect는 **한쪽만** 재귀하므로 비용이 $\max\!\bigl(E(k-1),\,E(n-k)\bigr)$로 묶인다. 절반 구간의 합이 $\sum_{i=n/2}^{n-1} i \le \frac{3n^2}{8}$으로 억제되는 것이 핵심 상한이며, 덕분에 전체 기댓값이 $O(n)$에 머문다.

단, 이것은 **평균** 분석이다. 최악은 여전히 $O(n^2)$이다. 최악까지 없애려면 pivot을 항상 approximate median으로 고르는 [median of medians](/blog/selection)가 필요하다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>이 글의 바탕이 되는 quickselect와 median of medians는 <a href="/blog/selection">선택 문제</a>에서 다룬다. 퀵 정렬의 평균이 $\Theta(n \log n)$으로 유도되는 과정은 <a href="/blog/quicksort">퀵 정렬 평균 분석</a>에서 텔레스코핑으로 엄밀히 보인다.</p>
</div>
