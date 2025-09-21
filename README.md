# GitHub Profile Automation (Private → Public)

This project automates updates to the public profile repository **[AnujYadav-Dev/AnujYadav-Dev](https://github.com/AnujYadav-Dev/AnujYadav-Dev)** 
using scripts stored in a **private repository**.  

The automation is handled using **GitHub Actions**, which runs daily and on manual dispatch.

---

## 📌 How It Works
1. Workflow runs inside the **private repo** (contains `today.py` and dependencies).
2. It installs required Python packages from `cache/requirements.txt`.
3. Clones the **public repo** (`AnujYadav-Dev/AnujYadav-Dev`).
4. Runs `today.py` from the private repo, which updates the README and SVG files.
5. Commits and pushes changes back to the **public repo**.

---

## 🔑 Secrets Required
Add these in the **private repo’s** GitHub → Settings → Secrets and variables → Actions:

- `ACCESS_TOKEN` → A fine-grained Personal Access Token with `repo` permissions.
- `USER_NAME` → Your GitHub username (e.g., `AnujYadav-Dev`).

---

## 🗂️ Repository Structure
```
private-repo/
│── today.py
│── cache/
│   └── requirements.txt
│── .github/
│   └── workflows/
│       └── readme.yml   # workflow file
```

---

## 🚀 Usage
- Runs **every day at 04:00 UTC** automatically.
- Can also be triggered manually via **Actions → README build → Run workflow**.
- Updates the README and SVGs in the **public repo**.

---

## 👨‍💻 Author
**Anuj Kumar Yadav (AnujYadav-Dev)**  
Maintains both private + public repositories for GitHub profile automation.
