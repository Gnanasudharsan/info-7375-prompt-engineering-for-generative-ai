# Domain justification: part-time funded research, found from the money

## Executive summary

**What this is.** A one-page case for a new way of using the Reallocation Engine: not to rank job postings, but to find where research money sits before writing to a lab. **Why read it.** The mode was built for one situation, a full-time teaching professor who wants a part-time, paid research role in computational biology or data-heavy research, and the case below says why the engine's usual job-board checks cannot help that person and what can. **What it found.** The thing this person cannot see, whether a lab can pay anyone, is public in two federal award databases; a first real run found 349 matching awards at six Boston-area institutions, of which 223 could pay for work starting in January 2027. The same run also showed two ways the numbers mislead a reader who does not know the field, which the last section names.

## Who uses this mode, and when

One person: US citizen, no sponsorship needed, based in Boston, with a full-time teaching job and about 20 hours a week free in term and full-time in summer. They would work mostly remotely and be on site about once a week, within a few miles of Northeastern. Their problem is not finding job postings. Labs and research groups seldom advertise a part-time role, so the real route is to read lab websites, pick groups, and write to them. The mode is for the moment before that: **choosing which groups deserve a lab-page look and a message.** It is not for anyone who needs a visa, and it does not apply to a posted job (the engine's scan and scorer already cover those).

## The information asymmetry

A lab's website says what the lab studies. It never says whether the lab can pay a collaborator. That fact is on record: federal research awards are published, with the institution, the dates and the amount. A person who does not know the award databases, or the way award types differ, writes to forty labs and learns by silence which ones had no money. The engine's own premise is that the job-search problem is information, not motivation; this is the same premise applied to a market where nothing is advertised.

## How it connects to the engine's three layers

- **80 Days to Stay (funding signal).** The engine uses SEC Form D filings to tell a company that just raised money from one that did not. Federal award records play the same part for a lab: they are the funding signal that comes before any hiring. The unit changes (a funded project, not a company), and so does the question (can this pay a part-time collaborator, not will this sponsor a visa).
- **Job-Ops (liveness is a gate).** If a lab names an opening at a web page, the engine's liveness check applies to that page, and an `uncertain` result counts as not live. In the worked run the check returned `uncertain` for a made-up closed posting, which is why the mode treats uncertain as a failure.
- **The Cognitive Pivot (role quality).** The mode names a national wage floor from the engine's BLS extract for the occupations the work resembles. The Boston wage floor is the part that did not run: its input files are not in the repository (see the recipe).

Sponsorship, the engine's centre, is a non-issue for this person; the visa-timeline gate becomes an availability-window gate (start date, hours).

## Failure modes specific to this domain

1. **A big number that looks like capacity and is not.** A table that says "$68 million in single-cell awards at Boston Children's" invites the reading "there is money here to pay me." The shape of the error: the amounts are *annual* (NIH) or *total over years* (NSF), are tied to specific aims, and in the run 24 of 127 Boston Children's awards and 29 of 99 at Harvard Medical School were fellowships or training grants that pay one named person's training. The database's own count also overstates: RePORTER reported 130 rows for Boston Children's and 54 for MIT, but only 127 and 48 distinct projects (checked in the worked run). **Hardest to catch for** someone outside US research funding, such as a business-school colleague, an engineer or an international applicant, who has no reason to know that a K99 or an F31 is not a lab's budget or that one award can appear in several rows.
2. **A silent zero that reads as "no money."** An institution can return no awards because it has none or because the name is wrong. In the run, a one-letter typo returned zero, a partial name (`HARVARD`) quietly matched three different organisations, and the NSF search for Northeastern returned 227 awards of which 222 belonged to other universities. A reader sees a short or empty row and concludes the institution has nothing. **Hardest to catch for** anyone who does not know that these databases spell organisations differently, which is most people outside grants administration. The mode's control query and its list of returned organisation names exist for this, and for NSF, which has no control query, a zero is never treated as evidence.

*Written 2026-10-19. The run numbers are from `runs/` in this folder; none is quoted from memory.*
