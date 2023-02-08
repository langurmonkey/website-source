+++
author = "Toni Sagristà Sellés"
title = "The meteoric rise of nostr"
description = "The brand new protocol is seeing a huge early adoption driven by discontent with established social networks"
categories = ["Nostr"]
tags = ["technical", "web", "social", "network", "internet", "privacy", "technology", "english"]
date = "2023-02-02"
type = "post"
+++

After the acquisition of Twitter by *the South African con-man and billionaire* the free and open source social network world is generating a lot of heat. The number of users and nodes of Mastodon in particular and the Fediverse at large has been [climbing steadily](https://the-federation.info/) for months now. However, there is no shortage of people who voice their concerns about the federated nature of such services, which rely on centralized instances governed by *small dictators* with absolute power. But this is not the post to discuss these issues.

## Enter nostr

To answer such concerns, a brand new protocol called [nostr](https://github.com/nostr-protocol/nostr) is on the rise. **Nostr** is fundamentally different from Twitter and Mastodon in which it is just a protocol, a specification of how communication should be conducted. It is up to the community to implement clients and servers that talk this protocol. Nostr, which stands for **Notes and Other Stuff Transmitted by Relays**, is very simple in its basic specification. 

Nostr defines a set of **NIPs** (Nostr Implementation Possibilities) that lay out procedures to handle other aspects of a fully functioning system, like profile data, contact lists, identification, or mention handling. The basic protocol flow is described in detail in NIP01, which consists of a [short markdown document](https://github.com/nostr-protocol/nips/blob/master/01.md) hosted in GitHub. Essentially, each user has a keypair (secret and public keys) used to encrypt and sign events, which are JSON-encoded strings with a specific format. A user writes a **message**, signs it with his private key and send it to multiple relays. **Relays** are servers that receive and send messages to users and check their signatures, among other tasks. Each nostr client has a list of relays and sends them request events to subscribe to updates and message events to submit messages.

Since multiple relays have your messages, subscriptions and so on, no single relay can *mute* or *ban* you effectively. Additionally, users in possession of their encryption keys, providing encryption and authentication by default.

## Clients

There are many clients available that speak nostr. I have just tried a bunch. For instance, [Amethyst](https://play.google.com/store/apps/details?id=com.vitorpamplona.amethyst) is the best Android client around, and I myself use it. In iOS, [Damus](https://github.com/damus-io/damus) seems to be the most functional one. There is also a plethora of web clients. Some of the ones I have tried are:

- [snort.social](https://snort.social) --- has nice looks and seems to be fully-functional.
- [astral.ninja](https://astral.ninja) --- I used this one the most, works very well.
- [coracle.social](hptts://coracle.social) --- supports public channels.
- [anigma.io](https://anigma.io) --- looks a lot like WhatsApp web; they warn that private keys *may* leak.
- [alphaama.com](https://alphaama.com) --- this one is a bit weird, looks more like an experiment than a proper client.

And I'm sure desktop and CLI clients are also around, but I have not checked.

## Identification with NIP05

One of the NIPs, [NIP05](https://github.com/nostr-protocol/nips/blob/master/05.md), defines user identification within a domain name. This is similar to Twitter's checkmark, or Mastodon's verification ``rel="me"`` links. In nostr's case, all you need is your own domain and the ability to upload files and set the CORS policy. This requires access to the web server, so Codeberg Pages or similar won't work.

{{< fig src1="/img/2023/02/mastodon-verification.jxl" type1="image/jxl" src2="/img/2023/02/mastodon-verification.avif" type2="image/avif" src="/img/2023/02/mastodon-verification.jpg" class="fig-center" width="55%" title="Mastodon implements verification by checking the websites listed in your profile for the anchors that link back to the profile. This method enables the verification with may sites for a single account." loading="lazy" >}}

First, you need to upload a `nostr.json` file to the `/.well-known` subdirectory in your site, so that the full URL reads like `https://yourdomain.com/.well-known/nostr.json`. The file must contain your verification username and your **public key formatted in hex**. Make sure that your key is in hex. If you have only the npub key, you can convert it with [key-convertr](https://github.com/rot13maxi/key-convertr). The format of the `nostr.json` is the following.

```json
{
  "names": {
    "bob": "b0635d6a9851d3aed0cd6c495b282167acf761729078d975fc341b22650b07b9"
  }
}
```

This content must be freely accessible from any app, so you may need to set the right [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) policy in the web server. Since I use Apache, I added an `.htaccess` file with the following content to the public root of my website.

```.htaccess
Header add Access-Control-Allow-Origin "*"
Header add Access-Control-Allow-Methods: "GET,POST,OPTIONS,DELETE,PUT"
```

Once that is done, add the string `name@yourdomain.com` in the NIP05 field of your client, and you should be able to see the verification status in short. My NIP05 sits at [https://tonisagrista.com/.well-known/nostr.json](npub1kr5shpkaafvys2sg3j3ymhdxj0dkw0wynjqmktupk4ef2z3npw5qjjwt4f), so I entered `langurmonkey@tonisagrista.com` to the NIP05 field. Once you do this in one client, you don't need to do it again, and all other clients should be able to pick it up.

{{< fig src1="/img/2023/02/nostr-verification-snort.jxl" type1="image/jxl" src2="/img/2023/02/nostr-verification-snort.avif" type2="image/avif" src="/img/2023/02/nostr-verification-snort.jpg" class="fig-center" width="55%" title="Successful verification status with NOP05 in snort.social." loading="lazy" >}}

If you don't have your own domain, or you don't manage it directly, you can still get verified with one of the many verification services available. [NostrPlebs](https://nostrplebs.com) is one such service, which offers verification on nostr for a few satoshis.


## The future

Nostr is seeing a rise in users as it starts to gain traction. It seems to mainly be attracting folks interested in bitcoin and crypto. I'm sure that Edward Snowden tweeting fairly regularly about it also helps. Whether nostr is here to stay or it is just a seasonal bloom remains to be seen. In my opinion, it hits many of the right keys for a successful, private and secure protocol to succeed. However, I understand that most people don't care at all about these issues, and are perfectly okay with being spoon-fed curated timelines and targeted ads by big corporations. Only the fact that you need to have your private key at hand in order to login with any client might prove too high a fence to climb for most folks. Moreover, the network will only be able to scale if users have strong incentives to run relays, so It may come to pass that most relays implement a paid model. All in all, my current feeling is that nostr has the right ingredients in the right doses to succeed as a niche social network for geeks and privacy-minded people. Time will tell.

