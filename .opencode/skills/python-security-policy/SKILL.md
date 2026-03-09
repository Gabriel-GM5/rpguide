# Python Security Policy

The agent must enforce the following:

- no hardcoded secrets
- use os.environ for secrets
- validate all inputs
- avoid unsafe deserialization
- avoid eval and exec

Never expose:

- API keys
- credentials
- tokens
- environment variables