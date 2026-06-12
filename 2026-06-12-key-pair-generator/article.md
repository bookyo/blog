---
title: "Why Every 'Generate Key' Button Hides a One-Way Math Problem"
description: "The cryptographic asymmetry behind RSA, ECC, and Ed25519 — and why a single click loads so much trust onto one math problem."
---

## The button that built the modern internet

Every developer has clicked it. You set up a new server, GitHub asks for an SSH key, or you sign a JWT for the first time, and a little button offers to "Generate Key Pair." You click it. A wall of base64-looking text appears, you copy the public half, paste it somewhere, and move on with your day.

That button is the front door of asymmetric cryptography. Without it, HTTPS would not exist, package managers could not sign their releases, Bitcoin could not prove ownership of coins, and the green padlock in your browser would be decorative. It is the single most-clicked piece of cryptographic UX in the world, and almost no one stops to ask what it actually does.

The answer is stranger than the wall of text suggests. A key pair is not a password and its hash. It is two mathematically related numbers, and the relationship between them is so one-directional that the entire security of the internet rests on the fact that you cannot run it in reverse.

## Public and private are not roles, they are directions

The mental model that confuses almost everyone is the word "key." It implies a single thing that locks and unlocks. A cryptographic key pair is closer to a locked mailbox and a metal key. You can drop the mailbox on any street corner. Anyone in the world can walk up, drop a letter through the slot, and walk away. The mail stays inside, readable only by the person holding the metal key.

The mailbox is the public key. The metal key is the private key. The slot is the mathematical relationship between them.

What makes this arrangement work is the asymmetry. The slot is shaped so that a letter can only go in, never come out. The metal key is shaped so that it can only open the box, never fit the slot. In math, this is called a one-way function — an operation that is trivial in one direction and effectively impossible in the other.

## Multiplying is easy, factoring is brutal

For RSA, the most common key pair algorithm, the one-way function is multiplication. Take two random 1024-bit prime numbers, multiply them together, and you get a 2048-bit composite number. A modern laptop can do that in microseconds. Now ask: given only the 2048-bit composite, can you find the two original primes?

That question is integer factorization, and it is one of the hardest known problems in computer science. The best general-purpose algorithm, the General Number Field Sieve, would take roughly 10²⁰ operations to crack a 2048-bit RSA key. Even at a trillion operations per second, that is longer than the age of the universe. The asymmetry is not just "harder" — it is so vastly harder that you can safely publish one side of the math problem on a billboard.

When you click "Generate Key Pair" and pick 2048-bit RSA, the tool is doing this: it picks two huge random primes, multiplies them, and hands you the product as your public key. The primes themselves become your private key, encoded in a way that lets the public key unlock operations the public key cannot.

## Why three algorithms, three one-way problems

A good key pair generator does not just do RSA. It offers ECC and Ed25519 alongside it, because each algorithm uses a different one-way function, and each gives you a different tradeoff between key size, performance, and trust in decades of cryptanalysis.

**RSA** multiplies large primes. It is the oldest of the three, has the largest keys (2048 bits is the modern minimum, 4096 is paranoid), and is the only one of the three that everyone has hardware acceleration for. Almost every TLS certificate on the public web is RSA.

**ECC**, or Elliptic Curve Cryptography, uses a different one-way function: the elliptic-curve discrete logarithm problem. The math is harder to explain than multiplication, but the practical benefit is dramatic. A 256-bit ECC key offers roughly the same security as a 3072-bit RSA key. That is why HTTPS certificates are slowly migrating to EC keys — smaller, faster, less data over the wire, same security.

**Ed25519** is a specific elliptic-curve scheme that goes one step further. It fixes several design quirks in earlier ECC variants, is extremely fast, and produces tiny signatures. SSH has been defaulting to Ed25519 for years. If you have generated a key on a modern Mac with `ssh-keygen`, you have probably used it without knowing.

The reason a generator exposes all three is that you cannot always choose. Some old servers only accept RSA. Some signing pipelines mandate Ed25519. Some compliance frameworks still require specific key sizes. A one-algorithm generator forces you to install OpenSSL and read man pages; a three-algorithm generator gives you the same key, the same file format, and the right algorithm for whatever is on the other end.

## What PEM, Hex, and Base64 actually are

After the math, the tool has to hand you the result in a form you can store. This is where most people encounter the second surprise: the same key, encoded three different ways, can look like three completely different strings.

**PEM** is the format you have probably copied. It is base64 wrapped in `-----BEGIN PUBLIC KEY-----` and `-----END PUBLIC KEY-----` headers. The headers are not just decoration. They tell parsers what algorithm the key is for, what encoding the body is in, and what software generated it. A PEM public key is a complete, self-describing artifact that any tool written in the last thirty years can read.

**Hex** strips the headers and converts the base64 to hexadecimal. The byte that was 0x4d in base64 becomes "4d" in hex. Hex is sometimes easier to paste into a config file, a smart contract, or a small embedded system that does not have a base64 decoder.

**Base64** strips the headers but keeps the original encoding. This is the smallest text representation. It is what you would paste if you needed to embed a key in a URL, a JSON blob, or a database column with character limits.

All three encode the same key. The bytes on disk after decoding are bit-for-bit identical. Pick whichever the tool on the other end expects.

## Why the private key is the half you must protect

If the public key is the mailbox and the private key is the metal key, the practical advice is obvious: never copy the private key anywhere you do not trust. Never paste it into a chat window, never commit it to a git repo, never upload it to a public artifact server. The day someone else holds that key, the asymmetry collapses, and they are you.

This is why production systems use a Key Pair Generator inside a CI pipeline, not as a copy-paste step. The tool generates the pair, hands the public key to the deployment system, and stores the private key directly into a secret manager like HashiCorp Vault, AWS Secrets Manager, or Kubernetes secrets. The human never sees the private half. The risk is not that the algorithm breaks — the risk is that the half that is supposed to stay private ends up in a Slack message, a blog post, or a stack trace.

## The deeper implication

What makes a key pair generator feel almost philosophical is how much trust it loads onto a single click. The button does not "create" security. It creates a math problem. The security is whatever the math problem is worth to an attacker. For 2048-bit RSA in 2026, that worth is "the heat death of the universe." For 1024-bit RSA, that worth fell below "any well-funded nation-state" around 2010. The button does not warn you about this. The dropdown for key size is usually a single line.

The take-home is not "click the button." The take-home is that the button is a contract. It promises you security as long as the math holds, and it asks you, in exchange, to keep one half of the math problem off every screen, every repo, and every chat window the world can read. The public key can live forever on a billboard. The private key should live on exactly one device, and the day it leaves, the contract is over.

[Explore it yourself at Elysia Tools](https://elysiatools.com/en/tools/key-pair-generator) — pick RSA, ECC, or Ed25519, copy the public key, and try pasting it into `ssh-add -L` or a JWT library. The math is invisible, but the asymmetry is real, and it is the reason every login box, every signed commit, and every HTTPS connection in the world is shaped the way it is.
