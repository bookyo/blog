**A 4-bit counter stepping from 7 to 8 flips every one of its bits at once, and the code built to fix that flips exactly one.** The [Gray Code and Thermometer BCD Encoder Visualizer](https://elysiatools.com/en/tools/gray-code-and-thermometer-bcd-encoder-visualizer) puts four encodings of the same number side by side — plain binary, Gray, one-hot and thermometer — and then charts how many bits each encoding changes at every step of a counting sequence. Binary spikes to four flipped bits at that boundary. Gray never leaves one.

The four encodings are not interchangeable, and the difference is not academic. A Gray-coded counter can be sampled by a two-flop synchronizer at any instant during a transition and still read either the old value or the new one, never a mixture of the two. A binary counter sampled mid-transition can read a word that was never on the bus at all. That single property is why Gray code survives in rotary encoders, in Karnaugh-map axis orderings, and in asynchronous FIFO pointers, and why the other three codes do not.

## One Number, Four Codes

The tool encodes one value at a time into all four representations, for a word width of two to six bits. Four bits gives sixteen codes and a fifteen-bit thermometer word; six bits gives sixty-four codes and a sixty-three-bit thermometer word. It also reports the transition you are standing on: how many bits the previous value and this value differ by, in each encoding.

The four conversions are short enough to hold in your head:

<ul>
<li><strong>Binary</strong> — the plain positional code, the value padded out to the full word width.</li>
<li><strong>Gray</strong> — the binary value XORed with itself shifted right by one bit. The most significant bit passes through unchanged; every other bit is the XOR of itself and the bit above it.</li>
<li><strong>One-hot</strong> — a word of 2^N bits with a single 1 standing at the bit position equal to the value itself. For value 11 in a four-bit word that is bit 11 of the sixteen-bit field, which lands as the fifth character from the left when the word is written most significant bit first.</li>
<li><strong>Thermometer</strong> — a word of 2^N minus 1 bits, unary and aligned to the most significant end: as many 1s as the value, then zeros.</li></ul>

Read those four lines together and the trade is visible. Binary is the only one of the four that fits in N bits. One-hot needs 2^N bits and thermometer needs 2^N minus 1. Gray stays at N bits, exactly like binary, and only changes which N bits it uses.

## The Codes Side by Side

Take the tool's default case: the value 11 in a four-bit word. Binary is 1011. Gray is 1110, which is 1011 XORed with 0101. One-hot is sixteen bits with a single 1 in the position that binary calls 8 plus 2 plus 1, giving 0000100000000000. Thermometer is fifteen bits with eleven 1s at the top, giving 111111111110000.

Set the value to 8 instead and the same four encodings come back in a different shape. Binary is 1000, Gray is 1100, one-hot is 0000000100000000, and thermometer is 111111110000000 with eight 1s. Notice what the thermometer did: it did not rewrite its bits, it appended one more 1 and dropped a zero off the bottom. That is the defining property of the code, and it is why a thermometer word can be decoded with a comparator bank instead of a XOR tree.

The width arithmetic matters when you are counting wires. At six bits, one-hot is a sixty-four-bit bus and thermometer is a sixty-three-bit bus, both carrying a number that fits in six bits of plain binary. Every extra bit of word width doubles the one-hot bus and the thermometer bus, while Gray stays exactly as wide as the binary it replaces.

## The 7 to 8 Boundary

The worst step in any binary counter is the carry. Going from 7 to 8 in four bits turns 0111 into 1000, and all four bits change at the same instant. Sample that bus one gate delay after the clock edge and you can read 0000, or 0111, or anything in between, depending on where the individual bit paths happen to be.

Gray code has no such step. The same 7 to 8 transition moves Gray from 0100 to 1100, and exactly one bit changes. That is not a coincidence of this particular pair of values: the reflected binary code is constructed so that every consecutive pair in the whole sequence differs in one bit, and the same holds for the wrap from the largest value back to zero.

The other two codes behave differently again. The one-hot word clears one 1 and sets another, so two bits always change on every single step, and it never changes shape. The thermometer word appends a 1, so one bit changes on every step within the range — with one exception that the tool's own chart exposes and its summary card does not.

This is the part that catches people out. If you are crossing a clock domain with a counter, Gray is the code you want, because the two-flop synchronizer at the receiving end can only ever capture a valid old-or-new value. If you are feeding a decoder or a state machine, one-hot is the code you want, because the next-state logic collapses into a simple OR of single bits. They are not competing answers to the same question.

## What the Hamming Chart Does and Does Not Show

The chart is the centrepiece of the output. Each group is one step of the counting sequence, and each bar is the number of bits that changed between the previous value and this one, with four bars per group for the four codes.

Read the binary bar and the story is familiar. The worst step is always the full word width: four bits for a four-bit word, six bits for a six-bit word. The mean across the whole sequence is 1.875 bits for a four-bit word and 1.969 for a six-bit word, because the carry steps are rare enough to pull the average down towards two without ever removing the spike. The Gray bar is a flat line at one for every group, including the wrap, which is the entire argument for the code in one picture. The one-hot bar is a flat line at two.

The thermometer bar is where the chart stops being a faithful summary. Within the range, thermometer changes one bit per step, exactly like Gray. At the wrap from the largest value back to zero, the thermometer word goes from all ones to all zeros, and every single one of its 2^N minus 1 bits flips at once. For a four-bit word that is fifteen changed bits against a chart whose vertical axis is scaled to the binary maximum of four, so that one bar is three and three-quarter times the full height of the plot area and gets clipped flat against the top of the chart. At six bits it is sixty-three changed bits against an axis scaled to six, which is over ten times the plot height.

The tool's own metadata field for this is hardcoded to 1, and the summary card below the chart reads "always 1" with the note "monotonic fill". The chart draws the truth, the summary card draws the rule, and the rule is only true inside the range. If you are designing a thermometer-decoded front end, the wrap is the case to think about, not the case to skip.

## Where Each Code Earns Its Keep

<ul>
<li><strong>Gray</strong> — rotary and optical encoders, where a reading head between two tracks can only ever see one ambiguous bit; Karnaugh-map axes, where adjacent rows must differ in exactly one variable; and asynchronous FIFO read and write pointers crossing clock domains.</li>
<li><strong>Thermometer</strong> — the native output of a flash converter's 2^N minus 1 comparator bank. The fill is monotonic, so a bubble error, a single stuck 1 among zeros, is easy to detect and correct before the thermometer-to-binary encoder ever sees the word.</li>
<li><strong>One-hot</strong> — finite state machine state encoding and decoder selects. It costs 2^N wires, but the decode logic is nearly free and there is zero reconvergence between states, because a one-hot state never has two bits changing at once.</li>
<li><strong>Plain binary</strong> — the most compact of the four, and entirely the right choice inside a synchronous block where every bit settles before anything samples it.</li></ul>

The pattern across all four is that the wider code buys a guarantee. Binary is narrow and says nothing about how it behaves mid-transition. Gray is the same width and guarantees one changed bit. Thermometer and one-hot are much wider and guarantee a simple, decodable structure: one fills up, the other moves.

## Reading the Result Object

The tool returns JSON, and the fields are worth knowing because they let you check the arithmetic rather than trust a picture. `decimalValue` and `binaryCode` carry the input and its plain form. `grayCode`, `oneHotCode` and `thermometerCode` carry the three derived forms. `oneHotBits` and `thermometerBits` state the width of the two wide codes, so you never have to derive them yourself.

The transition fields are the interesting ones. `hdBinaryCurrent` and `hdGrayCurrent` give the changed-bit count for the step you are standing on, and they are what turn the tool from a converter into a comparison instrument. Setting the value to 8 in a four-bit word returns `hdBinaryCurrent` of 4 and `hdGrayCurrent` of 1, which is the boundary case in one glance.

The summary fields need more care. `maxBinaryHd` and `maxGrayHd` are computed across the whole counting sequence including the wrap, so they are the worst case over every transition, not the current one. `meanBinaryHd` is the average over that same sequence. Then there are `oneHotHdAlways`, hardcoded to 2, and `thermometerHdAlways`, hardcoded to 1. Both are constants that describe the ordinary case. Neither one is a measurement, and the thermometer one is wrong at the wrap, which is exactly where the chart disagrees with it.

The `language` field records which HDL stub you asked for, and the stubs themselves are worth reading. The Verilog encoder is three continuous assignments: the Gray line XORs the input with itself shifted right, the one-hot line shifts a single set bit by the input value, and the thermometer line shifts a full run of ones by the remaining width minus the input value. The reverse Gray-to-binary module cascades an XOR down from the most significant bit.

## What the Tool Cannot Tell You

The name promises BCD, and the tool does not produce it. Binary-coded decimal packs each decimal digit into its own four-bit group, and there is no option for it here; the four outputs are binary, Gray, one-hot and thermometer. The word "BCD" in the name is a leftover from the family the tool belongs to, and if you need real BCD you will not find it in this output.

The width ceiling is six bits, which covers every practical state machine and every practical counter, but it means the tool cannot show you what a sixteen-bit Gray counter looks like across its full sequence. The chart is also drawn for the full range, so at six bits the group labels are sparse and the binary carry spikes are one group in sixty-four.

The stubs are templates, not verified designs. The parameters are substituted for you and the width arithmetic is correct, but nothing here checks the result against a simulator, and nothing models the metastability that the Gray code is there to protect you from. The one-hot assignment in particular is written for a synthesizable width, not for the 32-bit literal that a careless reading would suggest.

The most useful thing to take away is the comparison itself. Four codes, one number, and a chart that shows exactly what each one costs when the value moves.

## Where This Fits Next

This tool rewards a habit most encoding references skip: check the transition, not just the value. Any counter, any state register, any bus crossing can be checked against the same question — how many bits change at once — and the answer tells you whether your synchronizer is safe, whether your decode logic is cheap, and whether your glitch margin is real.

If you want the broader picture, the [Truth Table Generator](https://elysiatools.com/en/tools/truth-table-generator) shows you the same combinational logic before it is encoded, the [Finite State Machine, Mealy-Moore and Karnaugh Minimization Tutor](https://elysiatools.com/en/tools/finite-state-machine-mealy-moore-karnaugh-minimization-tutor) is where one-hot state encoding and Gray-ordered map axes meet, and the [Base-N Radix Converter](https://elysiatools.com/en/tools/base-n-radix-converter) covers the plain positional part of the story. The [Boolean Algebra Simplifier](https://elysiatools.com/en/tools/boolean-algebra-simplifier) takes the same logic the other direction and proves which terms survive. Browse the [Development category](https://elysiatools.com/en/categories/development) or explore more tools at [elysiatools.com](https://elysiatools.com/en/tools). One number, four codes, and one chart that tells you which of them you can actually sample safely.
