# 5 Ethereum Smart Contract Examples Every Developer Should Know

The Ethereum ecosystem has over $50 billion in total value locked — and it all runs on smart contracts written in Solidity. Whether you're building your first token or a full DeFi protocol, seeing real working code beats reading docs any day.

Here are **5 complete Solidity examples** available free on [ElysiaTools.com](https://elysiatools.com/en/samples/ethereum-solidity) — no sign-up, no setup, just code.

---

## 1. Solidity Fundamentals & Basic Smart Contract

Most tutorials start with `Hello World`. This one starts with a **voting contract**.

You'll learn:
- State variables, mappings, and structs
- Function modifiers (`onlyOwner`, `validAddress`, `costs`)
- Events — the smart contract equivalent of `console.log`
- Ether handling: `payable`, `receive()`, and `fallback()`
- A complete `SimpleVoting` contract with time-limited voting

The `SafeMath` library section also shows you how to prevent the integer overflow bugs that plagued early DeFi.

**[Try it →](https://elysiatools.com/en/samples/ethereum-solidity)**

---

## 2. ERC-20 Token Standard Implementation

ERC-20 is the backbone of the token economy. Over 500,000 ERC-20 tokens exist. This example goes far beyond a basic `transfer()` function.

It includes:
- Complete ERC-20 interface (totalSupply, balanceOf, transfer, approve, transferFrom)
- **Pausable** — freeze all transfers during an emergency
- **Token locking** — cliff and vesting schedules
- **Blacklist** — block specific addresses
- **Batch operations** — transfer to hundreds of addresses in one tx
- Voting power tracking tied to token balance

This means: you get a production-grade token with admin controls, without touching OpenZeppelin's source.

**[Try it →](https://elysiatools.com/en/samples/ethereum-solidity)**

---

## 3. ERC-721 NFT Contract with Metadata

The ERC-721 standard is more complex than ERC-20 because every token is unique. This example covers the full implementation.

Highlights:
- Full `IERC721`, `IERC721Metadata`, and `IERC721Enumerable` interfaces
- **IPFS-ready metadata** — tokenURI points to off-chain data
- **Royalty system** — set a percentage that auto-goes to creators on every resale
- **Marketplace integration** — list, delist, and buy NFTs directly
- Enumerable extension: iterate all tokens an address owns
- Batch minting for NFT drops

If you've wondered how OpenSea's smart contracts work under the hood, this is the answer.

**[Try it →](https://elysiatools.com/en/samples/ethereum-solidity)**

---

## 4. DeFi Automated Market Maker (AMM) Protocol

This is the most advanced example — a Uniswap V2-style AMM from scratch.

What it does:
- **Liquidity pools** — users deposit token pairs, earn fees
- **Constant product formula** (`x * y = k`) for swap pricing
- **Slippage protection** — `getAmountOut` calculates minimum output
- **Yield farming** — governance tokens distributed proportional to liquidity provided
- Multi-hop swaps through multiple pools
- Emergency withdrawal for admin

The swap formula alone is worth studying: it explains why even a $1B pool can be manipulated by a $10M trade — and why MEV (Maximal Extractable Value) exists.

**[Try it →](https://elysiatools.com/en/samples/ethereum-solidity)**

---

## 5. Hardware Wallet Integration & Multi-Sig

Code is only as secure as the keys that control it. This example covers production-grade key management.

Covers:
- **Ledger integration** via WebHID/WebUSB
- **Trezor** via TrezorConnect
- **Multi-signature wallet** — require 2-of-3 owners to execute a transaction
- Transaction proposal → signing → execution workflow
- PBKDF2 key derivation and AES-256-GCM encryption for key storage
- Hardware-signed messages vs. metamask-signed messages

This is how you build a treasury wallet that can't be compromised by a single private key leak.

**[Try it →](https://elysiatools.com/en/samples/ethereum-solidity)**

---

## One Problem Nobody Talks About

All of these examples run on **Solidity 0.8.19**. But Solidity 0.9.x is around the corner, with breaking changes to error handling and assembly. 

The real skill isn't writing a contract — it's writing one that **still works** when you upgrade the compiler. ElysiaTools keeps these examples updated with every breaking change, so you're always learning the latest version.

**Explore all 5 examples → [ElysiaTools.com](https://elysiatools.com/en/samples/ethereum-solidity)**
