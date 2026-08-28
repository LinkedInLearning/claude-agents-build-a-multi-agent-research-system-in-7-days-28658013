# The Impact of AI Coding Assistants on Developer Productivity and Code Quality: A Research Report

## Executive Summary

AI coding assistants have reached near-universal adoption among professional developers (84–90%) [1][2][20], and the evidence consistently shows large speedups on short, well-bounded coding tasks (21–55%) [5][6][7][8][9] as well as increased enterprise throughput metrics such as pull requests, commits, and builds [10][11][23]. However, the picture darkens on three fronts: experienced developers working in large, familiar codebases were measured 19% *slower* with AI assistance despite predicting and later believing they were faster [3][4]; independent studies find AI-generated code carries more security vulnerabilities than human-written code, at rates ranging from roughly 24% to 72% depending on methodology [27][28][29][30]; and code-quality proxies (churn, duplication, declining refactoring) trend in a negative direction across large commit datasets [24]. A recurring and well-documented perception-reality gap means developers and organizations often believe AI is helping more than objective measurement shows [2][3][4][27]. Net benefit is heavily moderated by task type, codebase familiarity, developer experience, and usage pattern, and several important questions—including the experience-level conflict and the source of DORA's 2024-to-2025 delivery-stability reversal—remain explicitly unresolved in the underlying evidence.

## Findings

### Overview and Adoption

Adoption of AI coding assistants is now near-universal and still rising. DORA's 2025 report finds 90% adoption, up 14 percentage points year-over-year [1]. The Stack Overflow 2025 Developer Survey finds 84% usage, up from 76% in 2024 [2]. Gartner forecasts 90% of enterprise software engineers will use AI code assistants by 2028, up from less than 14% in early 2024 [20]. Despite this near-total adoption, the evidence on net value is mixed once studies move beyond short tasks and self-reported sentiment into controlled measurement of complex, real-world work [3][4][22].

### Productivity: Controlled and Field Evidence

**Short, bounded tasks show large, consistently replicated speedups.** In a GitHub/Microsoft study, Copilot users completed an HTTP-server-in-JavaScript task 55% faster than a control group, with a higher completion rate (78% vs. 70%) [5]. An independent academic replication found a near-identical 55.8% speedup [6][7]. In a more realistic enterprise setting, Google engineers (n=96) completed a C++ task (~474 lines of code across 10 files) about 21% faster with AI assistance (roughly 96 minutes vs. 114 minutes) [8][9].

**Enterprise field RCTs show increased throughput proxies.** Across Microsoft, Accenture, and a Fortune 100 electronics manufacturer (more than 5,000 developers), a large field RCT found completed pull requests up 26%, commits up 13.55%, and builds up 38.38%; within the Accenture arm specifically, PRs per developer rose 8.69%, PR merge rate rose 11%, and successful builds rose 84% [10]. Overlapping figures are also reported in a related publication, though the sample size is cited inconsistently there (4,867 vs. 1,974) [11].

**Experienced developers in large, familiar codebases were measurably slower.** A rigorous randomized controlled trial by METR studied 16 experienced open-source developers completing 246 real tasks in large, mature repositories they already knew well (averaging 22,000+ stars and 1,000,000+ lines of code). AI use (Cursor + Claude) produced a 19% *slowdown*, attributed to time spent reviewing and correcting AI suggestions that were "directionally correct but not exactly right" [3][4]. This finding was widely discussed in secondary commentary [12][13][14][15][16].

**Skill-acquisition tradeoff.** An Anthropic RCT found that AI assistance produced a statistically significant *decrease* in mastery when developers were learning a new Python library, even though it may have aided task completion [17].

**Well-being and sentiment gains are consistent and largely uncontested,** even in studies where objective productivity effects are flat or negative. In the GitHub/Microsoft study, 60–75% of developers reported greater job fulfillment and less frustration, 73% said Copilot helped them stay in flow, and 87% said it helped preserve mental effort on repetitive tasks [5]. In the Accenture RCT arm, 90% reported greater job fulfillment, 91% said they enjoyed coding more, and 70% reported reduced mental effort on repetitive tasks [10].

**Enterprise/survey-level productivity evidence.** GitHub/Accenture enterprise research found up to 55% faster coding, a drop in PR cycle time from 9.6 to 2.4 days (a 75% reduction), a 15% increase in PR merge rate, and an 84% increase in successful builds [23]. McKinsey reports 20–45% productivity gains on targeted tasks, reduced onboarding time for junior developers, and roughly 80% of individual users reporting improved personal productivity [21]. DORA's 2024 report found AI adoption associated with increased individual productivity, flow state, and job satisfaction, along with self-reported gains of +3.4% in code quality and +3.1% in code review speed [22]. The Cui et al. field study found a 26.08% overall increase in completed tasks, with the largest gains among less-experienced developers, and up to approximately 40.5% more PRs in the highest-usage weeks compared with zero-usage weeks [11].

**Organizational/delivery-system effects are mixed and time-variant.** DORA's 2024 report found that a 25% increase in AI adoption was associated with a 7.2% *decrease* in delivery stability and a 1.5% *decrease* in delivery throughput, hypothesized to reflect AI enabling larger batch sizes or changelists [22]. DORA's 2025 report reverses this, linking AI adoption to *higher* delivery throughput and proposing an "amplifier" thesis in which AI boosts high-performing organizations while intensifying dysfunction in weak-process organizations [1]. Separately, McKinsey notes that despite roughly 80% of individuals reporting personal productivity gains, most organizations are not seeing measurable enterprise-level earnings contribution from AI investment [21].

**Trust and sentiment are declining even as usage rises.** The Stack Overflow 2025 survey found only 29% of developers trust AI accuracy (down 11 points year-over-year), 46% actively distrust it, and only 3% report "high trust." Positive sentiment fell from over 70% in 2023–2024 to 60% in 2025. The top-cited frustration (45%) is AI code that is "almost right, but not quite," and 66% of developers report spending more time fixing AI output [2].

**A gap exists between purchased licenses and actual use.** Gartner reports that fewer than half—sometimes fewer than a third—of purchased AI coding assistant licenses see active use after several months [20].

### Code Quality and Maintainability

Analysis of a large commit dataset (211 million changed lines) by GitClear found that code churn (lines reverted or substantially updated within two weeks of being written) rose from 3.1% in 2020 to 5.7% in 2024. Refactored or "moved" code fell from roughly 25% in 2021 to under 10% in 2024 (also reported in parallel as a decline from 24.1% to 9.5%), while copy-pasted/cloned code rose from 8.3% to 12.3%, making 2024 the first year copy-paste code exceeded refactored code—a roughly 48% relative increase. Duplicated code blocks increased roughly 8-fold, and commits containing duplicated blocks rose roughly 10-fold over two years [24]. A 2026 GitClear follow-up found 47% more "error masking" (rescue/catch blocks, safe-navigation operators, stubbed methods) compared with a pre-AI baseline [24].

A LeadDev synthesis reports that human reviewers rejected 72% of AI-agent-generated patches for maintainability concerns in some organizational reviews, though this figure is not traceable to a named primary study and should be treated as unverified [25].

Harness's "State of Software Delivery 2025" survey found that 67% of developers report spending more time debugging AI-generated code, 68% report more time resolving AI-related security vulnerabilities, and 59% report deployment errors at least half the time when using AI tools; the report estimates organizations lose roughly $8 million per year per 250 developers, partly from increased review and QA burden, and flags "shadow AI" governance and IP-leakage concerns [26].

### Security

A controlled study by Perry, Srivastava, Kumar, and Boneh (ACM CCS 2023, n=47, using an early Codex-based assistant) found that AI-assisted participants produced significantly less secure code than non-AI controls across five tasks in Python, JavaScript, and C, particularly around string encryption and SQL injection. AI-assisted participants were also more likely to believe their code was secure despite it being less so—a "confidence trap": the group that produced the least-secure code trusted AI most (4.0 out of 5.0), while the group that produced the most-secure code trusted it least (1.5 out of 5.0) [27].

Pearce et al. (IEEE S&P 2022) analyzed 89 scenarios drawn from the MITRE CWE Top-25 and 1,689 Copilot-produced programs, finding that roughly 40% contained vulnerable code (39.33% of top suggestions; 40.73% across all suggested options) [28].

Fu et al. (ACM TOSEM) analyzed 733 real-world code snippets generated by Copilot, CodeWhisperer, and Codeium, finding that 29.5% of Python snippets and 24.2% of JavaScript snippets contained security weaknesses spanning 43 CWE categories, including 8 from the 2023 CWE Top-25 (CWE-330, CWE-94, CWE-79). Feeding static-analysis warnings back into Copilot Chat fixed up to 55.5% of identified issues [29].

Veracode's 2025 GenAI Code Security Report, with a Spring 2026 update, tested 100+ LLMs across 80 real-world tasks in 4 languages and found GenAI-introduced vulnerabilities in 45% of cases overall, with Java the riskiest language at a 72% failure rate. Models failed to defend against cross-site scripting (CWE-80) in 86% of relevant samples and against log injection in 88% of cases. AI-generated code was found to have 2.74 times more vulnerabilities than human-written code for comparable tasks, and newer, more capable models have not shown security improvement despite better functional correctness [30].

### Skill Formation and Over-Reliance

A study reported by AI CERTs News, involving a randomized trial of 52 junior Python developers, found that the AI-assisted group scored 50% on a follow-up quiz compared with 67% for controls—a 17-point gap. Learning-preserving usage patterns, such as prompting for explanations or conceptual dialogue rather than full delegation, mitigated the deficit [31].

Scientific American and a 2026 arXiv preprint on skill formation both report that AI-assisted coding may degrade skill formation, particularly under full-delegation usage patterns [32][33]. This is corroborated independently by the Anthropic RCT's finding of decreased mastery when learning a new library with AI assistance [17].

A peer-reviewed literature review in Springer's AI & SOCIETY (covering studies from 2015–2025) frames automation bias more narrowly than a blanket "over-trust" phenomenon: damage is concentrated in cases where users accept incorrect AI output on tasks they could otherwise have completed correctly themselves [34].

### Perception vs. Reality Gap

This theme recurs across multiple independent lines of evidence. In the METR RCT, experienced developers predicted before the study that AI would speed them up by 24%; after the study measured an actual 19% slowdown, they still believed AI had sped them up by roughly 20% [3][4][12][13][16]. In the Stack Overflow 2025 survey, declining trust (29%, down 11 points) and rising "almost right" frustration (45%) persist alongside continued high usage (84%) [2]. In the security domain, Perry et al. found that AI-assisted participants were more likely to believe their (objectively less secure) code was secure, with the least-secure-code group trusting AI most and the most-secure-code group trusting it least [27].

### Moderating Factors: Who Benefits Most

Task type and codebase familiarity appear to be the most consistently invoked moderator of AI's productivity effect. Short, bounded, or greenfield tasks show large speedups [5][6][7][8][9], while long-horizon tasks in large, mature, deeply familiar codebases show a slowdown [3][4]. No single study directly manipulates codebase size or familiarity as an experimental variable, so this remains an inferred, not directly proven, explanation.

Junior developers appear to benefit most in several sources: Peng et al. [6], a 2026 enterprise study [35], and McKinsey [21] all report junior developers gaining the most in relative terms, and McKinsey separately reports reduced onboarding time for juniors [21]. However, the Google/DORA enterprise-task RCT found that senior developers saw slightly larger gains than juniors on a realistic C++ task [8][9]. Gartner separately flags a "skills-experience paradox" risk specifically for junior developers, reflecting a long-term skill-risk framing distinct from short-term productivity gains [20].

## Conflicting Evidence

**Speedup vs. slowdown.** GitHub/Microsoft, Peng et al., and Google/DORA all found substantial task-level speedups from AI assistance (21–55%) on short or moderately realistic tasks [5][6][7][8][9], while METR found a 19% slowdown for experienced developers working in large, mature, deeply familiar codebases [3][4]. These findings are treated as reconcilable via task type and codebase familiarity as moderators, but no study directly tests this mechanism, so the reconciliation remains inferential rather than proven.

**Sample-size inconsistency in enterprise field data.** Cui et al.'s field RCT and an overlapping/related publication report the same underlying study with inconsistent sample sizes (4,867 vs. 1,974) [10][11]. This inconsistency is preserved and unresolved.

**PR merge-rate discrepancy.** GitHub/Accenture enterprise research reports a 15% increase in PR merge rate [23], while Cui et al.'s Accenture-specific arm reports an 11% increase [10]. Both figures are carried forward as reported, unresolved.

**DORA's 2024-to-2025 reversal on delivery stability and throughput.** DORA's 2024 report found AI adoption associated with decreased delivery stability (-7.2%) and throughput (-1.5%) [22], while DORA's 2025 report finds AI adoption associated with higher delivery throughput and proposes an "amplifier" thesis [1]. Neither report empirically traces whether this reversal reflects genuine tooling improvement, organizational process maturity change, or measurement/methodology drift across years; this is carried forward as an explicitly unresolved tension.

**Vulnerability-rate divergence.** Fu et al.'s real-world snippet analysis (24.2–29.5%) [29], Pearce et al.'s synthetic CWE-scenario analysis (~40%) [28], and Veracode's cross-model benchmark (45% overall, 72% for Java) [30] cannot be collapsed into a single comparable figure. They differ in task design (real-world vs. synthetic), language and model coverage, detection methodology, and time period (2021–2026 tool generations). All three figures are preserved independently; no single "true" vulnerability rate can be stated.

**Internally inconsistent GitClear churn figures.** GitClear's own reporting shows churn rising from 3.1% to 5.7% between 2020 and 2024 [24], while a separately cited figure (rising from 3.3% to 7.1% by 2025) has no traceable URL in the source material and cannot be reconciled with the first figure.

**Junior vs. senior benefit conflict.** Peng et al. [6], the 2026 enterprise study [35], and McKinsey [21] find juniors benefit most in relative terms, while the Google/DORA RCT finds seniors gained slightly more on a specific realistic task [8][9]. Gartner's "skills-experience paradox" for juniors [20] adds a long-term risk framing that sits in tension with, but does not directly contradict, the short-term gain findings. No source in the underlying evidence reconciles junior-vs-senior benefit under one consistent metric or methodology.

## Confidence and Limitations

### Confidence Summary

| Conclusion | Confidence | Basis |
|---|---|---|
| AI adoption is near-universal and still rising | High | Multiple independent, large-sample, recent surveys agree [1][2][20] |
| Short/bounded-task speedups are real and substantial | High | Three independent RCTs converge on similar magnitudes [5][6][7][8][9] |
| Enterprise throughput proxies (PRs/commits/builds) rise with AI access | High | Large-sample field RCT plus enterprise field data [10][11][23] |
| Experienced developers in large/familiar codebases can be slowed by AI | Medium-high | Single RCT with rigorous causal design but small sample (n=16) [3][4] |
| A perception-reality gap exists between believed and actual AI benefit | High | Demonstrated directly in a pre/post RCT design; consistent with survey trust decline and a security "confidence trap" [2][3][4][27] |
| AI-assisted code shows more churn, duplication, and reduced refactoring over time | Medium | Large-scale (211M lines) but single vendor source, non-peer-reviewed, with an internal inconsistency in churn figures [24] |
| AI-generated code introduces measurably more security vulnerabilities than human code | Medium-high | Multiple independent studies agree directionally; exact magnitudes differ by methodology and are not reconcilable into one figure [27][28][29][30] |
| AI assistance can impair skill acquisition under full-delegation use | Medium | Two independent RCT-style designs plus a peer-reviewed review converge; no long-term longitudinal data exists [17][31][32][33][34] |
| Junior vs. senior developers benefit differently from AI | Low (unresolved) | Direct conflict across sources using different metrics; no reconciling source [6][8][9][20][21][35] |
| Organizational-level delivery stability/throughput effects of AI | Low-medium (unresolved) | Reversal between 2024 and 2025 DORA reports is not mechanistically explained [1][22] |

### Unresolved Tensions and Open Questions

- The mechanism behind the speedup-vs-slowdown divergence (task type/codebase familiarity) has not been directly tested experimentally [3][4][5][6][8].
- The experience-level conflict (juniors vs. seniors benefiting most) is unreconciled across sources using different metrics [6][8][20][21][35].
- DORA's 2024-to-2025 reversal on delivery stability/throughput is hypothesized but not empirically traced [1][22].
- Vulnerability-rate magnitudes from Fu et al., Pearce et al., and Veracode cannot be collapsed into one comparable figure due to differing methodologies [28][29][30].
- GitClear's churn figures are internally inconsistent across reporting periods and not clarified by the underlying sources [24].
- No rigorous peer-reviewed causal study of current-generation (2025–2026) frontier models on security outcomes with a matched control group exists; the strongest controlled security studies use earlier model generations [27][28].
- No source reconciles GitClear's maintainability/churn proxies with the direct security-vulnerability literature into a unified framework.
- No long-term longitudinal data exists on skill atrophy, technical debt accumulation, or the durability of the Anthropic mastery-decrease finding [17].
- No quantification of downstream real-world security incidents (breaches, CVEs) attributable to AI-code overconfidence exists in the evidence reviewed.
- Whether the perception-reality gap documented by METR also applies to the positive self-reported sentiment/satisfaction metrics from GitHub/Microsoft and Accenture is untested [3][4][5][10].
- Most quality/security studies do not break results down by AI tool/model, agentic vs. autocomplete configuration, language, or task complexity; Veracode is a partial exception with cross-model coverage [30].
- Financial/ROI modeling detail at the organizational level is limited; McKinsey notes an individual-vs-enterprise gap without quantitative modeling, and Gartner's license-utilization figures are forecast-style [20][21].
- The evidence base is heavily Western/US enterprise-centric, with no demographic or regional breakdowns available.
- Vendor/commercial interest is a plausible but unconfirmed confound for several sources with a commercial stake in their own conclusions (GitHub/Microsoft evaluating its own Copilot product, GitClear, Harness, Veracode) [5][10][23][24][26][30].

### Unsourced Claims (excluded from Findings citations, noted here per synthesis)

The following claims appear in the underlying synthesis but carry no traceable URL and are therefore not cited in the Findings above; they are noted here for completeness rather than treated as evidentiary support:
- A GitClear figure reporting churn rising from 3.3% to 7.1% by 2025 (distinct from the sourced 3.1%→5.7% figure).
- A LeadDev-cited 72% patch-rejection rate lacking a traceable primary study (the LeadDev source itself is cited [25], but the underlying primary study is not).
- HBR (September 2025, BetterUp Labs/Stanford Social Media Lab, n=1,150): 41% received AI "workslop" in the past month; average 1 hour 56 minutes to resolve; roughly $186/worker/month (~$9M/year for a 10,000-person company); 53% annoyed; 42% viewed the sender as less trustworthy.
- Secondary Gizmodo coverage emphasizing "shifting work downstream."
- An arXiv 2026 paper titled "An Endless Stream of AI Slop," and blog commentary from Codacy and Atomic Robot, on rising reviewer burden and fatigue.
- A Security Scientist blog summary of the Perry et al. findings.
- A Kusari.dev blog claim of a 322% jump in privilege escalation paths and a 153% spike in architectural design flaws in AI-assisted codebases.
- A DEV Community post describing emerging gaps in systems design, memory management, concurrency, and security architecture among junior/mid-level developers.
- A Philipp Dubach blog report that aggregate self-reported productivity gains are modest (~10%) despite ~93% adoption, with only 16.3% reporting "great extent" improvement and 41.4% reporting little/no effect.
- A Medium/StartupInsider report that juniors gain 21–40% in relative task speed vs. 7–16% for seniors.
- A Fastly blog report that seniors ship 2.5x more AI-generated code into production than juniors (32% vs. 13% reporting more than half of production code is AI-generated).
- A Cerbos blog reference noted in the source material without an associated specific claim.

## References

1. DORA. "DORA 2025 Report." https://dora.dev/dora-report-2025/
2. Stack Overflow. "2025 Developer Survey — AI." https://survey.stackoverflow.co/2025/ai
3. METR. "Early 2025 AI Experienced OS Dev Study" (blog). July 10, 2025. https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
4. METR. Research paper (arXiv). https://arxiv.org/pdf/2507.09089
5. GitHub. "Research: Quantifying GitHub Copilot's Impact on Developer Productivity and Happiness." https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/
6. Peng, S., Kalliamvakou, E., Cihon, P., & Demirer, M. arXiv. https://arxiv.org/abs/2302.06590
7. MIT Economics. "Draft Copilot Experiments." https://economics.mit.edu/sites/default/files/inline-files/draft_copilot_experiments.pdf
8. Google/DORA. "Impact of Generative AI in Software Development" (PDF). https://services.google.com/fh/files/misc/dora-impact-of-generative-ai-in-software-development.pdf
9. Osmani, A. "The Reality of AI-Assisted Software" (Substack commentary). https://addyo.substack.com/p/the-reality-of-ai-assisted-software
10. Cui, Z., Demirer, M., Jaffe, S., Musolff, L., Peng, S., & Salz, T. arXiv. https://arxiv.org/pdf/2410.12944
11. MIT GenAI. PubPub publication. https://mit-genai.pubpub.org/pub/v5iixksv
12. Willison, S. "AI, Open Source, Productivity" (blog, July 12, 2025). https://simonwillison.net/2025/Jul/12/ai-open-source-productivity/
13. IT Brew. "AI Coding Tools Might Actually Be Slowing You Down" (August 4, 2025). https://www.itbrew.com/stories/2025/08/04/ai-coding-tools-might-actually-be-slowing-you-down/
14. Goedecke, S. "Impact of AI Study" (blog). https://www.seangoedecke.com/impact-of-ai-study/
15. Augment Code. "Why AI Coding Tools Make Experienced Developers 19% Slower — and How to Fix It" (guide). https://www.augmentcode.com/guides/why-ai-coding-tools-make-experienced-developers-19-slower-and-how-to-fix-it
16. Let's Data Science. "Developers Thought AI Made Them Faster, the Data Said Otherwise" (blog). https://letsdatascience.com/blog/developers-thought-ai-made-them-faster-the-data-said-otherwise
17. Anthropic. "AI Assistance and Coding Skills" (research). https://www.anthropic.com/research/AI-assistance-coding-skills
18. arXiv. Longitudinal case study on AI coding tool effects. https://arxiv.org/pdf/2509.20353
19. arXiv. Security/quality impacts reference. https://arxiv.org/pdf/2502.13199
20. Gartner. "Gartner Says 75 Percent of Enterprise Software Engineers Will Use AI Code Assistants by 2028" (press release, April 11, 2024). https://www.gartner.com/en/newsroom/press-releases/2024-04-11-gartner-says-75-percent-of-enterprise-software-engineers-will-use-ai-code-assistants-by-2028
21. McKinsey & Company. "Unleashing Developer Productivity with Generative AI." https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai
22. DORA. "2024 DORA Report." https://dora.dev/research/2024/dora-report/
23. GitHub. "Research: Quantifying GitHub Copilot's Impact in the Enterprise with Accenture." https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/
24. GitClear. "Coding on Copilot" / "AI Copilot Code Quality" reports, plus 2026 follow-up. gitclear.com
25. LeadDev. Synthesis on AI-agent patch review/maintainability. leaddev.com
26. Harness. "State of Software Delivery 2025." harness.io
27. Perry, N., Srivastava, M., Kumar, D., & Boneh, D. ACM CCS 2023 (arXiv). https://arxiv.org/abs/2211.03622
28. Pearce, H. et al. IEEE S&P 2022 (arXiv). https://arxiv.org/abs/2108.09293
29. Fu, Y. et al. ACM TOSEM (arXiv). https://arxiv.org/abs/2310.02059
30. Veracode. "2025 GenAI Code Security Report" and Spring 2026 update. veracode.com
31. AI CERTs News. "AI Study Shows Code Skill Atrophy from Assistants." https://www.aicerts.ai/news/ai-ld-study-shows-code-skill-atrophy-from-assistants/
32. Scientific American. "Is AI Ruining Our Skills? Early Results Are In, and They're Not Good." https://www.scientificamerican.com/article/is-ai-ruining-our-skills-early-results-are-in-and-theyre-not-good/
33. arXiv. Skill formation preprint (2026). https://arxiv.org/html/2601.20245v1
34. Springer, AI & SOCIETY. Literature review (2015–2025 studies). https://link.springer.com/article/10.1007/s00146-025-02422-7
35. arXiv. Enterprise study on junior/newer hires (2026). https://arxiv.org/html/2601.20112v1