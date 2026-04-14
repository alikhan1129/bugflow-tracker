# AI Guidance & Constraints

This file outlines the foundational mandates and engineering standards used to guide AI agents (like Gemini CLI) during the development of BugFlow.

## Foundational Mandates
- **Pragmatic Minimalism**: Prioritize simplicity over abstraction. Avoid unnecessary layers, files, or patterns.
- **Contextual Precedence**: Instructions in this file and `proj details.txt` take absolute precedence over general defaults.
- **Technical Integrity**: All changes must include validation logic. Bug fixes must be empirically reproduced before being patched.

## Engineering Standards
- **Correctness**: Status transitions must be strictly enforced (OPEN → IN_PROGRESS → RESOLVED → CLOSED).
- **Interface Safety**: Use Pydantic for strict input validation. AI outputs must be parsed and validated against expected schemas with intelligent fallbacks.
- **Observability**: Failures in external integrations (like LLMs) must be visible via logs and handled gracefully with user-facing fallbacks.
- **Change Resilience**: Logic is encapsulated in `services.py` to ensure that adding features (like a new database or AI model) has minimal impact on the rest of the system.

## AI Usage Rules
- **Temperature Control**: LLM calls must use a low temperature (0.2) to ensure deterministic triaging.
- **Validation Layer**: AI-generated content is treated as untrusted. It must be validated against `AITriageResponse` schemas.
- **Smart Fallback**: When the AI fails or provides invalid data, the system must utilize a keyword-based heuristic layer to maintain functional correctness.
