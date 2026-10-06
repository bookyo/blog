# Tip + Sales Tax + Currency Conversion + Discount Stacking Final Price Waterfall Field Guide: When Sequential Discounts, Tax Cascade, Tip Etiquette, and Mid-Market FX Decide What You Actually Pay at Checkout

<strong>A receipt is not a single number — it is a waterfall.</strong> The price on the shelf is the start, not the end. Every line that follows — the 10% off coupon, the 5% off for paying with the store card, the loyalty points redemption, the local sales tax, the restaurant tip, the dynamic-currency-conversion markup your card issuer charges at a foreign hotel — falls into a stack that determines what you actually hand over. The order matters, the base matters, and the rounding policy matters. Three things at once can turn a "$50" item into "$41.18" or "$54.62" depending on which jurisdiction you are in and which card you tap.

The free calculator at [Elysia Tools](https://elysiatools.com/en/tools/tip-sales-tax-currency-conversion-discount-stacking-calculator) walks through this entire waterfall line by line — stacked discounts (sequential vs additive, percent and fixed amounts), sales-tax cascade on the correct base (after store discounts per US rules, or pre-discount for manufacturer-coupon jurisdictions; additive US-style or compound GST+PST), tip on the pre-tax etiquette base with rounding policies, per-person split, and mid-market vs DCC currency conversion with the 3–7% dynamic-conversion markup and issuer FX fee compared. This guide is the field reference for the math behind each of those lines.

## What the Waterfall Actually Does — and Why "Total" Is the Last Row, Not the First

A naive checkout math runs `total = subtotal + tax + tip` and stops. A waterfall runs every adjustment on the running balance, in order, on the right base, with the right rounding policy at every step. The difference matters because two consecutive 20% discounts are not 40% off. The first 20% takes the price from $100 to $80. The second 20% takes $80 to $64 — a 36% effective discount, not 40%. And if sales tax is applied to the post-discount base in one state and to the pre-discount base in the next, the tax line differs even when every other input is identical.

The calculator emits each intermediate row so you can see exactly which base each downstream line used. The same `$100` list, two stacked 20% coupons, applied in two jurisdictions:

- New York (US-style additive, tax-on-post-discount): `$100 → 80 → 64 → 64 × 1.08875 = $69.68` (effective 30.32% off the list).
- Quebec (compound GST+PST, manufacturer-coupon rules apply pre-discount): `$100 → 80 → 64 → 64 × 1.14975 = $73.58` (effective 26.42% off the list).

Both are legal. Both are correct. The 3.9-percentage-point gap is not rounding error — it is the structural difference between tax-on-post-discount and tax-on-pre-discount, and the difference between additive and compounded provincial taxes. A single "tax rate" field in a calculator will silently collapse that.

## Stacked Discounts — Sequential vs Additive, and Why "20% + 15%" Is Not 35%

A "20% off + 15% off" coupon pair is the textbook case. Most shoppers do the mental math and arrive at 35% off. The actual math is multiplicative, not additive:

- Sequential (multiplicative): `final = list × (1 - 0.20) × (1 - 0.15) = list × 0.80 × 0.85 = list × 0.68` → 32% effective discount.
- Additive (add the percentages, apply once): `final = list × (1 - 0.35) = list × 0.65` → 35% effective discount.
- True stacked-with-cap (some retailers cap at 40% total): `final = list × max(1 - 0.40, 0.68) = list × 0.60` → 40% effective discount.

The Elysia Tools calculator exposes this with explicit per-row inputs — `discount 1 percent`, `discount 2 percent`, `stacking mode: sequential | additive | capped`. Try the same `$100` + `20% + 15%` under all three modes and the total reads `$68.00 / $65.00 / $60.00`. The order of application is also configurable: a store card discount applied before a manufacturer coupon changes the tax base in some US states and not in others.

For mixed percent-and-fixed discounts (a "$10 off" coupon plus a "15% off" coupon), the calculator has a separate mode: `apply fixed first, then percent, on the running balance`. Fixed-then-percent vs percent-then-fixed produces different totals when both coupons are active. Most US retailers run fixed-then-percent because it produces a smaller discount and is easier to reconcile with their inventory system; EU/UK retailers almost always run percent-then-fixed because consumer-protection law treats the largest discount as the headline figure.

## Sales Tax Cascade — The Hidden Geography Behind Every Receipt

Sales tax is not one line; it is a stack of lines that depend on jurisdiction, product category, discount source, and whether the transaction is in-store or online. Three cascades cover the cases the calculator handles:

<ul><li><strong>US-style additive.</strong> State tax + county tax + city tax + special district tax, all applied to the same base (post-store-discount, pre-manufacturer-coupon). A typical NYC receipt is 4% state + 4.5% city + 0.375% MCTD = 8.875% total. The calculator lets you enter each component separately and sums them at audit time.</li><li><strong>Canadian compound.</strong> GST (federal) computed on the post-discount base, then PST/HST/QST (provincial) computed on <code>subtotal + GST</code>. Quebec's 5% GST + 9.975% QST compounds; Ontario's 5% GST + 8% PST (or 13% HST instead) is additive-then-HST. The compound variant produces a slightly higher effective rate because the provincial tax is applied to a base that already contains the federal tax.</li><li><strong>EU/UK VAT-inclusive.</strong> The shelf price already includes VAT; the receipt's "VAT" line is a back-out, not an add-on. The calculator handles this by accepting a <code>price includes VAT</code> flag and showing both the net and gross lines.</li></ul>

Product-category exemptions are the next layer: groceries are typically exempt from state sales tax in most US states but subject to prepared-food tax once they cross the deli threshold. Clothing is exempt in MA, NJ, NY (under $110), and PA, but taxable in TX, FL, and CA. The calculator's `category override` flag accepts a tax multiplier from 0.0 (fully exempt) to 1.0 (fully taxable). For a `$50` grocery + `$30` clothing purchase in NYC, the line math becomes `tax = 30 × 0.08875 = $2.66` (clothing taxable, groceries exempt), not `80 × 0.08875 = $7.10`.

## Discount Source Matters — Store Coupons vs Manufacturer Coupons vs Loyalty Points

The line "10% off coupon" is ambiguous in three different ways, and the legal/policy distinction changes which base tax applies to:

<ul><li><strong>Store coupons</strong> — issued by the retailer itself. Sales tax applies to the post-coupon price in nearly every US state (the retailer is "giving up" revenue, so the state does not collect tax on the giveaway).</li><li><strong>Manufacturer coupons</strong> — issued by the product maker, redeemed at the retailer. Some states (NY, CT, FL) treat these as a price reduction AT the shelf (tax applies to post-coupon), others (MA, MO, VA) treat them as a rebate AFTER the sale (tax applies to pre-coupon). The same coupon produces two different tax lines depending on which state you're in.</li><li><strong>Loyalty points / store credit</strong> — always a post-tax reduction. The retailer collects full sales tax on the original price, then deducts the points at the till. This is the easiest case to model but the easiest case to forget when "discount" is the only input field on the calculator.</li></ul>

The Elysia Tools waterfall accepts a `discount source: store | manufacturer | loyalty` flag per coupon line so the tax base is correct at audit. A `$100` item + `$10 store coupon` + `$5 manufacturer coupon` + `8.875% NYC tax` produces `$100 - $10 - $5 = $85 × 1.08875 = $92.54`. A `$100` item + `$10 store coupon` + `$5 manufacturer coupon treated as rebate` + `8.875% NYC tax` produces `$90 × 1.08875 = $98.99`, then a `- $5 loyalty rebate` line for `$93.99`. The $1.45 gap is the manufacturer-coupon rebate treatment.

## Tip Etiquette — Pre-Tax or Post-Tax, and the Rounding Policy That Matters

Two questions determine the tip line: what is the base, and how does it round? The base question has a clear etiquette answer in the US (tip on the pre-tax subtotal, not on the post-tax total), but the rounding question varies by POS system and is where most tip-math complaints originate:

- Pre-tax base, rounded to nearest dollar: `$80 pre-tax × 0.18 = $14.40 → $14.00`. The patron rounds down to a clean number; the server sees a slightly lower tip.
- Pre-tax base, rounded up to nearest dollar: `$80 pre-tax × 0.18 = $14.40 → $15.00`. The patron rounds up to a clean number; the server sees a slightly higher tip.
- Post-tax base (technically wrong, but some POS systems default to it): `$88.75 post-tax × 0.18 = $15.975 → $16.00`. The "right" 18% on the post-tax base is higher than the right 18% on the pre-tax base.

The calculator exposes all three with an explicit `tip base: pre-tax | post-tax | post-discount` flag and a `rounding: down | up | nearest | none` flag. For a `$100` list + `10% coupon` + `8.875% tax` + `18% tip` in NYC:

- Pre-tax + round-down: `$90 × 0.08875 + $90 × 0.18 = $7.99 + $16.20 = $24.19` total tip+tax line.
- Post-tax + round-up: `$97.99 × 0.18 = $17.64 → $18.00`, total tip+tax line is `$25.99`.
- Pre-tax + no rounding: `$90 × 0.18 = $16.20`, total tip+tax line is `$24.19`.

The 80-cent gap is the rounding policy. For groups splitting the bill, the `split: N ways` flag divides each line — but the rounding policy is applied to the per-person total, not the pre-split total, so 4-way splits can shift the total by up to 4 × $0.50 = $2.00.

## Currency Conversion — Mid-Market vs DCC, and the 3–7% Markup You Did Not Budget For

Foreign-card transactions expose a markup the cardholder usually does not see until the statement closes. The hotel terminal, the airport kiosk, or the online checkout offers **Dynamic Currency Conversion (DCC)** — pay in your home currency at "today's rate" — and the alternative is to pay in the local currency and let your card issuer do the conversion. The DCC rate is always 3–7% worse than the mid-market rate your card issuer would use, plus a separate issuer FX fee of 0–3% on top. The combined markup can be 10% of the transaction for no service rendered.

The calculator accepts three rates — `mid-market`, `DCC offered`, and `issuer FX fee` — and shows the per-rate subtotal for the same local-currency amount. For a €100 hotel charge on a USD card with a 1.08 mid-market rate, a 1.13 DCC offered rate, and a 1% issuer FX fee:

- Mid-market + 1% issuer fee: `€100 × 1.08 × 1.01 = $109.08`.
- DCC offered: `€100 × 1.13 = $113.00`.
- DCC + 1% issuer fee (some cards stack): `€100 × 1.13 × 1.01 = $114.13`.

The $5.05 gap between mid-market and DCC-with-issuer-fee is the actual cost of accepting DCC at the terminal. The calculator's `always decline DCC` flag inverts the DCC line to show the savings had you declined: `$114.13 - $109.08 = $5.05 saved`. On a 2-week trip with $1,500 of card charges, that scales to $75 of avoidable markup — about a dinner for two.

## Putting It Together — A Worked Example That Hits Every Line

A traveler in Montreal pays a $200 CAD hotel bill in USD with a US-issued card, uses a "10% AAA member discount" plus a "$20 loyalty points redemption," tips 18% on the pre-tax base, and is offered DCC at the terminal. The waterfall, in order, with the correct base at every step:

1. List price: `$200 CAD`.
2. AAA member discount (10%, sequential): `$200 × 0.90 = $180 CAD`.
3. Loyalty redemption ($20 fixed, applied after percent): `$180 - $20 = $160 CAD`.
4. GST (5%, federal, on post-discount base): `$160 × 0.05 = $8 CAD`.
5. QST (9.975%, provincial, on `subtotal + GST`): `($160 + $8) × 0.09975 = $16.76 CAD`.
6. Pre-tax base for tip: `$160 CAD` (the pre-tax base, NOT the post-tax base of `$184.76`).
7. Tip 18% on `$160`: `$28.80 CAD`, rounded up to `$29.00 CAD`.
8. Total in CAD: `$160 + $8 + $16.76 + $29 = $213.76 CAD`.
9. Conversion to USD at mid-market (assume 0.74 USD/CAD): `$213.76 × 0.74 = $158.18 USD`.
10. Issuer FX fee (1%): `$158.18 × 1.01 = $159.76 USD`.
11. If DCC had been accepted (offered rate 0.71 USD/CAD, no issuer fee stacked): `$213.76 × 0.71 = $151.77 USD` — paradoxically cheaper in this case because the DCC rate spread happened to be in the cardholder's favor, which is rare but documented.

The calculator reproduces this entire waterfall in a single pass and lets you toggle each line on/off to see the marginal effect. The "everything off" baseline is `$200 CAD → $148 USD at mid-market`; the "everything on" total is `$159.76 USD` — a 7.95% markup over the simplest path, almost all of it attributable to the compounded QST-on-GST cascade and the tip-on-pre-tax rounding policy.

## Quick Reference — The Four Rules That Decide Every Receipt

Four rules, applied in order, decide every receipt's final line regardless of jurisdiction or transaction type:

<ol><li><strong>Discounts apply multiplicatively, not additively.</strong> Two consecutive 20% discounts are 36% off, not 40%.</li><li><strong>Tax base depends on jurisdiction AND coupon source.</strong> US state sales tax applies to post-store-discount; manufacturer coupons vary by state; Canadian QST compounds on <code>subtotal + GST</code>.</li><li><strong>Tip etiquette base is pre-tax, but the POS system may default to post-tax.</strong> Check the receipt's base — if the 18% tip looks higher than expected, the POS is tipping on post-tax.</li><li><strong>DCC is a 3–7% markup on top of your issuer FX fee.</strong> Always pay in the local currency unless the DCC rate happens to be better than the mid-market rate for that day (rare; requires pre-trip rate check).</li></ol>

The Elysia Tools calculator at [elysiatools.com/en/tools/tip-sales-tax-currency-conversion-discount-stacking-calculator](https://elysiatools.com/en/tools/tip-sales-tax-currency-conversion-discount-stacking-calculator) bakes all four rules into the waterfall so the receipt math is auditable line by line. Try the worked example above as a sanity check; if your total matches to the cent, the four-rule model is the right one for your transaction class.
