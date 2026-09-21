A BGP best-path decision collapses to two questions the moment a prefix lands in your routing table: *is the path a loop*, and *is it the best of what survived*. The Elysia Tools [BGP AS Path Loop Policy Sandbox](https://elysiatools.com/en/tools/bgp-as-path-loop-policy-sandbox) answers both in one deterministic pass — and it does so without a router, a session, or a peer's permission slip.

Explore more tools at [elysiatools.com](https://elysiatools.com/en/tools).

<strong>BGP best-path selection is a sandbox problem, not a hardware problem.</strong> Most engineers first encounter AS_PATH loop detection in the wild, when a misconfigured customer prepend pulls traffic across the ocean and back. The sandbox tool lets you feed in JSON-formatted route entries, JSON-formatted policy rules, and a default action — then it runs the same algorithm your edge router would run: scan the AS_PATH, reject any path containing the local AS, apply your prefix rules, and pick the winner by LocalPref, then by AS_PATH length, then by origin. The whole thing is reproducible, offline, and free. No need for a GNS3 VM, no need for a router image, and no need to file a change-window ticket for what is, fundamentally, a string-comparison problem.

## What the Sandbox Actually Does (and What It Skips)

The tool has five inputs and one boolean output: it returns the route entries that survive your policy, plus the winner if `selectBestPath` is on. The five inputs are:

<ul>
<li><strong>Local AS</strong> — a 32-bit integer (default `64500`) representing your own autonomous system number. The loop check rejects any AS_PATH containing this value.</li>
<li><strong>Route Entries (JSON)</strong> — an array of objects, each with `prefix`, `asPath` (space-separated ASNs), `localPref`, `med`, and `origin` (`igp`, `egp`, or `incomplete`).</li>
<li><strong>Policy Rules (JSON)</strong> — an array of objects, each with `name`, `action` (`permit` or `deny`), optional `prefix`, and optional `setLocalPref`.</li>
<li><strong>Default Action</strong> — what happens to a route that no rule matches: `permit` or `deny`.</li>
<li><strong>Select Best Path</strong> — a boolean that triggers the deterministic best-path algorithm on the surviving routes.</li>
</ul>

What it skips is just as important: it does not simulate the BGP finite-state machine, does not maintain an Adj-RIBs-In or Loc-RIB, does not speak TCP/179, and does not advertise anything to a peer. It is a decision table, not a router. Treat it like a unit test for your prefix-list intent.

## Five Numbers the Tool Reads On Every Route Entry

Every route entry carries five fields. The sandbox reads each one in a fixed order, and the order matters.

<ul>
<li><strong>prefix</strong> — CIDR (`203.0.113.0/24`). The sandbox matches prefix exactly; it does not aggregate. If your policy rules reference `203.0.113.0/24` but your route carries `203.0.113.0/25`, the rule does not fire.</li>
<li><strong>asPath</strong> — space-separated ASNs left-to-right, with the most recent AS first (`64501 64496`). Loop detection walks the string looking for the local AS. Origin ASN (leftmost) is the neighbor that advertised the route.</li>
<li><strong>localPref</strong> — 32-bit integer, higher wins. Only meaningful within your own AS (it does not transit). Default `100`. Policy rules can rewrite this with `setLocalPref`.</li>
<li><strong>med</strong> — MULTI_EXIT_DISC, 32-bit integer, lower wins. Used between two BGP peers in the same AS to break ties.</li>
<li><strong>origin</strong> — `igp` (originated via network statement), `egp` (legacy, from redistributed EGP), or `incomplete` (redistributed from another protocol). The best-path algorithm prefers `igp` > `egp` > `incomplete`.</li>
</ul>

Get any one of those wrong and the best-path output is wrong. The sandbox surfaces the inputs as parsed values, so you can spot a typo in `asPath` (extra space, missing ASN) before it propagates.

## How the Loop Check Walks a Single AS_PATH String

Loop detection is the cheapest and most consequential part of the algorithm. Given local AS `64500` and an AS_PATH like `64501 64496 64500 64499`, the scan finds `64500` in position 3 and rejects the route immediately. The sandbox reports `loopCount` in the metadata so you can see exactly how many routes were rejected for this reason, separate from policy denials.

This matches real router behavior: a route that contains your own AS in the path is by definition a routing loop, and accepting it would re-advertise your own prefix back to you. In a lab, you might want to study the loop rather than reject it. The sandbox makes that explicit: turn `selectBestPath` off, feed the path in, read the `metadata.selectedPrefix` as `null` or your fallback. In production, that field should always be non-null for a healthy prefix.

## When `defaultAction` Saves You From a Silent Hole

The default-action field is the one most teams set and forget. It runs at the very end of the policy chain, after every rule has been evaluated and either matched or skipped. If no rule matches and the default is `deny`, the route is dropped. If the default is `permit`, the route survives untouched.

Most prefix lists in the wild end with an implicit deny. The sandbox makes that explicit, which is useful in two ways:

<ul>
<li>You can audit whether a missing rule would have leaked. Feed a route that no rule covers and watch whether it survives.</li>
<li>You can test the opposite default without rewriting your router config. Set `defaultAction: permit` and see what new traffic would emerge if you flipped the implicit-deny to implicit-allow.</li>
</ul>

This is the difference between a policy that *looks* safe and a policy that *is* safe. The sandbox lets you prove the second.

## How `setLocalPref` Rewrites a Winning Prefix

Policy rules can do more than permit or deny: a rule can rewrite `localPref` on a matching prefix. The shape is `{"name":"prefer customer","action":"permit","prefix":"203.0.113.0/24","setLocalPref":200}`. After the rule fires, every surviving route for that prefix carries the rewritten LocalPref, and the best-path algorithm uses the new value.

The trick is the order: LocalPref is the first tiebreaker, before AS_PATH length. If two routes for the same prefix both survive the policy and you want the shorter-path route to win, leave both alone. If you want the longer-path route to win (for example, a customer route over a peer route), bump its LocalPref. The sandbox shows you the rewritten value in the per-route output so you can confirm the rewrite fired.

## Five Checks Before You Trust the Sandbox Output

The sandbox is deterministic, but it is not a substitute for thinking. Run these five checks before you commit a policy to a router.

<ul>
<li><strong>01 — Loop count</strong> — Does `metadata.loopCount` match the number of paths you intentionally fed in with the local AS embedded? If it is higher, you have a typo.</li>
<li><strong>02 — Accepted count</strong> — Does `metadata.acceptedCount` match the routes you expected to survive? Mismatches here usually mean a missing rule.</li>
<li><strong>03 — Default action</strong> — Is the default `permit` when you wanted `deny`, or vice versa? The audit will catch this only if you read it.</li>
<li><strong>04 — Best-path path</strong> — Does `metadata.selectedPrefix` agree with the route you would have picked by eye? If not, your LocalPref or AS_PATH understanding is off.</li>
<li><strong>05 — Local AS echo</strong> — Does any surviving AS_PATH still contain the local AS? It should not; if it does, the loop check missed something.</li>
</ul>

## The Sandbox Versus a Lab Router

A lab router (Cisco IOS-XR, Arista EOS, Juniper Junos, FRRouting) gives you a real session, a real Adj-RIB, and a real wire. The sandbox gives you a single algorithm run, with JSON in and JSON out. For testing prefix lists, the sandbox is faster: type six routes and two rules, run, read. For testing MED tiebreakers across two peers, the sandbox is easier: feed two routes with identical prefix but different MED and watch the algorithm pick the lower. For testing route-reflector behavior, the sandbox is wrong: it does not model cluster-list loops or originator-ID, only AS_PATH loops.

Use the sandbox for the question you ask ten times a day ("did my prefix-list do what I thought?") and use the lab for the question you ask once a quarter ("does my route-reflector cluster behave under a peer failure?"). They are different tools for different questions, and the BGP AS Path Loop Policy Sandbox is the one you keep open in a browser tab.

## When the Sandbox Says No (and That Is the Answer)

The most useful sandbox output is often a denial. Feed a route you expected to accept and watch the tool reject it; the rejection is a teaching moment, not a failure. Three patterns show up over and over:

<ul>
<li><strong>The route your peer advertised has your own AS in it.</strong> That is a loop, by definition. The sandbox rejects it before your policy runs. The fix is operational (call the peer, do not retry), not policy-shaped.</li>
<li><strong>The route has a typo in `asPath` — an extra space or a missing ASN.</strong> The loop check still finds the local AS if it is there; the typo usually surfaces in a higher `loopCount` than expected, not in a missing route.</li>
<li><strong>The policy rules match nothing.</strong> The default action then decides. If the default is `deny`, every route that should have been covered by an unwritten rule vanishes. The sandbox tells you `acceptedCount: 0` and you go write the rule you should have written.</li>
</ul>

A "no" from the sandbox is a starting point, not an endpoint. Read the `loopCount`, the `acceptedCount`, and the `selectedPrefix` together and the policy intent becomes visible. That visibility is what the tool is for.

Open the [BGP AS Path Loop Policy Sandbox](https://elysiatools.com/en/tools/bgp-as-path-loop-policy-sandbox), paste four routes and two rules, and run it. Five seconds later you will know whether your policy does what you think it does — before you push it to a router that touches real packets.