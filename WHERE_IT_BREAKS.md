# Where it breaks / don't over-trust

1. **Paraphrases outside the implemented patterns.** The assistant uses simple keyword routing rather than semantic retrieval. An unusual phrasing can fall through to `CANNOT_ANSWER` or match the wrong branch.
2. **Multiple amounts in one question.** Fee extraction is heuristic. If a question contains several unrelated amounts, the selected transaction amount can be wrong; add explicit structured parsing before production use.
3. **Merchant-specific and calendar-dependent facts.** The code does not know a customer's actual bank limit, merchant KYC status, local bank holidays, or whether a closure request was processed. It must not claim exact account-specific outcomes.
