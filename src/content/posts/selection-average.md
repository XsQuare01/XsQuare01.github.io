---
title: "추가 설명 — quickselect는 왜 평균 O(n)인가"
date: 2026-06-29T09:01:00
description: "선택 문제 본문이 '대부분 O(n)'으로 넘어간 quickselect의 평균 시간을 기댓값 점화식으로 엄밀히 따진다. quick sort와 달리 한쪽으로만 재귀하기 때문에 E(n)에 max 항이 생기고, 이를 상계로 풀면 E(n) ≤ 4n = O(n)이다."
tags: ["Algorithm", "Selection", "Quickselect", "Expected Value", "추가 설명"]
category: algorithm
difficulty: 고급
---

[선택 문제](/blog/selection) 본문은 quickselect를 소개하면서 "대부분 $O(n)$"이라는 말로 평균을 넘어갔다. 최선·최악은 간단히 보였지만, **평균이 정말 $O(n)$인지**는 기댓값 점화식을 세우고 직접 풀어야 확인할 수 있다. 이 글이 그 빈칸을 채운다.

---

## 한쪽만 재귀한다는 차이

[quick sort 평균 분석](/blog/quicksort)부터 떠올려 보자. pivot의 등수를 $k$라 하면, quick sort는 왼쪽 $k-1$개와 오른쪽 $n-k$개 **양쪽 모두**를 재귀해야 한다. 그래서 점화식에 $E(k-1) + E(n-k)$가 더해진다. 두 비용을 **합산**하기 때문에 결국 $\Theta(n \log n)$이 나온다.

quickselect는 다르다. 분할 후 $k$번째 원소가 어느 쪽에 있는지 pivot 등수와 비교해 알 수 있으므로, **관계없는 쪽은 버리고 한쪽만 재귀**한다. 그 비용은 $E(k-1)$ 또는 $E(n-k)$ **둘 중 하나**다.

최악의 경우를 상계로 잡으면, 어느 쪽으로 재귀하더라도 비용은 $\max\!\bigl(E(k-1),\,E(n-k)\bigr)$ 이하다. 이것이 quick sort 점화식과 quickselect 점화식의 결정적 차이다.

---

## 기댓값 점화식

pivot의 등수 $k$가 $1$부터 $n$까지 각각 확률 $\frac{1}{n}$로 나온다고 가정한다. 분할 자체는 배열을 한 번 훑으므로 $n$이다. 재귀 비용의 상계를 $\max$ 항으로 잡으면 점화식이 선다.

$$
E(n) \le n + \frac{1}{n}\sum_{i=1}^{n}\max\!\bigl(E(i-1),\,E(n-i)\bigr)
$$

이것이 풀어야 할 점화식이다.

<div class="callout callout-simple">
<div class="callout-title">여기서 $\max$를 먼저 정리하지 않는 이유</div>

$\max\!\bigl(E(i-1),\,E(n-i)\bigr)$를 $E\!\bigl(\max(i-1,\,n-i)\bigr)$로 바꾸고 싶어진다. 크기가 큰 쪽이 비용도 크다는 것이 당연해 보이기 때문이다. 하지만 그 치환은 **$E$가 증가함수**라는 사실을 쓰는 것이고, 우리는 아직 그것을 증명하지 않았다. 지금 증명하려는 대상이 $E$ 자신이므로 순환에 빠지기도 쉽다.

대신 $\max$를 **귀납 단계로 미룬다.** 거기서는 $E(i-1)$과 $E(n-i)$를 먼저 각각 $4(i-1)$, $4(n-i)$로 바꾼 뒤 $\max$를 취하게 되고, $\max(4a,\,4b) = 4\max(a,\,b)$는 아무 성질도 필요로 하지 않는다. 미루기만 해도 단조성 가정이 사라진다.

</div>

---

## 상계 풀이 — $E(n) \le 4n$

**수학적 귀납법**으로 $E(n) \le 4n$을 보인다.

**기저 사례.** $E(0) = 0$이고, $n = 1$이면 비교 없이 바로 반환하므로 $E(1) = 0 \le 4$. 둘 다 성립한다.

**귀납 가정.** $j < n$인 모든 $j$에 대해 $E(j) \le 4j$라고 가정한다.

**귀납 단계.** 합 안의 각 항에 가정을 먼저 적용한다. $i-1$과 $n-i$는 둘 다 $n$보다 작으므로 가정을 쓸 수 있다.

$$
\max\!\bigl(E(i-1),\,E(n-i)\bigr) \;\le\; \max\!\bigl(4(i-1),\,4(n-i)\bigr) \;=\; 4\max(i-1,\,n-i)
$$

이제 $\max$가 $E$ 밖으로 나왔다. 점화식에 넣으면

$$
E(n) \le n + \frac{4}{n}\sum_{i=1}^{n}\max(i-1,\,n-i)
$$

이고, 남은 일은 정수 합 $\sum_{i=1}^{n}\max(i-1,\,n-i)$의 상한뿐이다.

### 합을 정확히 세기

$i$가 $1$부터 $n$까지 돌 때 $\max(i-1,\,n-i)$가 어떤 값들을 훑는지 $n = 6$과 $n = 7$로 보자.

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 합 |
|---|---|---|---|---|---|---|---|---|
| $n = 6$ | 5 | 4 | 3 | 3 | 4 | 5 | | 24 |
| $n = 7$ | 6 | 5 | 4 | **3** | 4 | 5 | 6 | 33 |

짝수 $n$에서는 모든 값이 정확히 두 번씩 나온다. **홀수 $n$에서는 가운데 값 하나가 한 번만 나온다** ($n=7$의 $3$). "각 항이 두 번씩"이라고 뭉뚱그리면 홀수에서 틀리므로, 두 경우를 나눠 센다. $n = 2m$과 $n = 2m+1$로 두면

$$
\sum_{i=1}^{n}\max(i-1,\,n-i) =
\begin{cases}
2\displaystyle\sum_{j=m}^{2m-1} j = 3m^2 - m, & n = 2m \\[1.2em]
2\displaystyle\sum_{j=m+1}^{2m} j + m = 3m^2 + 2m, & n = 2m+1
\end{cases}
$$

이다. 두 값 모두 $\dfrac{3n^2}{4}$ 이하다. 짝수에서는 $3m^2 - m \le 3m^2 = \frac{3n^2}{4}$이고, 홀수에서는 $\frac{3n^2}{4} = 3m^2 + 3m + \frac{3}{4}$이므로 $3m^2 + 2m$보다 $m + \frac{3}{4}$만큼 크다.

$$
\sum_{i=1}^{n}\max(i-1,\,n-i) \;\le\; \frac{3n^2}{4}
$$

### 마무리

이를 대입하면

$$
E(n) \le n + \frac{4}{n} \cdot \frac{3n^2}{4} = n + 3n = 4n
$$

귀납 가정이 $n$에서도 성립한다. 따라서 모든 $n$에 대해 $E(n) \le 4n = O(n)$이다.

$E$의 단조성은 어디에도 쓰이지 않았고, 홀수 $n$의 중앙항도 정확히 한 번으로 세었다.

---

<div class="callout callout-key">
<div class="callout-title">핵심 정리</div>

**quickselect의 평균 시간은 $E(n) \le 4n = O(n)$이다.**

quick sort가 $\Theta(n \log n)$인 이유는 **양쪽 재귀**의 비용 $E(k-1) + E(n-k)$를 합산하기 때문이다. 합산된 비용들을 텔레스코핑하면 조화수 $H_n \approx \ln n$이 나타나 $n \log n$ 항이 생긴다.

quickselect는 **한쪽만** 재귀하므로 비용이 $\max\!\bigl(E(k-1),\,E(n-k)\bigr)$로 묶인다. 귀납 단계에서 각 항을 $4j$로 바꾼 뒤 $\max$를 밖으로 빼면 $\sum_{i=1}^{n}\max(i-1,\,n-i) \le \frac{3n^2}{4}$가 핵심 상한이 되고, 덕분에 전체 기댓값이 $O(n)$에 머문다. 이 순서 덕분에 $E$의 단조성을 가정하지 않아도 된다.

단, 이것은 **평균** 분석이다. 최악은 여전히 $O(n^2)$이다. 최악까지 없애려면 pivot을 항상 approximate median으로 고르는 [median of medians](/blog/selection)가 필요하다.

</div>

<div class="callout">
<div class="callout-title">이어지는 글</div>
<p>이 글의 바탕이 되는 quickselect와 median of medians는 <a href="/blog/selection">선택 문제</a>에서 다룬다. quick sort의 평균이 $\Theta(n \log n)$으로 유도되는 과정은 <a href="/blog/quicksort">quick sort 평균 분석</a>에서 텔레스코핑으로 엄밀히 보인다.</p>
</div>
