# GitHub Profile Automation (Profile-Brain)

This repository is a **fully dynamic, reusable, and configurable GitHub Action template** that automates updates to any GitHub profile repository. It dynamically generates SVGs with your latest GitHub statistics (like age, commits, stars, repositories, and lines of code) and commits them to your profile README repository.

---

## 📌 How It Works
1. You **fork** this repository or use it as a template.
2. The GitHub Action runs inside this repository on a schedule or via manual dispatch.
3. It uses a Personal Access Token (PAT) to securely clone your **target repository** (e.g., your profile README).
4. The `today.py` script runs, fetching your data via the GitHub GraphQL API and updating your SVGs.
5. Finally, it commits and pushes the updated SVGs directly back to your target repository.

---

## ⚙️ Configuration (Secrets & Variables)

This project uses **GitHub Actions Secrets and Variables** to remain fully dynamic. You don't need to change any code! Just configure your repository settings.

Navigate to your repository's **Settings > Secrets and variables > Actions**.

### 💡 Example Configuration
To make this concrete, here is what your setup might look like if your username is `AnujYadav-Dev` and you want to save the SVGs in a folder called `assets` inside your profile repository:

**Secrets** (Hidden values):
- `ACCESS_TOKEN` = `github_pat_11A...`

**Variables** (Visible settings):
- `USER_NAME` = `AnujYadav-Dev`
- `BIRTH_DATE` = `2000-01-01`
- `TARGET_REPO` = `AnujYadav-Dev/AnujYadav-Dev` *(Targets the profile repository)*
- `DARK_SVG_PATH` = `assets/github-metrics-dark.svg`
- `LIGHT_SVG_PATH` = `assets/github-metrics-light.svg`
- `CACHE_DIR` = `cache`
- `COMMIT_AUTHOR_NAME` = `github-actions[bot]`
- `COMMIT_AUTHOR_EMAIL` = `41898282+github-actions[bot]@users.noreply.github.com`

---

### 🔐 Repository Secrets
These are sensitive values that should remain hidden. Add these under the **Secrets** tab:

| Secret Name | Required | Description |
|---|---|---|
| `ACCESS_TOKEN` | Yes | A fine-grained [Personal Access Token](https://github.com/settings/tokens?type=beta) with the following permissions:<br>- **Account permissions**: `read:Followers`, `read:Starring`, `read:Watching`<br>- **Repository permissions**: `read:Commit statuses`, `read:Contents`, `read:Issues`, `read:Metadata`, `read:Pull Requests` (Select "All repositories") |

### 🛠️ Repository Variables
These are configuration options that can be visible. Add these under the **Variables** tab. If not provided, the action will gracefully fallback to standard defaults.

| Variable Name | Default Fallback | Description |
|---|---|---|
| `USER_NAME` | `${github.repository_owner}` | Your GitHub username. Used to query the API and generate the dynamic author string. Defaults to the owner of the repository. |
| `BIRTH_DATE` | *(None)* | Your birthdate in `YYYY-MM-DD` format (e.g., `2006-12-08`). Used to calculate the exact time since you were born. |
| `TARGET_REPO` | `${github.repository_owner}/${github.repository_owner}` | The repository where the SVGs will be committed. Defaults to your GitHub Profile repository. |
| `DARK_SVG_PATH` | `dark_mode.svg` | The path to the dark mode SVG inside the target repo. |
| `LIGHT_SVG_PATH` | `light_mode.svg` | The path to the light mode SVG inside the target repo. |
| `CACHE_DIR` | `cache` | Directory path where the repository cache/archive is stored. |
| `COMMIT_AUTHOR_NAME` | `github-actions[bot]` | Name used when committing the updated files. |
| `COMMIT_AUTHOR_EMAIL` | `41898282+github-actions[bot]@users.noreply.github.com` | Email used when committing the updated files. |

---

## 🗂️ Repository Structure
```
Profile-Brain/
│── .github/
│   └── workflows/
│       └── build.yaml   # GitHub Action Workflow
│── cache/
│   └── requirements.txt # Python dependencies
│── README.md            # This file
│── today.py             # Core automation script
```

---

## 🚀 Usage
1. Fork this repository.
2. Go to the **Actions** tab and enable workflows if prompted.
3. Configure your Secrets and Variables in the repository settings.
4. Run the workflow manually via **Actions → README build → Run workflow**.
5. After verifying it works, the **Cron Job** will run automatically according to the schedule in `build.yaml`.

---

## 🙏 Credits
Based on the original [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant) by [Andrew6rant](https://github.com/Andrew6rant).

---

## 📄 License
MIT License - Feel free to customize, share, and fork!
