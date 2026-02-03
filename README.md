# GitHub Profile Automation (This → Profile)

This project automates updates to the public profile repository **[AnujYadav-Dev/AnujYadav-Dev](https://github.com/AnujYadav-Dev/AnujYadav-Dev)** 
using scripts stored in **this repository**.  

The automation is handled using **GitHub Actions**, which runs daily and on manual dispatch.

---

## 📌 How It Works
1. Workflow runs inside this **repo** (contains `today.py` and dependencies).
2. It installs required Python packages from `cache/requirements.txt`.
3. Clones the **public repo** (`AnujYadav-Dev/AnujYadav-Dev`).
4. Runs `today.py` from the this repo, which updates the README and SVG files.
5. Commits and pushes changes back to the **public repo**.

---

## 🔑 Secrets Required
Add these in the **private repo’s** GitHub → Settings → Secrets and variables → Actions:

- `ACCESS_TOKEN` → A fine-grained Personal Access Token with `repo` permissions.
- `USER_NAME` → Your GitHub username (e.g., `AnujYadav-Dev`).

---

## 🗂️ Repository Structure
```
Profile_README_Brain/
│── .github/
│   └── workflows/
│       └── readme.yml   # workflow file
│── cache/
│   └── requirements.txt
│── README.md
│── today.py


```

---

## 🚀 Usage
- Runs According to **Corn Job** automatically.
- Can also be triggered manually via **Actions → README build → Run workflow**.
- Updates the README and SVGs in the **public repo**.

---

## 🙏 Credits

Based on [Andrew6rant/Andrew6rant](https://github.com/Andrew6rant/Andrew6rant) by [Andrew6rant](https://github.com/Andrew6rant).

---

## 📄 License

MIT License - Feel free to customize and share!
