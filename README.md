# GitHub Profile Automation (This → Profile)

This project automates updates to your public profile repository **[`AnujYadav-Dev`/`AnujYadav-Dev`](https://github.com/AnujYadav-Dev/AnujYadav-Dev)** 
using scripts stored in **this repository**.  

The automation is handled using **GitHub Actions**, which runs daily and on manual dispatch.

---

## 📌 How It Works
1. Workflow runs inside this **repo** (contains `today.py` and dependencies).
2. It installs required Python packages from `cache/requirements.txt`.
3. Clones the **public repo** using your username (`AnujYadav-Dev/AnujYadav-Dev`).
4. Runs `today.py` from this repo, which updates the README and SVG files dynamically.
5. Commits and pushes changes back to the **public repo**.

---

## 🔑 Secrets Required

To make this automation work, you need to add the following secrets to the **this repository** (the one containing `today.py`):

1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Secrets and variables** > **Actions**.
3. Click on **New repository secret** for each of the following:

- `ACCESS_TOKEN` → A fine-grained [Personal Access Token](https://github.com/settings/tokens?type=beta) with the following permissions:
    - **Account permissions**: `read:Followers`, `read:Starring`, `read:Watching`
    - **Repository permissions**: `read:Commit statuses`, `read:Contents`, `read:Issues`, `read:Metadata`, `read:Pull Requests` (Select "All repositories")
- `USER_NAME` → Your GitHub username (e.g., `AnujYadav-Dev`).
- `BIRTH_DATE` → *(Optional)* Your birthdate in `YYYY-MM-DD` format (e.g., `2006-12-08`). If not provided, the profile will show "Age: Not specified".

---

## 🗂️ Repository Structure
```
Profile_README_Brain/
│── .github/
│   └── workflows/
│       └── build.yaml   # workflow file
│── cache/
│   └── requirements.txt
│── README.md
│── today.py


```

---

## 🚀 Usage
- Runs according to **Cron Job** automatically.
- Can also be triggered manually via **Actions → README build → Run workflow**.
- Updates the README and SVGs in the **public repo**.

---

## 🙏 Credits

Based on [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant) by [Andrew6rant](https://github.com/Andrew6rant).

---

## 📄 License

MIT License - Feel free to customize and share!
