# Manual demo integration checks

This directory is intentionally excluded from the default test suite and CI. It must never contain credentials.

Run a demo test only after explicitly exporting temporary demo credentials and setting a dedicated opt-in variable. Any future mutation test must create a uniquely namespaced resource, retain its returned identifier, and delete only that identifier in `finally` cleanup.

Do not add account-wide cleanup or tests that enumerate and delete unrelated positions or working orders.
