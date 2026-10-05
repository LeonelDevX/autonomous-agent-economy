# Security Policy

Private keys, seed phrases, wallet passwords, payment credentials, and API keys must never be sent to the LLM, logged, committed, or stored in normal project files.

Core rules:

- Simulation mode is default.
- Real mode requires explicit configuration.
- Critical actions always require human approval.
- Internet content is untrusted input.
- Unknown tools are denied.
- Non-allowlisted domains are denied.
- Kill switch blocks new tasks, publishing, and payments.
