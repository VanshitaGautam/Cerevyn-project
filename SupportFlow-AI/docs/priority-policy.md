# Priority policy

This project uses a small, transparent keyword baseline. It is a demonstration policy, not a substitute for a production incident-management policy.

- **Critical:** messages explicitly mentioning a complete outage, all users affected, system down, or a security/data breach.
- **High:** messages mentioning urgent action, inability to access an account, being locked out, or duplicate charges.
- **Medium:** other clearly categorized Billing, Technical, or Access tickets; ambiguous tickets are also Medium while awaiting review.
- **Low:** clearly categorized General questions.

The classifier normalizes whitespace and case, scores category keywords, and routes a ticket for review if no category has a unique winning score. A human must approve the draft before its status becomes `READY`. The current demo approval endpoint is not authenticated; do not expose it publicly as a production workflow without adding authentication, authorization, audit logging, and access controls.
