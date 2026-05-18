# CrisisLens architecture

```mermaid
flowchart TD
    A[Field photo] --> C[Gemma 4 multimodal prompt]
    B[Short field note] --> C
    C --> D[Strict JSON crisis schema]
    D --> E[Schema normalization + safety defaults]
    E --> F[Deterministic routing tool]
    F --> G[Human coordinator review]
    G --> H[SMS / radio summary]
    G --> I[JSON + Markdown export]
```

## Design principle

CrisisLens deliberately separates model reasoning from operational routing.

- Gemma 4 extracts and reasons over evidence.
- The app normalizes and displays the report.
- A deterministic tool routes reports by incident type and urgency.
- A human coordinator verifies before action.

This design makes the prototype easier to audit and safer than a fully autonomous responder agent.
