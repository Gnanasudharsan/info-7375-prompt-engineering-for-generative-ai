# Pre-Mortem: CampusFit AI

**Premise:** It's 18 months from now and CampusFit AI has shut down. Here are the most likely reasons, ranked by how likely they are and how much damage they would do.

## First, a challenge to "demand is proven"

The 68% figure is the weakest part of the pitch, and it may be hiding the biggest risk.

- **Where does it come from?** Check the source, sample size, who funded it, and the exact question wording. If you can't trace it, don't use it.
- **"Would pay" is not paying.** Survey answers about hypothetical purchases usually overstate real buying, often by a lot. Saying "sure" costs nothing. Entering a card for $9.99 every month is a different decision.
- **"An AI meal planner" is not your product.** Interest in a general category doesn't show demand for campus-dining-specific plans plus workouts at $9.99/month.

Treat demand as **your biggest untested assumption**, not a proven fact.

## Top reasons it could fail

### 1. Free alternatives are good enough (high likelihood, high impact)
A student can paste the dining hall menu into ChatGPT, Claude, or Gemini and ask for a high-protein day. That takes 30 seconds and costs nothing. MyFitnessPal's free tier, YouTube programs, and campus rec center trainers also compete for the same need. Your product has to be clearly better than "free plus slight effort." Convenience alone may not get there.

### 2. The dining data problem is harder than the AI (high likelihood, high impact)
Your core value depends on accurate, current menus and nutrition data for each campus.
- There are thousands of campuses, run by different operators (large contractors and self-operated programs), with different menu systems.
- Menus change daily, items run out, and posted nutrition data is often incomplete or wrong.
- There may be no API. Scraping may violate terms of service or break constantly.

If you can't reliably get the data, the product falls back to a generic planner. That puts you right back in failure #1.

### 3. Price doesn't fit the student budget (high likelihood)
$9.99/month is about $120/year. Many students already pay for a mandatory meal plan and see that as their food cost. Students often share streaming accounts to save $5. You're asking them to pay *on top of* food they've already paid for.

### 4. Semester-shaped churn (high likelihood)
Fitness apps already churn heavily. Students add more:
- Summer, winter break, and study abroad, when campus dining doesn't apply
- Finals, when routines collapse
- Spikes in September and January that fade fast

You might effectively get about 7 paid months per year from your best users. That changes your LTV math.

### 5. Health, safety, and reputational risk (medium likelihood, very high impact)
College-age users are a higher-risk group for disordered eating. An app that pushes calorie targets and "optimized" eating to 18–22-year-olds could cause real harm and generate damaging press. Allergen errors from bad dining data are a second risk: one serious allergic reaction is an existential event. You need guardrails such as no extreme deficits, screening, and allergen disclaimers. You also need a stance on this before universities will work with you.

### 6. Distribution is expensive and campus-by-campus (medium-high likelihood)
Each campus is basically a separate market, with its own data integration and its own marketing. Student ambassador programs, Greek life, and club sports can work, but they scale linearly and slowly. Customer acquisition cost could easily exceed what a high-churn $9.99 subscriber is worth.

### 7. You might be selling to the wrong customer (medium likelihood)
Universities, dining services, rec centers, and athletic departments care about student wellness and engagement. They also have budgets and the data you need. A B2B or B2B2C model, where the school pays and students get it free, could fix failures #2, #3, and #6 at once. Going direct-to-consumer only may be the strategic mistake.

### 8. Two products, half-built each (medium likelihood)
Workout planning and meal planning are each crowded categories. Splitting effort across both may leave both mediocre. Your differentiator is campus dining, so that's probably where to focus.

## What to test first

Test the riskiest assumptions in the cheapest way, in this order:

**Test 1: Will students actually pay? (1–2 weeks)**
- Build a landing page for one campus (your own is the obvious choice) with the real $9.99 price.
- Use a "pre-order" or "join for $X" button that collects real payment or a refundable deposit, not just an email.
- Drive 300–500 students to it through club Slack/Discord groups, rec center flyers, and Reddit.
- **Signal:** conversion to payment, not signups. Set a kill threshold in advance, for example under 2–3% paying.

**Test 2: Concierge MVP (3–4 weeks)**
- Recruit 15–25 paying students. Build their plans *manually* (you plus an LLM) from the actual dining menus.
- **Measure:** Do they follow the plans? Do they renew after month 1? What do they say beats ChatGPT?
- This tests value and retention before you write production code.

**Test 3: The "vs. free ChatGPT" test**
- Have a few students use your plan for one week and their own ChatGPT prompting for another week.
- If they can't tell the difference or don't care, your differentiation isn't real yet.

**Test 4: Data feasibility (in parallel, 1 week)**
- Contact your campus dining services. Ask whether they'll share menu and nutrition data, and how accurate it is.
- Try to get clean data for 3 different campuses run by different operators. Note how long it takes.
- While you're there, ask whether *they* would pay for or sponsor something like this. That tests the B2B path (#7) for free.

**Test 5: Safety review (before any public launch)**
- Talk to your campus counseling or health center about eating disorder risk and what guardrails they'd expect.

## Suggested kill or pivot criteria

| Signal | Implication |
|---|---|
| Under 2–3% pay on the landing page | B2C demand is weak, so explore B2B or pivot |
| Under 50% of concierge users renew for month 2 | Value or retention problem |
| Users can't tell you apart from ChatGPT | Find a real differentiator before building |
| Dining data takes more than a week per campus | Scaling problem, so a dining partnership is required |
| Dining services or rec centers show strong interest | Seriously consider B2B2C |

**Bottom line:** The idea isn't dead, but "demand is proven" isn't true yet. Your biggest risks are real willingness to pay against free alternatives, and access to dining data. Both can be tested in under a month for almost no money, so test them before you build the app.