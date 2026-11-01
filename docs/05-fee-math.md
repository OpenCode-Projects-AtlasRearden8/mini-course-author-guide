# Platform-Versus-Marketplace Fee Math

Where your mini-course lives decides how much of each sale you keep. Do the
math on paper *before* setting anything up — it is five minutes of
arithmetic that prevents a year of quiet margin leak. This chapter gives
you the worked example, the break-even rule, and the decision rule.

> All percentages and prices below are **illustrative examples** used to
> teach the arithmetic, with rates you would have found in the U.S. market
> in early 2026-class product. Fees change all the time; before you decide,
> look up the current rate of the two or three services you are actually
> considering and rerun these exact calculations with their numbers.

## The three venues, in one breath

- **Self-hosted:** your static site for the lesson pages + a
  payment processor (e.g., Stripe or PayPal) taking you a flat percentage
  plus a few cents per sale, plus (in real life) the hosting cost of files.
- **Marketplace/storefront-builder** (frequently Gumroad-style): they
  handle the page, the card, the delivery, and the buyer trust they bring.
  They charge a bigger percentage per sale, and usually $0/month.
- **Full course platform** (frequently Teachable/Thinkific-style): they
  host lesson structure, videos, and progress. They charge a monthly fee
  plus a transaction percentage, dropping to a smaller percentage at
  higher tiers.

## The worked example (rerun it with real rates)

Say the mini-course sells for **$49**, and you expect **8 sales/month** to
start. Here is the arithmetic pattern — the three numbers you need from
any real service are (a) percentage of sale, (b) fixed cents-per-charge,
(c) monthly fee.

### Math for self-hosted (Stripe-like: 2.9% + $0.30)

- Percent: $49 × 0.029 = $1.421
- Fixed: $0.30
- Net per sale: $49 − $1.42 − $0.30 = **$47.28**
- 8 sales: **$378.24/month**, before hosting costs (static hosting for
  pages + a few GB of video ≈ $0–$10/month at this size).

### Math for marketplace (10% flat, no monthly fee)

- Per-sale fee: $49 × 0.10 = $4.90
- Net per sale: **$44.10**
- 8 sales: **$352.80/month**.

### Math for course platform ($39/month + 5%, illustrative)

- Per sale: $49 − ($49 × 0.05) = $46.55
- Gross-of-fee income 8 sales: $372.40
- Minus monthly: $372.40 − $39 = **$333.40/month.**

### The same table at a glance

| Venue | Fee model | Net per $49 sale | Net on 8 sales/mo | Monthly fixed |
| --- | --- | --- | --- | --- |
| Self-hosted | ~2.9% + $0.30 | ~$47.28 | ~$378.24 | $0–$10 (hosting) |
| Marketplace | ~10% flat | ~$44.10 | ~$352.80 | $0 |
| Course platform | ~$39/mo + 5% | ~$46.55 | ~$333.40 | $39 |

At eight sales a month the marketplace-seller pay pattern costs you about
**$25/month** versus self-hosted — the price of not maintaining a page
yourself. The course platform trails because its monthly fee eats a small
catalog's margin.

## The break-even rule for monthly fees

For any venue with a monthly fee, compute the number of sales where it wins:

> Break-even sales = monthly fee ÷ (net per sale without the monthly fee −
> net per sale with it)

With the numbers above: $39 ÷ ($47.28 − $46.55) ≈ **53 sales/month.**
Under that, self-hosted (or a $0/month marketplace) wins. Above roughly
53 and a full platform starts to pay for its monthly fee — *in this
example*. Rerun with real rates; small changes in the percentages move the
break-even a lot.

## The four real-world costs new sellers forget

1. **Refund reserve.** Whatever your refund window (see the next
   chapter), assume small: at 5% refund rate, and you eat the processor
   fee on the refund — net slightly drops on all sales.
2. **Payment rails' small taxes:** cross-border sales, currency
   conversion, VAT handling for EU buyers. Serviceable everywhere, but
   your $47.28 becomes $45–46 on an EU sale, usually. Check.
3. **Your time-to-ship.** Self-hosted costs an afternoon up front. If the
   afternoon does not exist this month, a $0/month marketplace is the
   honest answer — the fee is buying you shipping *now*.
4. **Payout delay.** Marketplaces and platforms may hold funds for days or
   weeks; direct processors usually pay out in a couple of days. For a
   first launch this rarely matters; if cash flow matters, check payout
   terms.

## The decision rule (say it out loud)

- **Choose self-hosted** if you want the highest margin, will ship pages
  yourself this week, and your monthly sales are likely under the
  break-even you just computed. This is the default for a v1 mini-course.
- **Choose a marketplace** if you need to ship *today* with $0 infrastructure
  and goodwill of a trusted checkout, and can tolerate ~10% to buy speed.
- **Choose a full platform** if you will build a multi-module course with
  progress tracking and enrollment management — a different project, and
  not this one.

And one more: you can *start on one and move later*. Buyers of a $49
mini-course mostly care that the lesson works; a plain "the course moved
here" email at v1.1 keeps them better than any lock-in would.

## Exercise (15 minutes)

1. Pick your price (a promise-sized lesson usually lands at $19–$79).
2. Look up real current rates for: your payment processor of choice, one
   marketplace, one course platform. Write the three numbers for each.
3. Rerun the worked example at your price and a conservative sales count
   (say, 5/month). Round numbers are fine; wrong direction is not.
4. Compute your personal break-even for the platform with a monthly fee.
5. Circle your venue in pen. Done means done; revisit at 100 sales total.
