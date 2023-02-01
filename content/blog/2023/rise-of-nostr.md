+++
author = "Toni Sagristà Sellés"
title = "The meteoric rise of nostr"
description = "The brand new protocol is seeing a huge early adoption"
categories = ["Nostr"]
tags = ["technical", "web", "social", "network", "internet", "privacy", "technology", "english"]
date = "2023-02-02"
type = "post"
+++

After the acquisition of Twitter by *the South African billionaire* the free and open source social network world is generating a lot of heat. The number of users and nodes of Mastodon in particular and the Fediverse at large has been [climbing steadily](https://the-federation.info/) for months now. However, there is no shortage of people who voice their concerns about the federated nature of such services, which rely on centralized instances governed by *small dictators* with absolute power. But this is not the post to discuss these issues.

## Enter nostr

To answer such concerns, a brand new protocol called [nostr](https://github.com/nostr-protocol/nostr) is on the rise. Nostr is fundamentally different from Twitter and Mastodon in which it is just a protocol, a specification of how communication should be conducted. It is up to the community to implement clients and servers that talk this protocol. Nostr, which stands for **Notes and Other Stuff Transmitted by Relays**, is very simple in its basic specification, and defines a set of NIPs (Nostr Implementation Possibilities) that lay out procedures to handle more complex use cases, like contact lists, identification, or mention handling.

NIP01 describes the basic protocol flow in a [short markdown document](https://github.com/nostr-protocol/nips/blob/master/01.md). Essentially, each user has a keypair (secret and public keys) used to encrypt and sign events, which are JSON-encoded strings with a specific format. Each event has a unique ID and is sent to one or more relays. Relays are servers that receive and send messages to users, among other tasks. So if you are a client, you have a list of relays, and you send them a request event to subscribe to updates. When you write a post from a client, that post is sent directly to multiple relays.

In the end, all of this

## Identification with NIP05



