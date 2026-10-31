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

In this post I document a little experiment I have been playing around for a while to explore language models in PyTorch. I'm specifically interested in how small can a language model be made while still doing *something*?

  <!--more-->

Here is a list of some of the properties and concepts that this post touches on:

- Closed world, with 96 words and hard rules
- Embeddings are learned
- Bag of words -> No order
- Ceiling of ~47%
- Flexible embedding dimensionality
- Flexible hidden layer dimensionality
- Accuracy vs embedding dimensionality and hidden layer size

I'll call the language model in this post **TinyLM**. It can have between a few hundred and a few thousand parameters, depending on the dimensionality of the embeddings and the size of the hidden layer.

## The world

Our world is composed of only 96 words. Some are nouns, some are verbs, some are prepositions, but everything that can be expressed is done through those 96 words. I combined those using some rules and got ~2000 sentences. This is our whole world. This is our training dataset. This is everything TinlyLM will ever be able to produce and recognized.

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
