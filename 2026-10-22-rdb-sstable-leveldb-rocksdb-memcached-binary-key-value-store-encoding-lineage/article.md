A Redis RDB file is not a database. It is a tape. That distinction decides how you read one. A tape has a magic number, a declared format version, a stream of typed records that moves forward and never looks back, and a trailing checksum that tells you whether the read landed. Redis snapshots, LevelDB and RocksDB write-ahead logs, SSTable footers, Memcached wire packets, BoltDB pages and LMDB pages are all tapes in this sense, and the forensic question is never what the store contained but what the byte stream claims and whether its own integrity check agrees.

The [RDB SSTable LevelDB RocksDB Memcached Binary KV-Store Encoding Lineage decoder](https://elysiatools.com/en/tools/rdb-sstable-leveldb-rocksdb-memcached-binary-key-value-store-encoding-lineage) walks six storage formats in one browser tab, detects which one a hex blob actually is, expands every header and record field, verifies the checksum that format carries, and — when you paste a second snapshot — reports which keys appeared, vanished, changed value or drifted on TTL.

## The tape metaphor: what six formats share

Six formats sound like six unrelated specifications. Structurally they are one idea in six costumes.

Every one opens with a **magic signature** so a reader can refuse to continue if the bytes are not what it expected. Redis writes the nine ASCII bytes `REDIS0011` at the head of every RDB file, where the trailing digits are the format version. LevelDB's log begins each record with a 7-byte header whose first byte carries the record type. Memcached's binary protocol marks a response by the high bit of the first byte, `0x80`.

Every one then declares **what kind of record follows** before the payload. In RDB a single byte selects string, list, set, hash, zset or one of the auxiliary opcodes. In the LevelDB log that byte is `1` for a full record, `2` for a first fragment, `3` for a middle fragment and `4` for the last fragment of one logical record split across a block boundary.

Every one ends with **an integrity check** over what was read. RDB closes with a CRC-64 (Jones polynomial, reflected). LevelDB's per-record CRC32C is masked before it is written. Memcached ships no trailing checksum at all — which is itself a finding.

Treat the family as a lineage, not a list. Streaming versus index versus page is the axis that predicts which byte answers which question: RDB and the LevelDB log stream records forward, the SSTable footer is a fixed-width index at the *end* of a file whose data blocks come before it, and BoltDB and LMDB pages are fixed-size slotted pages.

## Reading an RDB header and its AUX fields

Start with the simplest file in the family, because it teaches the grammar the others reuse.

The nine magic bytes carry two facts. `REDIS` is the signature. The four digits after it are the RDB version — for the test corpus's real 431-byte snapshot from redis-server 7.2.4, that reads 11. Immediately after come AUX field pairs, each an opcode byte `0xFA` followed by a length-prefixed key and value. The example decodes `redis-ver` to `7.2.4` and `redis-bits` to `64`. Check those two first in any investigation: a snapshot claiming version 11 while reporting `redis-bits: 32` tells you a 32-bit build produced it.

Length prefixes in RDB are not a fixed width. A first byte below `0x40` is itself the length. A first byte with top two bits `01` means a 14-bit big-endian length follows. Top two bits `10` means a 32-bit length follows, encoding a special case at the top of the range. That three-way branch is why a naive "read one length byte" parser derails on any snapshot containing a large value.

Once AUX fields end, opcode `0xFE` selects a database index and `0xFB` announces the resizedb hint. Those two opcodes mark where header ends and keyspace begins.

## The opcodes that carry your data

Every key is announced by a type byte, and that byte chooses the layout of everything after the key string.

Plain strings use two well-known encodings. `0xC0` is an integer-encoded string whose payload is a little-endian signed value of 1, 2, 4 or 8 bytes, determined by the low bits of the encoding byte; a zero-length variant is the canonical **null**. Anything else in the `0xC0` family is a plain string with a length-prefixed payload. In the worked example, `greeting` decodes through an integer-encoded path to `hello world`, while `name` decodes as a plain string to `Ada`.

Containers are where the format gets interesting. A small hash uses **listpack** encoding — one contiguous run of bytes holding every field and value with back-references — and a zset can do the same. A small set of integers uses **intset**, a sorted array of fixed-width integers with a count in its header. A short list is stored as a **quicklist**, a linked chain of listpack nodes rather than individually allocated nodes. The example's `hobbies` key unpacks from one listpack payload into six named fields.

Two opcodes matter in a truncated or tampered file: `0xF8` is a 64-bit **module aux** field and `0xF7` is a module payload, both signalling custom opcodes you need module source to interpret. And the file's final eight bytes are the CRC-64 trailer — in the example that trailer verifies, which is the difference between "this is a Redis snapshot" and "these bytes merely start with the word REDIS".

## Verify the CRC-64 before you believe anything

Integrity checks are where format knowledge converts into forensic confidence, because the checksum covers the entire body and therefore validates every field you decoded before it.

Three checksums appear here and they are not interchangeable. RDB uses **CRC-64** Jones reflected. The LevelDB and RocksDB log uses **CRC32C** (Castagnoli), masked before storage — a masking step that exists so a CRC value can never be mistaken for a valid length field during recovery. Memcached has no trailing checksum, so a truncated chain has no self-report of its own truncation.

The masked-CRC32C detail bites people. If you recompute Castagnoli over the payload and it disagrees with the stored value, the mismatch may be entirely an artifact of forgetting the mask. Recovering a log record means checking both the masked value as written and the unmasked value your library returns, because libraries almost universally return the unmasked form.

What a checksum buys is narrow but real. A clean CRC-64 means the snapshot is internally consistent. It does not mean it is the snapshot you wanted, and it does not mean the data is correct. It means no byte was flipped, truncated or reordered in transit, so any semantic oddity you find originates in the data or the writer, not the transfer.

If the checksum fails, the decoder still reports every field it could parse. That partial decode is often more useful than a hard failure: it marks the offset at which the file stopped being trustworthy, and everything before it is still evidence.

## WAL records, blocks and the 32 KiB boundary

The write-ahead log is where this lineage diverges from the snapshot in a way that changes your reading strategy. An SSTable is immutable and sorted; a log is neither.

The log is a sequence of 32 KiB blocks, and the block boundary is a hard physical constraint. A record that does not fit the remaining space is split, and fragments are marked by their type byte so the reader can reassemble them. Each record carries a 7-byte header: one byte of length (split across low and high length bits past 256), two bytes of log number, two bytes of payload length, and two bytes of masked CRC32C. The header length is the *total* logical length including its own header and checksum, while the payload-length field is the payload alone — reading those as one number is a classic off-by-seven that desynchronises the stream.

A tail of garbage in the log is not evidence of corruption. It is the normal residue of a crash between a partial write and its completion; modern LevelDB and RocksDB truncate at the last valid checksum.

SSTables are almost the mirror image. The **footer is a fixed-width block at the end of the file**, carrying varint64 BlockHandle pairs (offset and size) for the metaindex and index blocks, a varint32 metaindex handle, padding to 40 bytes, then a 40-byte magic. Inside the data blocks, **prefix compression** and **restart points** do the compression: every restart interval opens with a shared-key offset of zero, and entries between restarts share a prefix with their predecessor — so a naive reader treating every key as complete produces garbage for most entries. Varints are not self-delimiting either; the final byte carries the continuation flag.

## Memcached packets: headers without a checksum

Memcached inverts the safety property the on-disk formats rely on. There is no trailing checksum, so the 24-byte header is the entire contract.

The header is eight fields in fixed order: request or response magic, opcode, key length, extras length, data type, vbucket or status, total body length, and an opaque identifier a client matches responses against. Request and response magic differ only in the high bit of the first byte, which is why auto-detection treats `0x80` as the response marker. The rest of the packet is extras, then key, then value, in that order.

Opcodes are the whole vocabulary: `0x00` get, `0x01` set, `0x02` add, `0x03` replace, `0x04` delete, `0x05` increment, `0x06` decrement, `0x07` quit, `0x08` flush, plus the stats family. Getting extras length wrong shifts every subsequent field, so a decoder must treat the declared extras length as the authority for where the key begins.

The tool's second worked example pastes five packets back to back — a GET for "Hello", its hit response carrying flags and value "World", an ADD with flags and expiry extras, a VERSION response reporting 1.3.1, and a key-not-found error. The decoder reports five packets, two requests, three responses, and `Hello` as the first key. That example is worth more than the opcode table, because it shows the same offset arithmetic surviving a packet with no value, one with a value, and one that is an error.

A packet chain is also the only place in this family where **truncation is detectable from the stream alone** — if the sum of declared body lengths does not equal available bytes, the chain is short.

## Diffing two snapshots and reading the TTL matrix

The diff is what makes this a tool rather than a decoder, and its five categories map onto the questions an investigator actually asks: **added**, **removed**, **changed**, **expiry-changed** and **unchanged**.

In the worked example, a second SAVE taken after editing keys produces exactly one added key, one removed key, one changed value, one expiry drift and seven unchanged keys — which reads in plain language as "someone added a key, deleted a key, rewrote one value and refreshed one TTL". Each is reported as a separate number rather than collapsed, and that is the point: a TTL drift with identical bytes is invisible to a byte-level diff and is exactly the signal you would otherwise miss.

The matrix needs one input from you, a reference Unix timestamp. Expiry is stored as an absolute Unix second count, or as a 4-byte little-endian millisecond count in the modern `0xFC` opcode that replaced the older 1-byte and 4-byte-second absolute encodings. Without a reference time you can report *that* a key expires but not whether it expired before or after the incident you are investigating. Supplying one turns the matrix into a timeline: expired already, expires within the hour, later today, never expires.

It also decides what an apparently missing key means. A key absent from snapshot B was either deleted or expired, and those have different causes. The expiry matrix resolves the ambiguity when the key is present in A with an expiry falling between the two saves.

Treat the diff as evidence, not as a diff of intent. It reports bytes and timestamps. Concluding that an operator did it rather than a scheduled job is a separate inference needing corroboration — but the byte-level facts are now in one place instead of reconstructed from two hex dumps by hand.

## A pre-commit checklist before you trust a decode

Five checks decide whether a decoded keyspace can carry the weight of an investigation, and running them in order saves the expensive kind of confidence — the kind you only discover was wrong when someone else re-reads the file.

**Confirm the magic before reading a field.** The detected format is a claim made before parsing. If it is not the format you expected, stop and find out why before spending time on contents.

**Check the integrity verdict and treat failure as a truncation point.** A valid CRC-64 or CRC32C means every byte before it is trustworthy. A failure means untrustworthy from that offset on, and the partial decode before it is still usable.

**Verify the header fields that move every subsequent offset.** For a Memcached packet that is the extras length; for a LevelDB record the two competing length fields; for hex input generally whether you pasted contiguous hex with no stray separators and no odd nibble count.

**Reconcile the key count against the diff categories.** If snapshot A holds ten keys and the diff says one added and one removed, snapshot B must hold ten too. A mismatch means one of the three numbers is wrong, and it is cheaper to find that here.

**Write the reference timestamp down with the output.** Expiry conclusions are meaningless without the Unix second you evaluated them against.

Run all five and the decode is evidence. Skip one and it is a plausible story, which is harder to notice. For the integrity side specifically, the [CRC32 Checksum calculator](https://elysiatools.com/en/tools/crc32-checksum) computes Castagnoli over your own bytes — the fastest way to confirm whether a masked value in a log header survived the round trip. When the question is "what is actually in this file" rather than "what does this format mean", the [Hex Editor](https://elysiatools.com/en/tools/hex-editor) is the right stop. And for readable payload structure instead of a byte stream, the [MsgPack converter](https://elysiatools.com/en/tools/msgpack-converter) shows the same length-prefix and type-tag thinking in a format you can read, while the [Protobuf converter](https://elysiatools.com/en/tools/protobuf-converter) covers wire types that RDB's integer encodings resemble. Browse the rest at [elysiatools.com/en/tools](https://elysiatools.com/en/tools).