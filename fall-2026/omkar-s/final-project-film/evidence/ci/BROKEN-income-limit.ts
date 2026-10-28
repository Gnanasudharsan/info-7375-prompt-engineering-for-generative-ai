// MUTANT (Omkar's, 2026-10-22): the minimum income is changed from ₹15,000 to ₹1,500.
// In Omkar's words: "This could let applicants qualify even though their income is below the actual requirement."
// (Omkar chose this bug and wrote the sentence above in chat; Claude typed it into this file.)

import { RULES } from "../../src/constants.js";

export function incomeRuleRejection(monthlyIncome: number): string | null {
  if (monthlyIncome < 1500) {
    return `Monthly income below minimum ₹${RULES.MIN_MONTHLY_INCOME}`;
  }
  return null;
}
