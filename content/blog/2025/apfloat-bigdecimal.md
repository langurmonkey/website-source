+++
author = "Toni Sagrista Selles"
categories = ["Java"]
tags = ["java", "benchmarking", "performance", "JMH", "arithmetics"]
date = 2025-05-07
linktitle = ""
title = "Benchmarking arbitrary precision libraries in Java"
description = "`ApFloat` vs `BigDecimal`, a surprising outcome"
featuredpath = "date"
type = "post"
+++

I recently set out to compare the performance of [`ApFloat`](http://www.apfloat.org) and [`BigDecimal`](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/math/BigDecimal.html) for arbitrary precision arithmetic in Java. I use arbitrary precision floating point numbers in key places of the update cycle in Gaia Sky, so it made sense to explore this. My initial approach was a naive benchmark: a simple `main()` method running arithmetic operations in a loop and measuring the time taken. The results were strongly in favor of `BigDecimal`, even for large precision values. This was unexpected, as the general consensus I [found](https://stackoverflow.com/questions/277309/java-floating-point-high-precision-library) [online](https://groups.google.com/g/javaposse/c/YDYDPbzxntc?pli=1) [suggested](http://www.apfloat.org/apfloat_java/) that `ApFloat` is more performant, especially for higher precision operations (hundreds of digits).

To get more accurate and reliable measurements, I decided to implement a proper [JMH](@ "Java Microbenchmark Harness") benchmark. The benchmark project is available on [Codeberg](https://codeberg.org/langurmonkey/java-arbitrary-precision-benchmark). The benchmark tests addition, multiplication, and division for both `ApFloat` and `BigDecimal` at different precision levels ranging from 25 to 1000 digits.

<!--more-->

### Why JMH?

JMH is a benchmarking framework specifically designed for measuring performance in Java applications. It is developed by the OpenJDK team and provides a robust methodology for generating reliable and reproducible benchmark results by accounting for JVM warm-up, runtime optimizations, and other factors that can skew measurements. Given the surprising results in the naive implementation, using JMH allowed me to get more accurate measurements and mitigate potential inaccuracies caused by JVM behavior.

### The Benchmark Implementation

The JMH benchmark class is structured to measure the average time taken for each operation over several iterations and precision levels. Here's the structure:
- Addition, multiplication, and division benchmarks for both `ApFloat` and `BigDecimal`.
- Precision levels of 25, 27, 30, 500, and 1000 digits.
- Iterations and warm-up to minimize JVM effects.

Here is the full implementation:

{{< collapsedcode file="/static/code/2025/PrecisionBenchmark.java" language="java" summary="benchmark implementation" >}}

### The Results

I have run the benchmark with Java 21 and JMH 1.37. Below are the system specs and the specific versions.

```
# JMH version: 1.37
# VM version: JDK 21.0.7, OpenJDK 64-Bit Server VM, 21.0.7+6

CPU: Intel(R) Core(TM) i7-7700 (8) @ 4.20 Gz
GPU 1: NVIDIA GeForce GTX 1070 [Discrete]
GPU 2: Intel HD Graphics 630 [Integrated]
Memory: 32.00 GiB
Swap: 8.00 GiB
```

And here are the benchmark results:

```
Benchmark                                        (precision)  Mode  Cnt  Score    Error  Units
PrecisionBenchmark.testApFloatAddition                    25  avgt    4  0.021 ±  0.002  ms/op
PrecisionBenchmark.testApFloatAddition                    27  avgt    4  0.022 ±  0.002  ms/op
PrecisionBenchmark.testApFloatAddition                    30  avgt    4  0.023 ±  0.007  ms/op
PrecisionBenchmark.testApFloatAddition                   500  avgt    4  0.023 ±  0.004  ms/op
PrecisionBenchmark.testApFloatAddition                  1000  avgt    4  0.023 ±  0.001  ms/op
PrecisionBenchmark.testApFloatDivision                    25  avgt    4  0.687 ±  0.047  ms/op
PrecisionBenchmark.testApFloatDivision                    27  avgt    4  0.698 ±  0.077  ms/op
PrecisionBenchmark.testApFloatDivision                    30  avgt    4  0.710 ±  0.093  ms/op
PrecisionBenchmark.testApFloatDivision                   500  avgt    4  2.478 ±  0.482  ms/op
PrecisionBenchmark.testApFloatDivision                  1000  avgt    4  3.792 ±  0.493  ms/op
PrecisionBenchmark.testApFloatMultiplication              25  avgt    4  0.063 ±  0.012  ms/op
PrecisionBenchmark.testApFloatMultiplication              27  avgt    4  0.061 ±  0.012  ms/op
PrecisionBenchmark.testApFloatMultiplication              30  avgt    4  0.061 ±  0.011  ms/op
PrecisionBenchmark.testApFloatMultiplication             500  avgt    4  0.066 ±  0.013  ms/op
PrecisionBenchmark.testApFloatMultiplication            1000  avgt    4  0.063 ±  0.011  ms/op
PrecisionBenchmark.testBigDecimalAddition                 25  avgt    4  0.003 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalAddition                 27  avgt    4  0.003 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalAddition                 30  avgt    4  0.003 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalAddition                500  avgt    4  0.003 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalAddition               1000  avgt    4  0.003 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalDivision                 25  avgt    4  0.032 ±  0.003  ms/op
PrecisionBenchmark.testBigDecimalDivision                 27  avgt    4  0.032 ±  0.002  ms/op
PrecisionBenchmark.testBigDecimalDivision                 30  avgt    4  0.044 ±  0.002  ms/op
PrecisionBenchmark.testBigDecimalDivision                500  avgt    4  0.461 ±  0.031  ms/op
PrecisionBenchmark.testBigDecimalDivision               1000  avgt    4  0.828 ±  0.048  ms/op
PrecisionBenchmark.testBigDecimalMultiplication           25  avgt    4  0.005 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalMultiplication           27  avgt    4  0.005 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalMultiplication           30  avgt    4  0.007 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalMultiplication          500  avgt    4  0.005 ±  0.001  ms/op
PrecisionBenchmark.testBigDecimalMultiplication         1000  avgt    4  0.005 ±  0.001  ms/op
```

### Analysis

Contrary to expectations, `BigDecimal` consistently outperformed `ApFloat` across all operations and precision levels, including the higher precisions (500 and 1000 digits) where `ApFloat` was expected to excel. The disparity is particularly noticeable in division operations, where `ApFloat` is significantly slower than `BigDecimal`.

Specifically, `BigDecimal` was \~7 times faster in additions, \~16 times faster in divisions, and some \~10 times faster in multiplications. Those are significant numbers.

### Questions and Next Steps

I was genuinely surprised by these results, as they contradict the general consensus regarding `ApFloat`’s supposed performance advantage in high-precision arithmetic. I am reaching out to the community to validate my methodology and results. Are these findings trustworthy, or did I overlook something crucial in my benchmarking approach? Feedback and insights are very much welcome.
