# Public Readiness Gate

This repository is closer to public release after the current hardening pass, but the safe claim is:

**Ready for local-event use on a trusted event network after reviewed scripts are committed. Not yet ready to market as a general internet-hosted judging system until judge PIN storage/reset policy is hardened.**

## Verified Controls

- Django settings now distinguish local event mode from production-style deployment.
- Non-local mode requires `DJANGO_SECRET_KEY` and fails closed without it.
- Production-style defaults disable debug, remove wildcard hosts, enable secure cookies, enable SSL redirect, and set HSTS.
- Local Windows launcher explicitly sets `MUSTANGROUNDUP_LOCAL_EVENT_MODE=1` and `DJANGO_DEBUG=1`.
- Judge PIN login is throttled after repeated failed attempts.
- Judge logout requires POST with CSRF protection.
- Judge PINs are no longer shown in the operator dashboard or admin list/search.
- Generated `secret_key.txt` is ignored and was removed from the working tree.
- `db.sqlite3`, `build/`, and `dist/` are not tracked by Git.
- `scripts/*.ps1` are now visible to Git instead of being hidden by a broad ignore rule.

## Verification Commands

```text
.venv/Scripts/python.exe manage.py test
```

Result: 5 tests passed.

```text
cmd.exe /C "set DJANGO_SECRET_KEY=public-check-only-public-check-only-public-check-only-12345&& set DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=1&& set DJANGO_SECURE_HSTS_PRELOAD=1&& .venv\Scripts\python.exe manage.py check --deploy"
```

Result: no issues.

## Release Blockers

- Decide whether judge PINs are local disposable event codes or internet-facing credentials.
- If internet-facing judging is supported, replace plaintext PIN storage with hashed PINs plus reset/regenerate workflows.
- Commit or remove the currently untracked PowerShell scripts before release.
- Review tracked collected static assets and decide whether they are intentional source artifacts or should be generated during packaging.
- Build the installer from a clean tree and publish only the reviewed installer artifact.

## Local Event Release Criteria

- `scripts/setup-windows.ps1`, `scripts/start-server.ps1`, and `scripts/start-dev-server.ps1` are reviewed and intentionally tracked.
- A clean install creates a fresh database under the operator data directory.
- No real event database, generated secret, local backup, or packaged binary is committed.
- README states that the local `runserver` workflow is for trusted event networks, not direct internet exposure.
- Fresh judge PINs are generated for every event and are not reused.

## Internet Release Criteria

- `MUSTANGROUNDUP_LOCAL_EVENT_MODE=0`
- `DJANGO_DEBUG=0`
- `DJANGO_SECRET_KEY` is set to a long random value.
- `DJANGO_ALLOWED_HOSTS` is explicit.
- `DJANGO_CSRF_TRUSTED_ORIGINS` matches the HTTPS origin.
- `manage.py check --deploy` passes in the target environment.
- Judge PINs are hashed or replaced with stronger authentication.
- HTTPS, backups, logging, and dependency update process are documented.
