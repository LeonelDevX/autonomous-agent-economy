# Wallet Security

Private keys never enter the LLM context.

Agent -> Transaction Request -> Policy Engine -> Human Approval -> External Signer -> Payment Provider

The MVP provides abstractions only. Real signing should be implemented in a separate signer process or hardware wallet flow.
