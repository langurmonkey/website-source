+++
author = "Toni Sagrista Selles"
categories = ["Java"]
tags = ["java", "benchmarking", "performance", "JMH", "arithmetics"]
date = 2025-05-07
linktitle = ""
title = "Benchmarking arbitrary precision libraries in Java"
description = "`Apfloat` vs `BigDecimal`, a surprising outcome"
featuredpath = "date"
type = "post"
+++

*{{< sp orange >}}Edit (2025-05-08):{{</ sp >}} Changed some test parameters and re-run the tests. Also added bar plots.*

I recently set out to compare the performance of [`Apfloat`](http://www.apfloat.org) and [`BigDecimal`](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/math/BigDecimal.html) for arbitrary precision arithmetic in Java. I use arbitrary precision floating point numbers in key places of the update cycle in Gaia Sky, so it made sense to explore this. My initial approach was a naive benchmark: a simple `main()` method running arithmetic operations in a loop and measuring the time taken. The results were strongly in favor of `BigDecimal`, even for large precision values. This was unexpected, as the general consensus I [found](https://stackoverflow.com/questions/277309/java-floating-point-high-precision-library) [online](https://groups.google.com/g/javaposse/c/YDYDPbzxntc?pli=1) [suggested](http://www.apfloat.org/apfloat_java/) that `Apfloat` is more performant, especially for higher precision operations (hundreds of digits).

To get more accurate and reliable measurements, I decided to implement a proper [JMH](@ "Java Microbenchmark Harness") benchmark. The benchmark project source is available in [this repository](https://codeberg.org/langurmonkey/java-arbitrary-precision-benchmark). The benchmarks test addition, subtraction, multiplication, division, power, natural logarithm, and sine for both `Apfloat` and `BigDecimal` at different precision levels.

<!--more-->

### Why JMH?

JMH is a benchmarking framework specifically designed for measuring performance in Java applications. It is developed by the OpenJDK team and provides a robust methodology for generating reliable and reproducible benchmark results by accounting for JVM warm-up, runtime optimizations, and other factors that can skew measurements. Given the surprising results in the naive implementation, using JMH allowed me to get more accurate measurements and mitigate potential inaccuracies caused by JVM behavior.

### The Benchmark Implementation

The JMH benchmark project is structured to measure the average time taken for each arithmetic operation over several iterations and precision levels. Here's the structure:
- Separate benchmarks for **addition**, **subtraction**, **multiplication**, **division**, **natural logarithm**, **power**, and **sine**, additionally to an **allocation** test.
- Each benchmark tests `Apfloat` and `BigDecimal`.
- Create the actual objects at benchmark level to factor out allocation costs. Specific benchmark to test allocation overhead.
- Settled on four precision levels, on a scale ranging from *low* and *high* precision settings, represented as the number of digits. They are **25**, **50**, **500**, and **1000** digits.
- Average time mode.
- Every benchmark function only runs one operation once. The allocation test creates a couple of objects and consumes them.
- One warm-up iterations of one second each to minimize JVM effects (`@Warmup(iterations = 1, time = 1)`).
- Three main iterations of five seconds each for the measurement (`@Measurement(iterations = 3, time = 5)`). 
- Send results into `Blackhole` to prevent JIT optimizations.

Here is an example for the `Sin` benchmark:

{{< collapsedcode file="/static/code/2025/SinBenchmark.java" language="java" summary="benchmark implementation" >}}


### The Results

Below are the specs of the system I used to run the tests and the specific software versions used. Only the CPU and the memory should play a significant role.

```
# JMH version: 1.37
# VM version: JDK 21.0.7, OpenJDK 64-Bit Server VM, 21.0.7+6

CPU: Intel(R) Core(TM) i7-7700 (8) @ 4.20 GHz
GPU 1: NVIDIA GeForce GTX 1070 [Discrete]
GPU 2: Intel HD Graphics 630 [Integrated]
Memory: 32.00 GiB
Swap: 8.00 GiB
```

And here are the benchmark results.

**Addition**

{{< fig src="/img/2025/05/jmh-result-Addition.svg" class="fig-center" width="100%" title="Addition results" loading="lazy" >}}

We already see that `BigDecimal` is much faster in all precisions. It is not even close.

**Subtraction**

{{< fig src="/img/2025/05/jmh-result-Subtraction.svg" class="fig-center" width="100%" title="Subtraction results" loading="lazy" >}}

In the subtraction benchmark `BigDecimal` comes out on top as well.

**Multiplication**

{{< fig src="/img/2025/05/jmh-result-Multiplication.svg" class="fig-center" width="100%" title="Multiplication results" loading="lazy" >}}

The same story repeats for multiplication.

**Division**

{{< fig src="/img/2025/05/jmh-result-Division.svg" class="fig-center" width="100%" title="Division results" loading="lazy" >}}

Again. Division is a notoriously costly operation, but `BigDecimal` still comes out comfortably on top.

Now, let's test some more involved arithmetic operations, like the natural logarithm, the sine, and the power function. In `Apfloat`, those are directly implemented in the library. For `BigDecimal`, we use the [`big-math` project](https://github.com/eobermuhlner/big-math).

**Log**

{{< fig src="/img/2025/05/jmh-result-Log.svg" class="fig-center" width="100%" title="Log results" loading="lazy" >}}

The logarithm is faster with `Apfloat` at the higher precision settings, but it `BigDecimal` still wins in the lower precisions.

**Sin**

{{< fig src="/img/2025/05/jmh-result-Sin.svg" class="fig-center" width="100%" title="Sin results" loading="lazy" >}}

The sine is much faster in `BigDecimal` in all precision settings.

**Pow**

{{< fig src="/img/2025/05/jmh-result-Pow.svg" class="fig-center" width="100%" title="Pow results" loading="lazy" >}}

And finally, the power repeats the same story, with `BigDecimal` sitting comfortably on the throne again.


**Allocation**

For science, I thought it would be cool to test the allocation overhead, so I prepared the **Allocation** test, which allocates two instances of either `Apfloat` or `BigDecimal` and consumes them.

{{< fig src="/img/2025/05/jmh-result-Allocation.svg" class="fig-center" width="100%" title="Allocation results" loading="lazy" >}}

We see that allocation is very costly in both libraries. However, while `Apfloat` seems to be roughly constant with the precision, `BigDecimal` shows a higher cost with 25 digits, the lowest precision setting. I though this was very sus, so I re-ran the test a bunch of times and with more iterations and longer times, and got back the same result. I'm not sure what's the root cause for this, but it is surprising and intriguing.

Since both `Apfloat` and `BigDecimal` are immutable, allocation costs need to be factored in. New objects need to be allocated every time new operands are needed.


### Analysis

Contrary to expectations, `BigDecimal` consistently outperformed `Apfloat` across all operations and precision levels, including the higher precisions (500 and 1000 digits) where `Apfloat` was expected to excel. There is a single case when `Apfloat` is faster, and that is in the high precision natural logarithm benchmark. I think it's safe to say that this is due to the particular implementation or algorithm being used. Otherwise, the disparity is particularly noticeable in division and sine operations, where `Apfloat` is significantly slower than `BigDecimal`.
Specifically, `BigDecimal` was several times faster than `Apfloat` in most operations and precisions. Those are, in my opinion, significant results.

Finally, allocation seems to be faster with `Apfloat`, and there's a weird dependency on the precision for `BigDecimal` which I found strange.


### Questions and Next Steps

I was genuinely surprised by the outcome of these benchmarks, as it contradicts the general consensus regarding `Apfloat`’s supposed performance advantage in high-precision arithmetic. I am reaching out to the community to validate my methodology and results. Are these findings trustworthy, or did I overlook something crucial in my benchmarking approach? Feedback and insights are very much welcome.
