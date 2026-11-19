# Score experiment predictions (written before running, 2026-11-19)
Held-out: 28 postings I labeled blind (23 NOT_RELEVANT, 5 CANNOT_TELL, 0 RELEVANT). So these experiments measure false keeps, not missed jobs.
1. Threshold 5 -> 6: fewer keeps; false keeps (keep & my NOT_RELEVANT) drop or stay the same. Threshold 5 -> 4: more keeps, more false keeps.
2. Filter file v1.0 -> v1.1 (C4): false keeps drop or stay the same.
3. Claude prompt baseline -> revision: I expect the revision to call fewer of my NOT_RELEVANT postings RELEVANT.
4. Control (baseline prompt run twice): I expect a few verdicts to differ between the two identical runs. That would be sampling, not learning: every call is a fresh
   `claude -p` process with no memory, so a difference across runs is not evidence that anything was trained.
