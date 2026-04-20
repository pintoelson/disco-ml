### PROTOCOL

1. Analyze the provided Title and Abstract against the Inclusion (IC) and Exclusion (EC) criteria.
2. Maintain high "Inter-Rater Reliability" by strictly adhering to the text; do not infer methodologies not mentioned.
3. If the paper mentions "Decision-making" but lacks "Documentation" or "Formal Modeling," it should likely be Excluded or marked Uncertain.

### INPUT DATA

- **Inclusion Criteria (IC):** {INCLUSION_CRITERIA}
- **Exclusion Criteria (EC):** {EXCLUSION_CRITERIA}
- **Title:** {TITLE}
- **Abstract:** {ABSTRACT}

### TASKS

1. **Summarize:** Provide a 2-sentence technical summary.
2. **Screening Decision:** Select [Include, Exclude, Uncertain].
3. **Criteria Mapping:** Explicitly list which ICs were met and which ECs were triggered.
4. **Scoring:** Assign a value from 0.0 to 1.0. Do NOT round to 0.5 or 1.0. Calculate the value based on:

- **0.8 - 1.0**: Matches multiple ICs with explicit keywords in the abstract. High relevance to Ontology/MLOps.
- **0.6 - 0.7**: Matches at least one IC clearly, but depth is unclear from the abstract alone.
- **0.4 - 0.5**: Ambiguous. Mentions keywords but lacks context of "Documentation" or "Formalism."
- **0.1 - 0.3**: Triggers an EC, but has some tangential relevance to MLOps.
- **0.0**: Strong EC trigger (e.g., purely medical, unrelated physics, or non-English).

  **Instruction:** You must provide a specific decimal  to reflect the nuance of the match.

5. **Strict Grounding:** Do NOT mention unrelated machine learning architectures (e.g., Transformers, LLMs, CNNs) unless they are the primary subject of the Abstract. Focus on the ICs and ECs.

### OUTPUT FORMAT (STRICT JSON)

Return ONLY a valid JSON object:
{{
  "summary": "string",
  "decision": "Include | Exclude | Uncertain",
  "matched_ic": ["ICx", "ICy"],
  "triggered_ec": ["ECx"],
  "justification": "A rigorous explanation. STRICTION: Only use keywords found in the provided TITLE and ABSTRACT. If a concept is not explicitly mentioned in the input, do not include it. Reference the specific IC/EC IDs used.",
  "score": float
}}
