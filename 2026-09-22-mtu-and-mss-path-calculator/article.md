---
title: "MTU / MSS Path Calculator Field Guide: When Eight Encapsulation Layers, the 40-Byte MSS Rule, and the Don't-Fragment Ping Probe Decide Whether Your SD-WAN Packet Clears 1500 Bytes or Black-Holes at 1404"
slug: mtu-and-mss-path-calculator-field-guide-when-eight-encapsulation-layers-the-40-byte-mss-rule-and-the-dont-fragment-ping-probe-decide-whether-your-sd-wan-packet-clears-1500-bytes-or-black-holes-at-1404
tool: mtu-and-mss-path-calculator
date_gmt: 2026-09-22T11:17:20
---

<strong>An overlay that drops packets is rarely a routing problem; it is a frame-size problem wearing a routing costume.</strong> If you have ever watched a TCP session hang at 1 KB/s the moment it crosses a VXLAN tunnel, or seen a curl between two k8s pods inside the same node silently time out while `ping -M do -s 1472 10.0.0.1` returns `Message too long`, the path MTU between two endpoints is smaller than you assumed, and the difference is exactly the size of every tunnel header the packet has accumulated on its way down. The [MTU / MSS Path Calculator](https://elysiatools.com/en/tools/mtu-and-mss-path-calculator) takes five inputs — interface MTU, encapsulation stack, inner IP version, TCP header size, and any custom per-layer overhead — and produces three numbers that an SRE or SD-WAN engineer actually needs: the effective MSS after IP + TCP headers, the largest payload that survives end-to-end without fragmentation, and the exact `ping -M do -s` byte count that verifies the path with a single ICMP probe.

## Why a 1500-Byte Ethernet Frame Becomes a 1372-Byte Working Payload

The IPv4 path MTU contract is simple in theory and brutal in practice: every link along the route must carry a packet no larger than its own MTU, and the path MTU is the smallest of those. On a clean datacenter fabric that number is 1500 — Ethernet's default. The moment you stack GRE inside VXLAN inside WireGuard inside a VLAN tag inside a PPPoE session header, every one of those layers eats bytes from the 1500 budget before your application payload gets a turn, and IPv4 forbids routers from fragmenting mid-flight when the DF (Don't Fragment) bit is set, which is the default for every modern TCP stack and for `ping -M do`.

The math is small but unforgiving. A `vlan,pppoe` stack adds 4 (VLAN 802.1Q) + 8 (PPPoE session) + 2 (PPPoE PPP protocol ID) = 14 bytes of overhead between the Ethernet header and the IP payload, dropping the result on the wire from 1500 to 1486. If the inner payload is IPv4 + TCP, the IP header is 20 bytes and the TCP header is 20 to 60 bytes depending on options. With no TCP options, the MSS you can advertise safely is `1500 - 14 - 20 - 20 = 1446` bytes. With a single timestamp option pair (TSval + TSecr + 4 bytes of NOP padding), the TCP header grows to 32 bytes and MSS drops to `1500 - 14 - 20 - 32 = 1434`. Add WireGuard4 on top and the budget shrinks another 32 bytes; add GRE and another 24; add a second VLAN tag for QinQ and another 4. The total frames in a typical SD-WAN path — VLAN + VXLAN + WireGuard + GRE + IPv6 inner — easily consumes 80+ bytes of overhead before your application sees a byte.

## The Five Inputs the Calculator Expects

The tool exposes five controls, and each one carries a specific failure mode when set wrong.

**Interface MTU (bytes)** is the link MTU of the egress interface the overlay sits on. The default of 1500 is right for almost every modern Ethernet NIC, but it is wrong for three common cases: jumbo-frame interfaces (set this to 9000), loopback interfaces on Linux where you might want to test the inner MTU only (set this to 65535), and tunnel interfaces whose own MTU has already been lowered by `ip link set dev wg0 mtu 1420` to fit a smaller underlay.

**Encapsulation stack** is the comma-separated list of layers from outermost to innermost. Valid values are `vlan`, `qinq`, `pppoe`, `gre`, `gre_checksum`, `vxlan`, `geneve`, `wireguard4`, `wireguard6`, `ipsec_transport`, and `ipsec_tunnel`. Order matters: `vxlan,wireguard4` is a WireGuard tunnel carrying VXLAN, which adds 32 + 8 = 40 bytes; `wireguard4,vxlan` is a VXLAN tunnel over WireGuard, which adds 8 + 32 = 40 bytes (commutative in this case but not in every stack — IPsec transport mode does not include its own IP header, so it stacks differently from IPsec tunnel mode).

**Inner IP version** flips between IPv4 (20-byte header) and IPv6 (40-byte header) for the IP header size that gets subtracted along with the TCP header. IPv6 has a fixed 40-byte header (no `header.length` field, no options in the base header, with extension headers if any). Pick the version that matches the IP stack of the application whose traffic you are sizing.

**TCP transport header (bytes)** is the TCP header size, not the TCP MSS. The default of 20 is the bare TCP header with no options. The maximum of 60 accounts for a fully-populated options section (12 dwords × 4 bytes = 48 bytes of options + 20 of base header). Common in-the-wild values are 32 (one timestamp option pair, 12 bytes) and 44 (timestamp + SACK-permitted + two SACK blocks).

**Custom per-layer overhead (bytes)** is the escape hatch. Use it when your stack includes a layer the tool does not model: a vendor-specific MPLS label (4 bytes), a CAPWAP header (8 bytes), an ERSPAN type II encapsulation (20 bytes), or anything else. Adding 4 bytes here subtracts 4 bytes from the result.

## Reading the Three Outputs Without Misreading Them

The tool returns three numbers, and confusing them is the single most common mistake engineers make when sizing an overlay.

**Effective MSS** is the maximum segment size you can advertise in the TCP SYN without forcing the kernel to fragment. It already subtracts the IP header, the TCP header, and every encapsulation byte, so it is the number you configure with `iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu` or with the equivalent NM `tcp-mss` knob. The standard practice of clamping to `MTU - 40` works when the underlay is clean (no tunnel overhead) and the TCP header is bare. With tunnels in the path, the right clamp is whatever the tool reports, not `MTU - 40`.

**Max payload (no fragmentation)** is the largest UDP payload or non-TCP application datagram that fits end-to-end without forcing any hop to fragment. Use this number when sizing UDP-based protocols (RTP, VXLAN itself, QUIC datagrams before the connection is established, DNS responses over TCP fallback, NFSv3 writes, iSCSI PDUs). Note that QUIC's initial MTU is 1200 by RFC 9000 §14.1, so even on a clean path the QUIC initial datagram must respect the 1200-byte lower bound regardless of what the path supports.

**DF ping probe size** is the argument to pass to `ping -M do -s <N> <host>`. The Linux `ping` `-s` flag specifies the ICMP payload size, NOT the total packet size; the kernel adds 8 bytes for the ICMP header and 20 bytes for the IP header automatically. So a `-s` value of 1472 produces a 1500-byte ICMP packet, and the ICMP packet must equal the path MTU for the probe to succeed. If `ping -M do -s 1472 host` returns `Message too long` but `ping -M do -s 1464 host` succeeds, the path MTU is 1464 + 8 + 20 = 1492 — almost certainly a PPPoE link, since PPPoE consumes 8 bytes and brings 1500 down to 1492. The calculator emits the `-s` value, not the total packet size, because that is what you type into the shell.

## The Three Rules That Decide Whether the Path Is Real

Rule one: every hop along the route honors the DF bit. This is true for every modern router but breaks for IPsec gateways in tunnel mode that decrypt and re-encrypt without honoring the inner DF — in which case the path MTU you measure is the path MTU of the encrypted tunnel, not the path MTU of the inner packet. Set `ip tcp adjust-mss` on the tunnel endpoints to clamp MSS at the boundary or the inner session will still see stalls.

Rule two: the inner TCP stack advertises the clamped MSS, not the local interface MTU. On Linux the `net.ipv4.tcp_mtu_probing` sysctl (off by default before kernel 4.19, on by default after) controls whether the kernel probes for a smaller path MTU after a black-hole detection event. With the sysctl off, the kernel will not shrink the advertised MSS even after seeing ICMP "fragmentation needed" replies, and the session will stall on every retransmit until something times out.

Rule three: the application trusts the kernel's MSS, not its own MTU constant. Go's `net.Dialer` and Node.js's `net.Socket` both pull MSS from the kernel via `getsockopt(TCP_MAXSEG)` and respect it on the first send; raw socket libraries that hard-code 1500 will fragment one frame on the first send of every connection. If you are debugging a vendor SDK that ships a hard-coded `MTU=1500`, the bug is in the SDK, and the fix is `TCP_MAXSEG` clamp at the socket layer.

## Worked Example: VXLAN over WireGuard over VLAN

Stack: VLAN (4) + WireGuard4 (32) + VXLAN (8) + IPv6 inner (40) + TCP with timestamps (32). Interface MTU 1500. Total overhead: 4 + 32 + 8 + 40 + 32 = 116 bytes. Result MSS: `1500 - 116 = 1384`. Max payload: `1384 - 32 = 1352` bytes for the TCP payload only (subtracting TCP header again). DF ping probe size: `1500 - 116 + 8 = 1392` for ICMP payload — wait, that's not quite right. The ICMP echo itself is 8 bytes, the IP header is 40 (IPv6), and the encapsulated path is the inner IPv6 path. The probe becomes `-s 1352` if you want to test against the inner MSS, or `-s 1392` if you want to test against the inner IP packet size. The calculator returns the right one.

Try this exact configuration in the [MTU / MSS Path Calculator](https://elysiatools.com/en/tools/mtu-and-mss-path-calculator) and compare to a bare 1500-byte frame — the 1384 vs 1460 difference is what kills MTU-discoverable protocols that hard-code their MSS.

## Common Stack Footguns

`pppoe` is the most common surprise — it adds 8 bytes for the PPPoE session header and 2 bytes for the PPP protocol ID, totaling 10 bytes, and a typical home broadband link on PPPoE has a 1492-byte MTU, not 1500. If your VPS dashboard says MTU 1500 but the actual underlay is PPPoE, every TCP session will silently lose the first retransmit at 4 KB and look like a flaky network until you clamp MSS to 1452.

`wireguard4` vs `wireguard6` matters only when the underlay is IPv6 — the 32-byte overhead is the same, but the keepalive packet format differs and most SD-WAN stacks route differently.

`qinq` (stacked VLAN, 802.1ad) adds 8 bytes total, twice the single VLAN overhead. Carrier networks use QinQ for customer-VLAN isolation across metro Ethernet; if you are running QinQ without knowing it, the inner MSS drops by 8 bytes relative to your single-VLAN assumption.

`gre_checksum` adds 24 bytes (GRE header + optional checksum + optional key + optional sequence) vs the bare 24 bytes for `gre` — same in this calculator, but on real NICs the `gre_checksum` variant enables hardware checksum offload that silently rewrites the packet and changes the effective overhead by 4 bytes if the key field is populated.

`ipsec_transport` adds 36 to 52 bytes depending on the cipher (AES-GCM-128 with 128-bit ICV is 36; AES-CBC with HMAC-SHA256 is 52). `ipsec_tunnel` adds another 20 (IPv4) or 40 (IPv6) bytes for the outer IP header that transport mode omits. Pick the wrong one and your MSS estimate is off by a full IP header.

## Verifying the Path with One Ping

Once you have the DF ping probe size from the calculator, run `ping -M do -s <N> <host>` from one endpoint to the other. If the probe returns without `Message too long`, the path MTU is at least `N + 28` (IPv4) or `N + 48` (IPv6). If it returns `Message too long`, the kernel also tells you the next-hop MTU it learned from the ICMP "fragmentation needed" reply — that number is the ground truth for path MTU and supersedes whatever the calculator reported.

Run `ping -M do -s <N+1> <host>` next — if it also fails with the same next-hop MTU, the path MTU is definitively `N + 28` and the calculator's prediction was correct. If `N+1` succeeds, the path supports one byte more than you assumed and you can raise the clamp by 1.

For SD-WAN paths that traverse multiple ISPs, run the probe during peak and off-peak hours — congestion-driven fragmentation occurs when a link's queue fills and the active MTU shrinks below the configured MTU, which the calculator cannot predict because it sees only the static configuration, not the live underlay. The deeper packet-loss picture that drives those fragmentation events is the kind of thing a paired [HTTP/3 QUIC Handshake Anatomy](https://elysiatools.com/en/tools/http-3-quic-handshake-anatomy) walk makes visible — QUIC's 1200-byte initial datagram lands exactly in the danger band between a 1500-byte clean path and a tunnel-shrunken SD-WAN underlay.

## Where This Stops Being Useful (And What to Pair It With)

The tool is deterministic given a fixed encapsulation stack, but real overlay paths change. A load balancer that adds an X-Forwarded-For header is application-layer, not network-layer, and does not consume MTU. A CDN that terminates TLS at the edge adds an outer IP header (20 bytes IPv4 or 40 IPv6) bytes for the TLS termination point that the calculator does not know about. A service mesh that does sidecar injection (Istio, Linkerd) adds an outbound IP header on every hop between sidecars — model this as `ipsec_tunnel` × N where N is the number of sidecars in the request path.

For mobile paths (4G/5G), the underlay MTU is often 1428 or smaller, and the carrier may transparently fragment or drop oversize packets in violation of RFC 791. The calculator's static result will overstate the working MSS by 70+ bytes; treat its output as the upper bound and probe the live path with `ping -M do` before sizing any production workload that crosses cellular. When the underlay is IPv6 the same numbers shift by 20 bytes (IPv6 base header is 40 vs IPv4's 20, so the path MTU grows by 20 but the ICMP probe also grows by 20), which is easy to model in the calculator but easy to forget when you actually run the probe — verify the IP family of every hop with a paired [CIDR Calculator](https://elysiatools.com/en/tools/cidr-calculator) check on the prefix allocations before trusting the result.

For path MTU validation on raw IPv4, pair with any `ping -M do` implementation. For IPv6, pair with `ping6`; the `-M` flag is `do` on both. For path MTU on Linux with policy routing, pair with `ss -i` to confirm the kernel's view of MSS on a live socket, not just the configured clamp. For tracing which hop on a long path is shrinking the MTU, pair with a Paris-traceroute build (`paris-traceroute` or `scamper` with the `trace` command); standard traceroute uses 28-byte UDP probes that fit on any 1500-byte path and will not surface path MTU at all, while Paris-traceroute varies the packet size to discover the link MTU on every hop. For sizing overlay MTU in advance of any deployment, pair with a deployment-time audit script that compares the configured `iptables -t mangle -L -v` MSS clamp against the calculator's prediction — a mismatch is the most common cause of "it works in dev, stalls in prod" SD-WAN bugs. For multi-region replication where the inter-region link is the bottleneck, pair with a continuous `pmtud` daemon (the kernel does this when `net.ipv4.tcp_mtu_probing=1`, but a daemon logs every change and surfaces it to your monitoring). The calculator gives the static prediction; the daemon gives the live truth.

Try the [MTU / MSS Path Calculator](https://elysiatools.com/en/tools/mtu-and-mss-path-calculator) with your actual tunnel stack, then probe the result with `ping -M do -s <N>` against the worst-case path between your endpoints. The two numbers should match within 1 byte; if they do not, the underlay is doing something the calculator does not know about, and the right fix is a tcpdump on the egress interface to see what the kernel is actually transmitting. For more network and infrastructure tools, browse the [full tool catalog](https://elysiatools.com/en/tools).