# Pre-Mortem: CampusFit AI

**The premise:** It's October 2027. CampusFit AI has shut down. Here is the most likely story of why, starting with the assumption I'd challenge hardest.

## First, "demand is proven" is the riskiest belief in your plan

The 68% figure doesn't prove demand, even if it's accurate. I can't verify the source, so check who ran the survey, the sample size, and the exact question. Even if the number holds, there are three problems:

1. **Stated vs. revealed willingness to pay.** Survey "would pay" answers routinely overstate actual purchases by a wide margin, especially when no price is attached. "Would pay for something" is not "would pay $9.99/month, recurring."
2. **It measured a different product.** "An AI meal planner" is not "a $9.99 subscription bundling workouts with campus-dining meals." You have evidence of interest in a category, not your product.
3. **Who ran it matters.** If the survey came from a company selling meal planners, treat it as marketing.

Treat demand as your #1 unproven hypothesis, not a settled fact.

## Top reasons it failed, ranked by likelihood × severity

### 1. Students wouldn't pay $9.99/month when free substitutes were "good enough"
- ChatGPT, Gemini, and similar tools will produce a workout plan and meal ideas for free in about 30 seconds.
- Campus dining apps such as Nutrislice and Dine On Campus already show menus and nutrition data.
- Most campuses have free rec centers, group classes, and sometimes free nutritionist consults.
- $120/year is meaningful money for many students. Your real competitor is "free + slightly inconvenient."

### 2. The campus-dining data was too hard to get and keep accurate
This is your core differentiator, and it's operationally brutal:
- Every campus has different menus, often changing daily, and many are run by contractors like Aramark, Sodexo, or Chartwells.
- Nutrition data is inconsistent, and items run out or get substituted.
- Scraping may break or violate terms, and licensing may require B2B deals.
- If the app recommends a dish that isn't being served, trust collapses immediately.

This also means you can't scale like a normal app. You expand campus by campus, each with its own setup cost.

### 3. Retention cratered because of the academic calendar
- Summer, winter break, spring break, and finals weeks mean 3 to 5 months a year when the core use case disappears.
- Many students drop the dining plan after their first or second year, which removes the dining half of your value.
- Fitness apps already have notoriously poor 30- and 90-day retention. You stack seasonality on top of that.
- Your customers graduate, so lifetime value is capped by design.

### 4. Customer acquisition cost exceeded lifetime value
- Students are cheap to reach in theory but expensive to convert to paid.
- Rough math: if average subscriber lifetime is about 3 months, LTV is about $30 before app store fees of 15–30%. You'd need CAC well under roughly $20.

### 5. Health and liability risk scared off universities and users
- College populations have a meaningful prevalence of disordered eating. An AI that pushes calorie targets and workout volume to 18-year-olds can cause real harm.
- One viral story ("AI app told me to eat 1,100 calories") could end the company.
- This also blocks your best distribution channel. University partners and dining services will be cautious about endorsing it.

### 6. Two half-products instead of one great one
Workout planning and meal planning are each crowded categories. Bundling them can mean being mediocre at both and confusing the message.

### 7. Wrong payer
Students may love it, but the real buyers might be parents, athletic departments, university wellness programs, or the dining contractors themselves. Going direct-to-student may simply be the weakest business model.

## What to test first

Test the assumptions that would kill the idea, cheapest first. Set kill criteria before each test.

| Order | Assumption | Cheap test | Example kill criterion |
|---|---|---|---|
| **1** | Students will actually pay | **Fake-door / pre-sale at one campus.** Landing page with real pricing; collect a $5–10 refundable deposit or first month's payment. Drive traffic via dorm groups, Discord, flyers. | Under 3–5% of visitors pay, or under 30 paid sign-ups from about 1,000 targeted visitors |
| **2** | Campus dining integration is the differentiator | **Concierge MVP.** For 15–25 students at one school, manually build plans from the actual daily dining hall menu, delivered by text or email, for 3–4 weeks. No AI or app needed. | Fewer than half still engaged in week 3, or users say "ChatGPT does this" |
| **3** | You beat free AI | **Head-to-head.** Give half your testers ChatGPT plus a good prompt and half your concierge plans; compare satisfaction and stated WTP. | No clear preference for your version |
| **4** | Menu data is obtainable | **Feasibility audit of 5 campuses.** Can you get daily menus and nutrition reliably and legally? How many dining contractors cover your target schools? | Fewer than 3 of 5 viable without a contractor deal |
| **5** | Pricing and payer | Test $4.99/mo, $9.99/mo, $29/semester, and a parent-pays option. Separately, have 5 conversations with campus wellness or dining staff about B2B interest. | Semester pricing or B2B shows much stronger pull, so pivot the model |

Run a safety review in parallel, not afterward: guardrails on calorie floors, no weight-loss targeting for minors, eating disorder screening and resources, and a clear "not medical advice" stance. It's cheap now and existential later.

## My take

The two assumptions that could each kill this on their own are **#1 (willingness to pay vs. free AI)** and **#2 (reliable dining data)**. Both can be tested at one campus within about 4 weeks for under a few hundred dollars and without writing much code.

Would you like help drafting the landing page copy, the concierge-test protocol, or the interview script for students? And if you can share the source of the 68% stat, I'll help you assess how much weight it can actually bear.