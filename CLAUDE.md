# CLAUDE.md

Guidance for Claude Code (and anyone else) working in this repo.

## Project purpose

Practice project for learning Claude Code. It scaffolds a small Azure data
platform: Terraform infra (resource group, ADLS Gen2 storage, Key Vault) and
a Python CSV -> Parquet transformation step, with tests and CI.

## Hard rule: never run `terraform apply`

This repo is for learning Terraform structure and CI wiring, not for
provisioning real Azure resources. Only ever run `terraform init`,
`terraform fmt`, and `terraform validate` — locally and in CI. Do not run
`terraform apply`, `terraform destroy`, or `terraform plan` against a real
backend/subscription unless the user explicitly asks and sets that up
themselves.

There is no remote backend configured (`infra/versions.tf` has no `backend`
block) — state is local-only by design.

## Structure

- `infra/` — root Terraform config, calls `infra/modules/data_platform`.
- `infra/modules/data_platform/` — the reusable module: resource group,
  `azurerm_storage_account` (HNS-enabled for ADLS Gen2) + filesystem,
  `azurerm_key_vault` (RBAC authorization).
- `src/transform.py` — reads a CSV, cleans it (normalize column names, drop
  empty rows and exact duplicates), writes Parquet. Usable as a CLI
  (`python -m src.transform in.csv out.parquet`) or imported in tests.
- `tests/` — pytest tests for `src/`.
- `.github/workflows/ci.yml` — CI: terraform fmt/validate, pytest.

## Commands

```bash
# Terraform (fmt/init/validate only — never apply)
cd infra
terraform fmt -recursive
terraform init -backend=false
terraform validate

# Python
pip install -r requirements.txt
python -m pytest
python -m src.transform input.csv output.parquet
```

Always run tests as `python -m pytest`, not bare `pytest` — the test suite
imports `src` as a package, and a bare `pytest` invocation doesn't add the
repo root to `sys.path` the way `python -m` does, so `pytest` alone fails
with `ModuleNotFoundError: No module named 'src'` (this bit CI once; see
`.github/workflows/ci.yml`). The system Python on this machine is 3.9, which
installs pytest/pandas fine but doesn't reliably put the `pytest` entry point
on PATH — another reason to prefer `python3 -m pytest` locally.

## Conventions

- Terraform: one reusable module (`modules/data_platform`) consumed by the
  root config; resource naming via a `name_prefix` variable; all resources
  tagged via a shared `tags` variable.
- Python: plain functions over classes for the transform step; pandas for
  CSV/Parquet I/O; tests use `tmp_path` fixtures rather than committed
  fixture files.
- Keep infra and Python concerns independent — the Python script does not
  read Terraform outputs or talk to Azure; it operates on local files only.
