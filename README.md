# rpguide
Personal Persona-Based AI Assistant for General Purposes Usage

## Configuration
Configure the application using environment variables (create a `.env` file
based on `.env.example`). Key variables include the model, API key, language,
and the `DEBUG` flag. When `DEBUG` is set to `true` (or `1`), the app will
print which internal agent is being used for each request.

Example `.env` variables:

- `LLM_TYPE` - e.g. `gemini`
- `LLM_AI_API_KEY` - your provider API key
- `LLM_AI_MODEL` - the model id to use
- `EMBEDDINGS_AI_MODEL` - the embedding model id
- `LANGUAGE` - `en_us` or `pt_br`
- `DEBUG` - `true` or `false` (when `true`, prints which agent is used)

See `.env.example` for a full sample.
