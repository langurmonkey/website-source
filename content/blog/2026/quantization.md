+++
author = "Toni Sagrista Selles"
categories = ["AI"]
tags = ["llm", "ai", "local llm", "ai inference", "quantization"]
date = 2026-03-04
linktitle = ""
title = "GGUF quantization guide"
description = "A quick guide to understanding modern and legacy quantization methods in LLMs for local inference with GGUF/llama.cpp"
featuredpath = "date"
type = "post"
js = ["/js/mathjax3.js"]
+++

I like running my own LLMs locally. Open models are becoming more and more powerful, with exciting releases like the latest Qwen 3.5 family scoring highly in benchmarks even in their smaller variants. This makes managing and running your own models more viable, as it becomes increasingly easy to repurpose old hardware for local inference with progressively better results. For local users and modest purposes, the GGUF format introduced by llama.cpp is the de-facto default.

Since local inference is typically heavily restricted by the available hardware, several optimization techniques have been implemented to make the models leaner and faster. Perhaps the most important of these is **quantization**, which trims down the bit count per parameter to achieve lower memory usage and (sometimes) faster inference[^1]. The challenge is that there are many different formats and strategies for quantization. In this post, I summarize them, providing a bird's-eye view on the available techniques, their strengths, and their weaknesses.

[^1]: For an exceptionally good (visual) guide as to how quantization is actually performed, I recommend reading this *ngrok* blog post: [Quantization from the ground up](https://ngrok.com/blog/quantization).

<!--more-->

## Naming conventions

Most GGUF quantization names follow this pattern: **`Q{bits}{method}{size}`**

| Component | Meaning |
|-----------|---------|
| `Q` | Quantized format |
| `2/3/4/5/6/8` | Bits per weight (lower = smaller file, more compression) |
| `K` | "K-quant": grouped/blockwise quantization with per-group scales |
| `I` / `IQ` | "I-quant": importance-matrix/non-linear quantization for aggressive compression |
| `0` / `1` | Legacy ungrouped formats (symmetric/asymmetric) |
| `_S` / `_M` / `_L` | Small/Medium/Large: precision mix across tensor types |
| `_XS` / `_XXS` / `_NL` | Extra-small / Non-linear variants for I-quants |


## Unquantized formats

These are base formats with no compression. Usually, but not always, models are trained in these formats.

| Format | Bits | Description | Notes |
|--------|------|-------------|----------|
| **FP32** | 32-bit float | Full precision, ~26GB for 7B model | Research, debugging |
| **FP16** | 16-bit float | Half precision, ~13GB for 7B model | GPU training/inference baseline |
| **BF16** | 16-bit brain float | Same size as FP16, better dynamic range for training | Training on modern GPUs |


These preserve maximum accuracy but require significant VRAM. Most local users quantize to reduce size by 75-90%.


## Legacy quantization formats (`Q*_0`, `Q*_1`)

Simple per-block linear quantization. Fast but less accurate at low bits.

Following is a table that contains the format name, number of bits, size (for a 7B model), perplexity, and some notes/recommendations. The **perplexity** represents the difference between the quantized model and the base model, with lower scores indicating better accuracy and less uncertainty.[^3]


| Format | Bits | Size (7B) | Perplexity \\(\Delta\\) | Notes |
|--------|------|-----------------|--------------|-------|
| **Q8_0** | ~8-bit | ~6.7 GB | +0.0004 | Near-lossless; safe INT8 baseline |
| **Q5_1** | ~5-bit | ~4.7 GB | +0.0415 | Legacy; superseded by Q5_K_M |
| **Q5_0** | ~5-bit | ~4.3 GB | +0.0796 | Legacy; balanced but outdated |
| **Q4_1** | ~4-bit | ~3.9 GB | +0.1846 | Legacy; substantial quality loss |
| **Q4_0** | ~4-bit | ~3.5 GB | +0.2499 | Legacy; high quality loss |

K-quants or I-quants are generally preferred over legacy formats at \\(\leq 5\\) bits. Q8_0 remains useful for compatibility.

[^3]: A good technical explanation of perplexity is in [this section of this *ngrok* post](https://ngrok.com/blog/quantization#perplexity).

## K-Quant formats (modern default)

Use two-level block quantization (small blocks \\(\rightarrow\\) super-blocks) with double-quantized scales for better quality-per-bit.

| Format | Effective Bits | Size (7B) | Perplexity \\(\Delta\\) | Notes |
|--------|---------------|-----------|--------------|----------|
| **Q6_K** | ~6.0 | ~5.15 GB | +0.0044 | "Almost lossless" with savings |
| **Q5_K_L** | ~5.3 | ~4.6 GB | +0.010 | High-quality 5-bit |
| **Q5_K_M** | ~5.1 | ~4.45 GB | +0.0142 | Recommended high-quality 5-bit |
| **Q5_K_S** | ~4.9 | ~4.33 GB | +0.0353 | Recommended balanced 5-bit |
| **Q4_K_L** | ~4.7 | ~4.0 GB | +0.040 | Relaxed 4-bit mix |
| **Q4_K_M** | ~4.5 | ~3.80 GB | +0.0535 | **Most popular default** |
| **Q4_K_S** | ~4.3 | ~3.56 GB | +0.1149 | Smaller 4-bit, more loss |
| **Q3_K_L** | ~3.5 | ~3.35 GB | +0.1803 | Aggressive 3-bit |
| **Q3_K_M** | ~3.3 | ~3.06 GB | +0.2437 | Balanced 3-bit |
| **Q3_K_S** | ~3.1 | ~2.75 GB | +0.5505 | Very small, high loss |
| **Q2_K** | ~2.5 | ~2.67 GB | +0.8698 | Extreme compression, not recommended |

**`Q4_K_M`** seems to be the community sweet spot, as it offers \\(\sim 75\\%\\) size reduction with minimal noticeable quality loss for most tasks.


## I-Quant formats (aggressive compression)

IQs use non-linear reconstruction, lookup tables, and importance-matrix calibration for maximum quality at very low bit counts. They trade decoding speed for size.

| Format | Effective Bits | Size (7B) | Notes |
|--------|---------------|-----------|-------|
| **IQ4_NL** | ~4.5 | ~3.9 GB | Non-linear 4-bit; CPU-friendly speed |
| **IQ4_XS** | ~4.25 | ~3.7 GB | Best quality/size at 4-bit; slightly slower decode |
| **IQ3_M** | ~3.6 | ~3.2 GB | High-quality 3-bit I-quant |
| **IQ3_S** | ~3.4 | ~3.0 GB | Balanced 3-bit aggressive |
| **IQ3_XS** | ~3.2 | ~2.8 GB | Very small 3-bit |
| **IQ3_XXS** | ~3.0 | ~2.6 GB | Extreme 3-bit compression |
| **IQ2_M** | ~2.7 | ~2.4 GB | High-quality 2-bit (rare) |
| **IQ2_S** | ~2.5 | ~2.2 GB | Aggressive 2-bit |
| **IQ2_XS** | ~2.3 | ~2.0 GB | Very aggressive 2-bit |
| **IQ2_XXS** | ~2.1 | ~1.9 GB | Extreme; significant quality loss |

I-quants require **importance matrix (imatrix) calibration** during quantization for best results. Without it, quality can degrade noticeably.


## Special formats

There are even more aggressive quantization methods, like ternary quantization, which converts weights to ternary values.[^2]

| Format | Bits | Description |
|--------|------|-------------|
| **TQ1_0** | ~1.6 | Ternary quantization \\(\\{-1, 0, +1\\}\\), for massive models like DeepSeek where fitting in VRAM is critical |

[^2]: *C. Zhu and S. Han and H. Mao and W. J. Dally*. "Trained Ternary Quantization." *arXiv preprint* [arXiv:1612.01064](https://arxiv.org/abs/1612.01064) (2016).

## Decision guide

Below I attempt to provide some general rules as to what quant to choose in certain situations.

- Best balance overall \\(\rightarrow\\) `Q4_K_M`
- Max quality, still compressed \\(\rightarrow\\) `Q5_K_M` or `Q6_K`
- Tight VRAM, acceptable quality loss \\(\rightarrow\\) `Q4_K_S` or `IQ4_XS`
- Max compression \\(\rightarrow\\) `IQ3_XS` or `Q3_K_S` \\(\Delta\\) {{< sp red >}}test quality!{{</ sp >}}
- Near-lossless accuracy \\(\rightarrow\\) `Q8_0` or keep `FP16`/`BF16`
- CPU inference \\(\rightarrow\\) `Q4_K_M` or `IQ4_NL` \\(\because\\) {{< sp orange >}}better decode speed{{</ sp >}}
- Fit a ~50B model on 16GB VRAM \\(\rightarrow\\) `IQ3_S` or `Q3_K_M` \\(+\\) CPU offload


## Conclusions

The set of quantization methods available may look like the wild west at first glance, but this mess is not without some order. There are always good reasons behind every quantization type. Here are some takeaways:

1. **Bits \\(\neq\\) quality alone**: A well-designed 4-bit format (`Q4_K_M`, `IQ4_XS`) can outperform a naive 5-bit legacy format.
2. **Suffixes matter**: `_M` variants selectively keep sensitive layers at higher precision, improving quality with minimal size cost.
3. **Hardware matters**: I-quants compress more but decode slower on CPUs; K-quants often give better tokens/sec on consumer hardware.
4. **Calibration helps**: Models quantized with an importance matrix (imatrix) retain more accuracy, especially at \\(\leq 3\\) bits.
5. **Test your use case**: Perplexity benchmarks are only guides. Always validate outputs for your specific tasks.


For the latest format support and benchmarks, check the [llama.cpp repository](https://github.com/ggerganov/llama.cpp) or community hubs like Hugging Face, where curators like [bartowski](https://huggingface.co/bartowski) and [Unsloth](https://huggingface.co/unsloth) publish tested GGUF variants.
