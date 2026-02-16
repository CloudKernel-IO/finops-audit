# Cloud Management & FinOps Engine 🛡️💰

**Identify and eliminate cloud waste across Azure, AWS, and GCP in seconds.**

This engine is a security-first, read-only auditing tool designed for infrastructure teams to detect orphaned assets and unattached resources that drive up cloud bills.

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.9+**
- **Cloud CLI tools** configured locally (Azure CLI, AWS CLI, or gcloud) OR **Service Principal/IAM Role** credentials.

### 2. Installation
First, install [Poetry](https://python-poetry.org/docs/#installation). Then:

```bash
git clone https://github.com/[TU_ORGANIZACION]/finops-audit.git
cd finops-audit
poetry install
```

### 3. Execution
To run a full audit across all configured providers:
```bash
poetry run python main.py --all
```

## 🔐 Security & Permissions (Zero-Write Policy)
The engine follows the Principle of Least Privilege. It only requires read-only access. No write or delete permissions are needed.

| Provider | Required Role / Permission |
| --- | --- |
| Azure | Reader |
| AWS | ReadOnlyAccess |
| GCP | Viewer |

Note: We recommend using Managed Identities or OIDC for GitHub Actions to avoid handling long-lived secrets.

## 📊 Audited Resources
Currently, the engine detects the following "Ghost Resources":

- Compute: Unattached Managed Disks (Azure), Available EBS Volumes (AWS), Unused Zonal Disks (GCP).
- Networking: Reserved but unassociated Public IPs (Standard/Static/Elastic).
- Batch: Idle nodes and abandoned pools.

## 🤖 Automated Audits with GitHub Actions
You can automate this audit to run every Monday at 9:00 AM using the provided workflow:

1. Go to Settings > Secrets > Actions in this repo.
2. Add your Cloud Credentials.
3. Enable the .github/workflows/daily_audit.yml.

## 🧪 Testing & Coverage
Run unit tests with coverage:
```bash
poetry install
poetry run pytest -m "not integration" --cov=. --cov-report=term-missing --cov-report=xml
```

Integration tests are optional and require cloud credentials. Enable them with:
```bash
RUN_AWS_INTEGRATION=true RUN_AZURE_INTEGRATION=true RUN_GCP_INTEGRATION=true poetry run pytest -m integration
```

## 📬 Contact
For questions or access to the Pro version, reach out at bernabepuente@cloudkernel.app.

## 📄 License
Distributed under the MIT License. See LICENSE for more information.

## Looking for Automated Remediation?
The Pro version of this engine can automatically delete detected waste based on custom policies. Contact us for more info.