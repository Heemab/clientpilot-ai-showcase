# Rotate the private deployment credentials

These steps require the owner or a delegated administrator to access the relevant deployment, database, and provider accounts. Apply them to the private project and its deployed services. Store new values in the deployment secret manager and use the ignored `backend/.env` only for local development. Update all workers and other consumers before checking that the new configuration is live. Review provider activity for unexpected use.

## Django signing key

Use the private project's active virtual environment. On Windows PowerShell, generate a compatible key directly into the clipboard:

```powershell
python -c "import secrets; print(secrets.token_hex(32))" | Set-Clipboard
```

Paste it as `SECRET_KEY` in the private deployment's secret manager. For a private local checkout, update `backend/.env`. Clear the clipboard with `Set-Clipboard -Value ''` and delete the value from clipboard history if enabled. Remove the exposed key from any `SECRET_KEY_FALLBACKS`, restart every web or worker process, and verify that a fresh login works. Existing signed sessions and password-reset links can become invalid. On shared machines, prefer generating the value directly in the secret manager. [Django signing settings](https://docs.djangoproject.com/en/6.0/ref/settings/#secret-key)

## PostgreSQL role password

Schedule a brief restart window, then connect interactively as an administrator or the application role. Replace the angle-bracket fields with connection details. Use the provider's verified TLS connection parameters for remotely hosted databases.

```text
psql -X -W -h <db-host> -p <db-port> -U <admin-or-application-role> -d <db-name>
\password <application-role>
\q
```

Enter a password from your password manager at both prompts. Replace `DB_PASSWORD` in every private application instance, restart the app and any pooler or workers using the credential, and verify a new connection and a read-only Django operation. Review active sessions and coordinate termination of any unexpected connections. [PostgreSQL psql reference](https://www.postgresql.org/docs/current/app-psql.html)

## SMTP credential

For Gmail SMTP, sign in to the account that owns `EMAIL_HOST_USER`. Open Google Account App Passwords, create a dedicated replacement, update `EMAIL_HOST_PASSWORD` in the private deployment, and delete the old app password from the same page. If you suspect active misuse, revoke the old password immediately and expect a brief mail outage. For another SMTP provider, create or rotate the SMTP credential in that provider's console and update `EMAIL_HOST_USER` if it issues a new username. Restart the app and send one test message to a mailbox you control. [Google app password instructions](https://support.google.com/mail/answer/185833)

## SerpApi key

Sign in to SerpApi, open **Manage API Key**, and select **Regenerate API Key**. Set `SERPAPI_API_KEY` in the private Django deployment and in any standalone engine environment that used the old key. Restart the consumers, run one known Google Maps search, and check the usage dashboard. [SerpApi key dashboard](https://serpapi.com/manage-api-key) · [SerpApi rotation instructions](https://www.serpapi.com/blog/how-to-securely-store-api-keys/)

## Historical demo account

If the private database still contains an account provisioned by the old bootstrap command, reset it interactively with `python manage.py changepassword <demo-username>` or deactivate it via Django admin. Disable access to the old shared demo login before exposing the private deployment.
