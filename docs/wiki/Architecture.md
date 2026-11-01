# KMC Knowledge Assistant — Architecture

## System flow

```mermaid
flowchart TD
 A[chatbot.csv knowledge base] --> B[Prepare text and build TF-IDF artifacts]
 B --> C[Vectorizer and document matrix]
 D[User question] --> E[Vectorize question]
 C --> E
 E --> F[Cosine similarity ranking]
 F --> G{Best score meets threshold?}
 G -->|Yes| H[Return matched answer]
 G -->|No| I[Ask user to rephrase]
 H --> J[Flask JSON API]
 I --> J
 J --> K[Browser interface]
```

## Design notes

- Keep user-interface responsibilities separate from model, API and data-service responsibilities.
- Validate inputs at the application boundary and return clear error messages.
- Keep secrets and privileged credentials on the server side.
- Document the versions of data, dependencies and model artifacts used for reproducible results.
- Test the full user journey after deployment, not only the build step.

## Deployment boundary

GitHub Pages can host static HTML, CSS, JavaScript and prebuilt frontend assets. It cannot execute Python/Flask services, server-side React Router actions, private environment variables or database operations. Those parts require a separate backend or application host.
