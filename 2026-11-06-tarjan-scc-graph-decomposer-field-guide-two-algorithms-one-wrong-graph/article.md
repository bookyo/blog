---
title: "Tarjan Graph Decomposer Field Guide: Two Algorithms, One Wrong Graph"
---

**Two independent algorithms reading the same wrong input will agree with each other and disagree with your graph.** I traced the source of the Tarjan SCC / Bridge / Articulation-Point Graph Decomposer on [Elysia Tools](https://elysiatools.com/en/tools/tarjan-scc-tarjan-bridge-and-strongly-connected-components-topological-order-graph-decomposer) and re-derived each number it reported. On the tool's own 7-node example the two algorithms match exactly. They also match exactly when the graph you typed is not the graph you drew. Which one is the bug?

## The cross-check is real, and it is not about your input

The tool runs several passes over one edge list. It parses the graph, runs Tarjan's strongly-connected-components algorithm, runs Kosaraju's two-pass algorithm over the reversed graph, finds articulation points and bridges with low-links, condenses the components into a DAG and orders that DAG with Kahn's in-degree method, reports cycles, and walks the graph with a depth-limited BFS and DFS.

Tarjan's pass is iterative with an explicit frame stack, using disc and low arrays and collecting components as the stack unwinds. Kosaraju's pass is also iterative: an iterative DFS records finish order, then a second pass collects components on the reversed graph. Neither recurses, so a long chain of nodes does not risk a call-stack overflow.

What the agreement badge means is narrower than it looks. The comparison sorts the members inside each component, then sorts the components themselves, so it compares the partition and not the numbering. Tarjan's component 0 and Kosaraju's component 2 can be the same set of nodes, and here they are. The table you read is Tarjan's numbering. Kosaraju's own list is computed, compared, and then discarded — the source throws it away explicitly. The badge is one boolean.

Both algorithms walk the same adjacency structure, built from your edges in the direction you wrote them. Two implementations can agree because the input is right, or because they read the same thing the same wrong way. The badge certifies the algorithms, not your graph. Since the two share an input, a disagreement would mean a genuine bug, so agreement is the expected default and it carries almost no information about the data you fed it.

One honest footnote about the footer line that claims `O(V+E)` per pass. That bound holds for Tarjan, for Kosaraju, for the low-link cut analysis, for the cycle analysis and for both traversals. The condensation's Kahn loop is the exception: it scans the whole edge list once per component it pops, so it costs `O(C x E)` in components and edges. At the scale this tool accepts you will never feel it. At 5000 nodes you might.

## One arrow per line, or the parser drops half your graph

The parser accepts an edge list — `a b`, `a -> b`, `a,b`, with an optional third numeric token — or adjacency lines of the form `a: b c`. The edge-list branch strips a separator token from the line before splitting it into fields, and that strip replaces only the first separator it finds on the line.

So one line of `a -> b -> c` becomes, after the first arrow is replaced, the field list `a`, `b`, `->`, `c`. The edge is taken from the first 2 fields, giving you `a -> b`. The literal `->` field is not numeric, so it is not read as a weight either, and it and the node `c` are discarded. The run reported 2 nodes and 1 edge instead of 3 and 2, and it reported 0 parse warnings. The node `c` does not exist anywhere in the tool's world.

Write the same intent as one edge per line and you get 3 nodes, 2 edges, and a third articulation point — `b` — that the one-line version never reported. The fix is a single newline. For example, the measured node count moves from 2 to 3, and the measured articulation count moves from 0 to 1, with no other setting touched.

The warning channel exists, but it only fires on one side of that boundary. A line with too few fields is rejected with the message `Line ignored (need "a b" or "a -> b")`. A line with too many fields is accepted and truncated, silently. The tool tells you when it discards a whole line. It stays quiet when it discards part of a line it kept.

Two more parser details are worth having in your head. A colon anywhere on a line routes that line into the adjacency branch, so `a: b -> c` creates a node literally named `->`. And a third numeric token is parsed as an edge weight and stored on the edge, where none of the passes ever reads it. The weight is accepted, carried along, and ignored.

## Writing order decides the component count

Take one undirected triangle and write it down 2 ways. The first version lists `a b`, then `b c`, then `c a`. The second lists `a b`, then `c b`, then `a c`. Untick the directed box on both.

The undirected view is identical in each case: a complete triangle on 3 nodes. The cut analysis is identical in each case: 0 articulation points and 0 bridges, because a triangle has no cut points and no bridges. The component count is not identical at all.

In the first version the adjacency is `a->b`, `b->c`, `c->a` — a directed cycle — so the component pass finds 1 component of 3 nodes and the condensation is a single node with no edges. In the second version the adjacency is `a->b`, `c->b`, `a->c` — a tree — so the component pass finds 3 components of 1 node each, and the condensation is 3 nodes with 3 edges.

Nothing was mis-parsed. No warning fired. Both runs report 3 nodes, 3 edges, and a green agreement badge. Two independent implementations confirm the same answer, and the answer describes 2 different graphs. The only panel where the difference shows up is the condensation, where it takes a completely different shape.

The general lesson: a strongly-connected-component decomposition is a statement about the directed graph you wrote, not the undirected graph you meant. If you are reasoning about an undirected structure, the component panel is not the panel that answers your question.

## The undirected checkbox only enables one panel

The "Directed graph" checkbox sounds like it changes the analysis. It changes 1 line of output.

Trace the flag through the implementation and it is read in exactly one place: the cycle analysis. All other passes read the same structures either way. Tarjan and Kosaraju read the adjacency list, which is built from your edges in the direction you typed them, always. The condensation reads the same edge list, always. The cut analysis reads the undirected projection — always, whether the box is ticked or not, which is why the tool says so under the cuts panel. The BFS and DFS traversals read the adjacency list, always.

So ticking "Directed graph" does not make anything directed. It switches on the cycle panel: the Cycle stat card, the self-loop list, the measured count of nodes sitting on cycles, and the explanation of why a full topological order does not exist.

With the box unticked, that panel says 2 contradictory things a few lines apart. The Cycle stat card reads `no`, because the analysis was skipped and there is nothing to find. The "Topological order" line reads `none (graph cyclic) — component order: SCC...`, because the order field is null and the renderer falls back to that exact string. The detail line beneath adds a 3rd variant: cycle analysis targets directed graphs. Three lines describing a graph that is not the one you are looking at.

One more asymmetry closes the panel. A self-loop is a cycle, but a self-loop is also a one-node component, and the component table prints the word `cyclic` only when a component holds more than 1 member. On the graph `a -> a`, `a -> b`, `b -> c`, `c -> b`, the cycle panel counts 3 nodes on cycles, while the component table marks the pair `{b, c}` as cyclic and shows `{a}` with no marker at all. The node sits on a cycle in one panel and not in the other.

## Seven nodes, nine edges, three components

The tool's own directed example is worth reading closely, because each number in it can be checked by hand.

The input is 7 nodes and 9 edges: `a->b`, `b->c`, `c->a`, `c->d`, `d->c`, `e->a`, `f->e`, `f->g`, `g->f`. Tarjan finds 3 components — `{a, b, c, d}`, `{e}`, `{f, g}`. Kosaraju finds the same 3 sets in a different order: `{f, g}`, `{e}`, `{a, b, c, d}`. After sorting they agree exactly, which is the badge.

The low-link pass finds 4 articulation points, `a`, `c`, `e` and `f`, and 4 bridges: `a-e`, `c-d`, `e-f` and `f-g`. The condensation has 3 nodes and 2 edges, and Kahn's method orders them `SCC2`, `SCC1`, `SCC0` — the `{f, g}` pair first, then `{e}`, then the 4-node block.

The reasons explain the shape. The edges `c->d` and `d->c` pull `d` into the triangle `a->b->c->a`, so 1 four-node component swallows it. The node `e` hangs off `a` by a single edge, which makes `a-e` a bridge and `e` a cut point. The pair `f`, `g` closes its own two-cycle, and `f->e` ties that pair back to the big component through the bridge. Six of the 7 nodes sit on cycles. The 1 that does not is `e`, the only node that is purely a bridge endpoint.

A node can sit on a cycle and be a cut point at the same time. `a` is inside the 4-node component and is still an articulation point, because the cuts are computed on the undirected projection, where deleting `a` separates `e` from the rest of the graph.

The traversal panel shows the depth cap doing its job. A BFS from `a` with a maximum depth of 2 reaches 3 nodes: `a` at depth 0, `b` at 1, `c` at 2. The other 4 are listed as unreachable.

## The traversal panel reads your arrows too

The BFS and DFS passes read the directional adjacency, so they follow your arrows even with the undirected box unticked.

Take the 5-node path `a b`, `b c`, `c d`, `d e` and write it down 4 ways, all undirected, all starting at `a` with a depth limit of 4. The undirected view is a-b-c-d-e in each case. The cut analysis is stable across all 4: 3 articulation points — `b`, `c`, `d` — and 4 bridges in each case. The condensation is stable too: 5 components and 4 edges in each case. Only the measured reach count moves.

<ul>
<li><strong>Written forward</strong> as `a b`, `b c`, `c d`, `d e`: measured reach 5 of 5, at depths 0 through 4. All nodes on the path are found. </li>
<li><strong>Written as</strong> `a b`, `b c`, `d c`, `e d`: measured reach 3 of 5. Nodes `d` and `e` are unreachable. </li>
<li><strong>Written as</strong> `a b`, `c b`, `c d`, `e d`: measured reach 2 of 5. Nodes `c`, `d` and `e` are unreachable. </li>
<li><strong>Written backward</strong> as `b a`, `c b`, `d c`, `e d`: measured reach 1 of 5. Only `a` is found. </li>
</ul>

The last case is the sharpest. The path is written with `a` at the end of the chain of arrows, so `a` has no outgoing edge. The traversal starts at `a`, has nowhere to go, and reports 1 node reached. The undirected projection, 2 panels away, still shows `a` attached to `b` with a bridge between them.

The mechanism is visible in the mixed variants. In `a b`, `c b`, `c d`, `e d`, the node `b` has no outgoing edge, so the traversal takes its 1 step from `a` to `b` and stops. In `a b`, `b c`, `d c`, `e d`, the chain `a->b->c` runs out at `c`, because `c`'s only edge points at it. A sink in the middle of the path cuts off all of the downstream nodes.

The tool's second shipped example is the forward path at a depth limit of 3, which reaches 4 of 5 nodes and lists `e` as unreachable. That is a depth cap, not a direction bug, and its summary line says so. The two are still worth telling apart. A depth cap leaves the far end unreachable and the near end populated, in order. A direction bug leaves a hole in the middle of the graph, with reachable nodes on both sides of it and a sink where the traversal died.

## Reading the output honestly

Eight rules cover this tool, and each one maps to a specific line of the implementation instead of to general advice about graph algorithms.

<ul>
<li><strong>Check the node count first.</strong> It is the only measured number that shows what the parser saw. </li>
<li><strong>One edge per line.</strong> The warning channel only catches lines that are too short. </li>
<li><strong>Read the badge as a fact about the algorithms.</strong> Both read the same adjacency, so they will agree. </li>
<li><strong>Read the component panel as directed, the cut panel as undirected.</strong> A node can be on a cycle and still be a cut point. </li>
<li><strong>Treat "none (graph cyclic)" as a formatting default.</strong> The order field is always null when the box is unticked. </li>
<li><strong>Check the cycle count for self-loops.</strong> A self-loop shows in the component table without a cyclic marker. </li>
<li><strong>Expect the reach count to follow your arrow direction.</strong> The cuts do not move when you reorder the lines. </li>
<li><strong>Know the 3 hard stops.</strong> More than 5000 nodes is rejected outright, and so is an input with no edges. </li>
</ul>

The [Graph Shortest Path Calculator](https://elysiatools.com/en/tools/graph-shortest-path) on Elysia Tools is the natural companion when you want distances instead of components, and the [Minimum Spanning Tree Calculator](https://elysiatools.com/en/tools/minimum-spanning-tree) is built on the same undirected weighted view this tool's cut panel uses. The [GraphML / GEXF / Edge List Network Converter](https://elysiatools.com/en/tools/graphml-gexf-edge-list-network-converter) is the practical way to get a graph into the edge-list form this tool expects, instead of typing arrows by hand and discovering later which ones got dropped. And when the topological order is the point instead of a side effect, the [Critical Path Method Calculator](https://elysiatools.com/en/tools/critical-path-method) does the sort on an activity network with cycle rejection built in. Browse the wider catalog at [Elysia Tools](https://elysiatools.com/en/categories/development) for the rest of the developer tools set.

## Where to take it from here

Both algorithms agree on the 7-node example, on the triangle, and on each malformed input I have fed this tool. I wish they disagreed sometimes. An implementation that can be wrong in the same direction by both algorithms is harder to catch than one that occasionally disagrees with itself, and the green badge invites exactly the trust the parser cannot support.

So check the node count against the graph you meant to draw, and write one edge per line. The algorithms will never do that for you, and they will never tell you that they did not. The point is not that the tool is unreliable. The point is that a green badge and a correct decomposition are different claims, and only one of them is something the badge can prove.

Ultimately, the question this badge raises is the question a cross-check always raises. If two implementations agree, was the input right, or did they read the same mistake the same way? The honest answer costs one number: count the nodes, and compare.
