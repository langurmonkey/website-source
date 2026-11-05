+++
author = "Toni Sagrista Selles"
categories = ["AI"]
tags = ["LLM", "AI", "LM", "AI inference"]
date = 2026-10-31
linktitle = ""
title = "A tiny language model"
description = "An absolutely minimal language model that still does something"
featuredpath = "date"
type = "post"
draft = true
+++

In this post I document a little experiment I have been playing around with for a while that explores language models in PyTorch. I'm specifically interested in how small can a language model be made while still doing *something*. I got the idea while I was reading a post about GPT-2. A pre-COVID model, GPT-2 now seems minuscule in comparison to current frontier models. Its largest incarnation was trained on about 40 GB of text, had 1.5B parameters and used an embedding dimension of 1600. Nowadays, a GPT-2-like model can be trained with ~16-24 GB of VRAM.

If the GPT-2 family of models pales in comparison to current model dimensions, the model I present here pales in comparison to GPT-2. It can be trained in the CPU and needs very little RAM. It can have single-digit embedding dimensions, does not follow the transformer architecture,has not attention mechanism, and may not even use any hidden layers! It is a purely academic model, in the sense that it is absolutely simple but does nothing useful.

  <!--more-->

Here is a list of some of the properties and concepts that this post touches on:

- Closed world, with 96 words and hard rules
- Embeddings are learned
- Bag of words -> No order
- Ceiling of ~47%
- A few hundreds to a few thousands of parameters
  - Flexible embedding dimensionality
  - Flexible hidden layer dimensionality
- Analysis of accuracy vs embedding dimensionality and hidden layer size

I'll call the language model in this post **TinyLM**. It can have between a few hundred and a few thousand parameters, depending on the dimensionality of the embeddings and the size of the hidden layer. But let's start by the beginning.

## The world

Such a small model wouldn't fare very well trying to reproduce human language, so I reduced it to a set of predefined sentences. I call this set our closed world. This world is composed of only 96 words: 8 proper names, 12 actors, 6 prepositions, 28 places, one determinant, 24 objects, and 13 verbs. Verbs and objects are assigned to one or more classes. For instance, the `drink` class has the verbs "drank" and "sipped", and the objects "wine", "water", "soda", and "beer". Everything that can be expressed is done through those 96 words. I combined those using some rules and got the 2560 possible sentences that constitute our world. This is the whole world. This is the training dataset. This is everything TinlyLM will ever be able to learn and recognize.

## Model structure

Here I describe the structure of the model. The bag of words (no order), the optional hidden layer, etc.

### Accuracy ceiling

The model has an accuracy ceiling due to the fact that we use an unordered bag of words as the input. We encode no positions, so the same bag may have different followings in the world, setting a cap in the maximum accuracy.

## Embeddings

Here I show that even with these strict constraints and such a small world, the learned embeddings cluster around word type.

## Showing results

Here I show how the base accuracy of ~21% improves when I modify the hidden layer, and when I modify the embedding dimensionality.

## Conclusions

Here I show conclusions.
