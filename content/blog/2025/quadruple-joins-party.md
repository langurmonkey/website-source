+++
author = "Toni Sagrista Selles"
categories = ["Java"]
tags = ["java", "benchmarking", "performance", "JMH", "arithmetics", "Quadruple", "Apfloat", "BigDecimal"]
date = 2025-05-10
linktitle = ""
title = "Quadruple joins the fight!"
description = "This float-128 implementation beats others at same precision"
featuredpath = "date"
type = "post"
+++

<!-- Loading MathJax -->
<script type="text/javascript" id="MathJax-script" async src="/js/mathjax3.js"></script>

A few days ago I wrote about [benchmarking arbitrary precision floating-point libraries in Java]({{< ref "/blog/2025/apfloat-bigdecimal" >}}). I found out that `BigDecimal` is not as slow as it is said to be, beating `Apfloat` at the same precision level by a long margin in most operations. However, for [Gaia Sky](https://gaiasky.space), I don't need hundreds of significant digits at all. It turns out 27 significant digits are enough to represent the whole universe with a precision of 1 meter.

<!--more-->

The observable universe has a radius of about \\(4.4 \times 10^{26}\\) meters. To express the entire range down to 1 meter, we need to calculate the number of significant digits \\(d\\) as follows:

$$
\begin{align}
d &= \log_{10} \left(\frac{R}{\text{precision}}\right) \\\ \\\
&= \log_{10} \left(\frac{4.4 \times 10^{26}}{1}\right) \\\ \\\
&= \log_{10}(4.4 \times 10^{26}) \\\ \\\
&= \log_{10}(4.4) + \log_{10}(10^{26}) \\\ \\\
\approx 0.643 + 26 &= 26.643
\end{align}
$$

So, 27 digits are needed. In terms of bits, IEEE 754 double precision (64-bit) provides around 15–17 decimal digits of precision, which is enough for the Solar System, but insufficient for the whole universe. IEEE 754 quadruple precision (128-bit) provides around 34 decimal digits of precision, which is adequate for this level of precision. IEEE 754 quadruple precision numbers provides approximately 113 bits of significand precision, which is approximately \\(log_{10}(2^{113}) \approx 34\\) digits. The range of values we can precisely differentiate in the universe is \\(\approx \frac{4.4 \times 10^{26}}{10^{34}} = 4.4 \times 10^{-8}\\) meters. This is 4.4 nanometers! Of course, this is more than sufficient for our purposes.

## Enter Quadruple

Browsing through GitHub I found the [`Quadruple` library](https://github.com/m-vokhm/Quadruple), which provides an implementation of 128-bit floating point numbers in Java. The implementation is very compact, and includes **addition**, **subtraction**, **multiplication**, **division**, and **square root**. I decided to put it to the test using my JMH benchmark.

I created a new benchmark called "ThreeWay", which tests these operations (plus allocation) for `Apfloat`, `BigDecimal`, and `Quadruple`. In the arbitrary precision library I'm using only 32 significant digits of precision instead of 34. I do 1 set of 1 second as warm-up, and 5 iterations of 5 seconds for the measurement (see [source](https://codeberg.org/langurmonkey/java-arbitrary-precision-benchmark/src/branch/master/src/main/java/com/tonisagrista/ThreeWay.java)).

## Results

Below are the specs of the system I used to run the tests, and the specific software versions used. This time around I ran the benchmarks in my laptop while it was plugged in. Only the CPU and the memory should play a significant role.

```
# JMH version: 1.37
# VM version: JDK 21.0.7, OpenJDK 64-Bit Server VM, 21.0.7+6

CPU: Intel(R) Core(TM) i7-8550U (8) @ 4.00 GHz
GPU 1: NVIDIA GeForce GTX 1070 [Discrete]
GPU: Intel UHD Graphics 620 @ 1.15 GHz [Integrated]
Memory: 16.00 GiB
Swap: 8.00 GiB
```

And here are the benchmark results.

### Addition

{{< fig src="/img/2025/05/jmh-result-TWAddition.svg" class="fig-center" width="100%" title="Three-way Addition results -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWAddition.json)" loading="lazy" >}}


Of course, `Quadruple` is compact and only needs to care about 128 bits, while `Apfloat` and `BigDecimal` are generic to any precision, so we can expect `Quadruple` to be faster. And it is.

### Subtraction

{{< fig src="/img/2025/05/jmh-result-TWSubtraction.svg" class="fig-center" width="100%" title="Three-way Subtraction results -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWSubtraction.json)" loading="lazy" >}}

Same with subtraction.

### Multiplication

{{< fig src="/img/2025/05/jmh-result-TWMultiplication.svg" class="fig-center" width="100%" title="Three-way Multiplication results -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWMultiplication.json)" loading="lazy" >}}

And multiplication.

### Division

{{< fig src="/img/2025/05/jmh-result-TWDivision.svg" class="fig-center" width="100%" title="Three-way Division results -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWDivision.json)" loading="lazy" >}}

Division is also faster with the newcomer.

### Allocation (from string)

Finally, the allocation test. First, we test allocation from a string representation of a floating point number.

{{< fig src="/img/2025/05/jmh-result-TWAlloc.svg" class="fig-center" width="100%" title="Three-way Allocation results (from string) -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWAlloc.json)" loading="lazy" >}}

Surprising. Let's analyze this. We use [JOL](@ "Java Object Layout") to find out the instance size of each object.

- `Quadruple` has an instance size of 40 bytes (2 longs, 1 int, 1 boolean, plus header).
- `BigDecimal` has an instance size of also 40 bytes (2 ints, 1 long, 2 references to `BigInteger` and `String`, plus header).
- `Apfloat` has an instance size of 24 (3 references plus the object header).

It is unlikely that the issue is the instance size. It most definitely comes down to the code to convert the string into the internal representation of each type. This code seems much slower for the `Quardruple` than it is for the others. Let's see how it fares allocating from a `double`.

### Allocation (from double)

{{< fig src="/img/2025/05/jmh-result-TWAllocationDouble.svg" class="fig-center" width="100%" title="Three-way Allocation results (from double) -- [Interactive view](https://jmh.morethan.io/?source=https://tonisagrista.com/files/2025/apfloat-bigdecimal/jmh-result-TWAllocationDouble.json)" loading="lazy" >}}

The story is reversed. `Quadruple` is much faster than the others when allocating an object from a `double`.


## Analysis

There's not much to say. `Quadruple` is obviously much faster in a very significant way than the others. This is, of course, to be expected if we consider that `Quadruple` only deals with float-128 types and does not have to care about higher precisions. It may be enough for your purposes, like it is for mine. If this is the case, it may make sense to use it.

## Caveats

There are a couple of important caveats to consider if you want to use `Quadruple` as it is now:

- Only the basic operations are implemented (add, sub, div, mul, sqrt). If you need anything else, you are on your own.
- `Quadruple` instances are **mutable**. This is a bad design decision in my opinion, and would bar it from adopting further improvements that will land soon to Java like value types ([project Valhalla](https://en.wikipedia.org/wiki/Project_Valhalla_(Java_language))).
- Instantiation from `String` is very slow.

