# Pre-Mortem: CampusFit AI

**Premise:** It's October 2027 and CampusFit AI has shut down. Here are the most likely reasons, ranked by risk.

## First, the 68% statistic does not prove demand

Your core assumption is the weakest part of the pitch:

- **Where is it from?** Who ran the survey, how many students, which schools, and what exactly was asked? Without that, investors and judges will discount it heavily.
- **Saying isn't paying.** Survey willingness-to-pay is consistently inflated. "Would you pay for X?" costs nothing to answer yes to. Converting from free to paid in consumer apps typically happens at low single-digit rates.
- **The question doesn't match your product.** "Pay for an AI meal planner" (at any price, from anyone) is not the same as "pay $9.99/month for workouts plus campus-dining meals." Price, the bundle, and the brand are all untested.

Treat the 68% as a hypothesis, not validation.

## Top reasons it could fail

**1. Free substitutes are good enough.**
Students can ask ChatGPT or Claude: *"Here's my dining hall menu, I want 140g of protein, plan my day."* Add free workout apps and YouTube, and the question becomes why anyone pays $120 a year. Your real competitor is a free chatbot plus five minutes of effort.

**2. The campus-dining data problem.**
This is your differentiator and your hardest operational problem.
- Menus change daily, and many items run out or get swapped.
- Data lives in vendor systems (Aramark, Sodexo, Chartwells, Nutrislice, in-house portals) with no consistent public API.
- Nutrition info is often incomplete, and portions vary by who's serving.
- Each campus may need its own integration, so you scale school by school, not nationally.

If your plans recommend food that isn't available, trust collapses after one bad meal.

**3. Students' wallets don't match the pitch.**
- Students on dining plans have already prepaid for food, which leaves less perceived value and less money to spend.
- $9.99/month competes with Spotify Student, Netflix, and similar subscriptions.
- Students who cook off-campus aren't served by the dining focus, which shrinks your market as students age out of dorms.

**4. Seasonality and churn.**
The academic year is about 8–9 months, with breaks, finals, and summers off. Fitness apps already suffer severe motivation drop-off after January or the first weeks of a semester. Your lifetime value may be 2–3 months per user.

**5. Health and safety liability.**
College-age students have elevated rates of disordered eating. An AI pushing calorie targets and workout volume to this group carries real risks:
- Harm to users, plus reputational and possibly legal exposure.
- Universities, counseling centers, and dining services refusing to partner with you.

You need guardrails such as calorie floors, screening, and referral pathways from day one. This is not optional polish.

**6. Distribution is expensive.**
Students are reachable but noisy to market to. Paid acquisition cost can easily exceed a 3-month lifetime value of about $30. Without an organic loop (roommates, teams, clubs, RAs), the unit economics may never work.

**7. Your best customer may not be the student.**
Universities, rec centers, athletic departments, and dining vendors care about wellness, engagement, and dining satisfaction, and they have budgets. You may fail by selling to the wrong buyer. These B2B sales are slow but stickier.

## What to test first

Test in order of riskiest and cheapest:

| # | Assumption | Test | Pass signal (set before testing) |
|---|---|---|---|
| 1 | Students will actually pay $9.99 | Landing page with real pricing and a pre-order or paid waitlist, promoted on one campus | A meaningful share of visitors enter payment info, not just email |
| 2 | Campus dining plans beat free ChatGPT | **Concierge MVP:** manually build plans from Northeastern dining menus for 15–20 students for 2 weeks, and charge them | Students follow the plans and renew; they say it beats asking a chatbot |
| 3 | Dining data is obtainable at scale | Try to pull menu and nutrition data for 5 campuses on different vendors | Automatable for most of them without heroic effort |
| 4 | Retention survives the semester | Track concierge users weekly | Engagement at week 4 and week 8 |
| 5 | Institutions would pay | 5–10 conversations with rec center, dining, and wellness staff | Any willingness to pilot or co-fund |

**Run tests #1 and #2 first, together.** They directly challenge the 68% assumption and the "why not just use ChatGPT" objection, which are the two things most likely to kill this. You can run both at Northeastern within a few weeks for almost no cost.

## Reframe to consider

Pitch it as *"a dining-hall-aware nutrition coach, with safety guardrails, that universities can offer students,"* and consider freemium for students plus institutional licenses. That positioning defends against free AI substitutes and addresses the liability and churn problems at the same time.

If it would help, I can find published research on college students' willingness to pay, fitness-app retention, or disordered eating risk in calorie-tracking apps to strengthen the evidence in your pitch.