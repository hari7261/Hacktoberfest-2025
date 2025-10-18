# Good First Issues for FactReal

These are small, well-scoped tasks ideal for new contributors.

1) Improve transformer loading/caching
- Detect offline mode and prefer local HF cache
- Expose env to configure cache dir
- Add a startup check that warms model pipelines if available

2) Better explainability prompts
- Add prompt templates per label (biased/misleading/propaganda)
- Add a temperature/length config in .env
- Unit test to ensure non-empty explanations

3) Expand fact_checker with NewsAPI filters
- Add language and date filters from .env
- Aggregate publisher names into the response
- Graceful degradation on HTTP errors with detailed notes

4) Add language detection in preprocessing
- Use langdetect or fasttext to detect language
- Return language in classification response for context
- Skip reasoning for unsupported languages (configurable)

5) Rate limit and error middleware
- Simple sliding window per IP (in-memory)
- Consistent JSON error envelope
- Correlation ID in logs and responses

6) Postman collection & docs polish
- Add environment file for base URL
- Add examples for negative/neutral texts
- Document common 4xx cases in README

How to pick up an issue
- Comment on the issue to claim it
- Discuss approach briefly if changing public APIs
- Open a Draft PR early, convert to Ready when tests pass