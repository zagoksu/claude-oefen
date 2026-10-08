# claude-oefen

A small practice project combining a Terraform-defined Azure data platform
with a Python data transformation step. Built to learn Claude Code, not to
be deployed — see [CLAUDE.md](CLAUDE.md) for conventions and commands.

## Structure

```
infra/        Terraform (azurerm provider): resource group, ADLS Gen2 storage
              account, Key Vault. Local state only, no backend configured.
src/          Python data transformation: read CSV -> clean -> write Parquet.
tests/        pytest tests for src/.
.github/      CI workflow: terraform fmt/validate + pytest.
```

## Infrastructure (infra/)

Defines, via a reusable module (`infra/modules/data_platform`):

- an `azurerm_resource_group`
- an `azurerm_storage_account` with `is_hns_enabled = true` (ADLS Gen2) and a
  `raw` filesystem/container
- an `azurerm_key_vault` using RBAC authorization

**This project never runs `terraform apply`.** Only `init`, `fmt`, and
`validate` are used, locally and in CI, so nothing here provisions real Azure
resources.

```bash
cd infra
terraform fmt -recursive
terraform init -backend=false
terraform validate
```

## Data transformation (src/)

`src/transform.py` reads a CSV file, normalizes column names, drops empty
rows and exact duplicates, and writes the result to Parquet.

```bash
pip install -r requirements.txt
python -m src.transform input.csv output.parquet
```

## Tests

```bash
pip install -r requirements.txt
pytest
```

## CI

`.github/workflows/ci.yml` runs on every push/PR:
- `terraform fmt -check` and `terraform validate` (no backend, no apply)
- `pytest`
