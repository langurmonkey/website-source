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

I recently set out to compare the performance of [`Apfloat`](http://www.apfloat.org) and [`BigDecimal`](https://docs.oracle.com/en/java/javase/24/docs/api/java.base/java/math/BigDecimal.html) for arbitrary precision arithmetic in Java. I use arbitrary precision floating point numbers in key places of the update cycle in Gaia Sky, so it made sense to explore this. My initial approach was a naive benchmark: a simple `main()` method running arithmetic operations in a loop and measuring the time taken. The results were strongly in favor of `BigDecimal`, even for large precision values. This was unexpected, as the general consensus I [found](https://stackoverflow.com/questions/277309/java-floating-point-high-precision-library) [online](https://groups.google.com/g/javaposse/c/YDYDPbzxntc?pli=1) [suggested](http://www.apfloat.org/apfloat_java/) that `Apfloat` is more performant, especially for higher precision operations (hundreds of digits).

To get more accurate and reliable measurements, I decided to implement a proper [JMH](@ "Java Microbenchmark Harness") benchmark. The benchmark project source is available in [this repository](https://codeberg.org/langurmonkey/java-arbitrary-precision-benchmark). The benchmarks test addition, subtraction, multiplication, division, power, natural logarithm, and sine for both `Apfloat` and `BigDecimal` at different precision levels.

<!--more-->

### Why JMH?

JMH is a benchmarking framework specifically designed for measuring performance in Java applications. It is developed by the OpenJDK team and provides a robust methodology for generating reliable and reproducible benchmark results by accounting for JVM warm-up, runtime optimizations, and other factors that can skew measurements. Given the surprising results in the naive implementation, using JMH allowed me to get more accurate measurements and mitigate potential inaccuracies caused by JVM behavior.

### The Benchmark Implementation

The JMH benchmark project is structured to measure the average time taken for each arithmetic operation over several iterations and precision levels. Here's the structure:
- Separate benchmarks for **addition**, **subtraction**, **multiplication**, **division**, **natural logarithm**, **power**, and **sine**.
- Each benchmark tests `Apfloat` and `BigDecimal`.
- Create the actual objects at benchmark level to factor out allocation costs. Later on I provide a test with in-loop allocations.
- Settled on two precision levels, representative of *low* and *high* precision settings. They are **25** and **1000**.
- Average time mode.
- 200 in-test iterations.
- Two warm-up iterations of two seconds each to minimize JVM effects.
- Two main iterations of two seconds each in the main test. 
- Finally, send result into `Blackhole` to prevent JIT optimizations.

Here is an example for the `Sin` benchmark:

{{< collapsedcode file="/static/code/2025/SinBenchmark.java" language="java" summary="benchmark implementation" >}}


### The Results

I have run the benchmark with Java 21 and JMH 1.37. Below are the specs of my laptop and the specific software versions.

```
# JMH version: 1.37
# VM version: JDK 21.0.7, OpenJDK 64-Bit Server VM, 21.0.7+6

CPU: Intel(R) Core(TM) i7-8550U (8) @ 4.00 GHz
GPU: Intel UHD Graphics 620 @ 1.15 GHz [Integr]
Memory: 16.00 GiB
Swap: 8.00 GiB
```

And here are the benchmark results.

**Addition**

```
Benchmark                              (precision)  Mode  Cnt  Score   Error  Units
Addition.testApfloatAddition                    25  avgt    2  0.058          ms/op
Addition.testApfloatAddition                  1000  avgt    2  0.058          ms/op
Addition.testBigDecimalAddition                 25  avgt    2  0.006          ms/op
Addition.testBigDecimalAddition               1000  avgt    2  0.007          ms/op
```

**Subtraction**
```
Benchmark                              (precision)  Mode  Cnt  Score   Error  Units
Subtraction.testApfloatSubtraction              25  avgt    2  0.082          ms/op
Subtraction.testApfloatSubtraction            1000  avgt    2  0.083          ms/op
Subtraction.testBigDecimalSubtraction           25  avgt    2  0.006          ms/op
Subtraction.testBigDecimalSubtraction         1000  avgt    2  0.007          ms/op
```

Surprising. With both addition and subtraction `BigDecimal` comes out on top.

**Multiplication**
```
Benchmark                                    (precision)  Mode  Cnt  Score   Error  Units
Multiplication.testApfloatMultiplication              25  avgt    2  0.142          ms/op
Multiplication.testApfloatMultiplication            1000  avgt    2  0.143          ms/op
Multiplication.testBigDecimalMultiplication           25  avgt    2  0.008          ms/op
Multiplication.testBigDecimalMultiplication         1000  avgt    2  0.009          ms/op
```

**Division**
```
Benchmark                        (precision)  Mode  Cnt  Score   Error  Units
Division.testApfloatDivision              25  avgt    2  1.629          ms/op
Division.testApfloatDivision            1000  avgt    2  8.568          ms/op
Division.testBigDecimalDivision           25  avgt    2  0.067          ms/op
Division.testBigDecimalDivision         1000  avgt    2  1.730          ms/op
```

Same story here. Division is a notoriously costly operation, but `BigDecimal` still comes out comfortably on top.
Now, let's test some more involved arithmetic operation like the natural logarithm, sine, and power. Those are implemented directly in the `Apfloat` package. We use the [`big-math` project](https://github.com/eobermuhlner/big-math) for `BigDecimal`.

**Log**
```
Benchmark              (precision)  Mode  Cnt     Score   Error  Units
Log.testApfloatLog              25  avgt    2   112.835          ms/op
Log.testApfloatLog            1000  avgt    2  3977.143          ms/op
Log.testBigDecimalLog           25  avgt    2    15.191          ms/op
Log.testBigDecimalLog         1000  avgt    2  6006.199          ms/op
```

The log is roughly twice as fast with `Apfloat` in the high precision setting, but it is much faster in `BigDecimal` in low precision.

**Sin**
```
Benchmark              (precision)  Mode  Cnt      Score   Error  Units
Sin.testApfloatSin              25  avgt    2    610.609          ms/op
Sin.testApfloatSin            1000  avgt    2  27157.444          ms/op
Sin.testBigDecimalSin           25  avgt    2      7.516          ms/op
Sin.testBigDecimalSin         1000  avgt    2   4504.473          ms/op
```

The sine is much faster in `BigDecimal` in both precision settings.

**Pow**
```
Benchmark              (precision)  Mode  Cnt  Score   Error  Units
Pow.testApfloatPow              25  avgt    2  0.311          ms/op
Pow.testApfloatPow            1000  avgt    2  0.350          ms/op
Pow.testBigDecimalPow           25  avgt    2  0.194          ms/op
Pow.testBigDecimalPow         1000  avgt    2  0.036          ms/op
```

And finally, the power repeats the same story, with `BigDecimal` sitting comfortably on the throne again.

I also wanted to test the overhead due to allocation, so I prepared the **AdditionAlloc** test, which creates the operand instances in the loop.

**Addition (in-loop allocation)**
```
Benchmark                                       (precision)  Mode  Cnt  Score   Error  Units
AdditionAllocation.testApFloatAdditionAlloc              25  avgt    2  0.210          ms/op
AdditionAllocation.testApFloatAdditionAlloc            1000  avgt    2  0.234          ms/op
AdditionAllocation.testBigDecimalAdditionAlloc           25  avgt    2  0.281          ms/op
AdditionAllocation.testBigDecimalAdditionAlloc         1000  avgt    2  0.170          ms/op
```

Here we clearly see that the allocation overhead dominates the results. Surprisingly, `BigDecimal` seems faster when using 1000 digits of precision than when it uses only 25. The results are otherwise similar for both libraries.


### Analysis

Contrary to expectations, `BigDecimal` consistently outperformed `Apfloat` across all operations and precision levels, including the higher precisions (500 and 1000 digits) where `Apfloat` was expected to excel. There is a single case when `Apfloat` is faster, and that is in the high precision natural logarithm benchmark. It's safe to say that this is due to the particular implementation or algorithm being used. Otherwise, the disparity is particularly noticeable in division and sine operations, where `Apfloat` is significantly slower than `BigDecimal`.

Specifically, `BigDecimal` was several times faster than `Apfloat` in most operations and precisions. Those are, in my opinion, significant results.

### Questions and Next Steps

I was genuinely surprised by the outcome of these benchmarks, as it contradicts the general consensus regarding `Apfloat`’s supposed performance advantage in high-precision arithmetic. I am reaching out to the community to validate my methodology and results. Are these findings trustworthy, or did I overlook something crucial in my benchmarking approach? Feedback and insights are very much welcome.
