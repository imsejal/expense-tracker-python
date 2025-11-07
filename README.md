# Expense Tracker (L7 Informatics Internship)

## Features

- Log daily expenses (category, amount, user)
- Category-level monthly budgets (YYYY-MM)
- Alerts when budget is exceeded or low (10% left)
- Split expenses among groups (records per member)
- CLI-based demo interface
- Docker-ready

## Requirements

- Python 3.10+
- pip

## Setup (local)

1. Clone repo
2. Create virtualenv:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   ```

3. (Optional) set email credentials:

export SENDER_EMAIL="you@gmail.com"
export SENDER_PASSWORD="app-password"

4. Run:

```bash
python main.py
```

Run with Docker

1. Build:

```bash
docker build -t expense-tracker .
```

2. Run (pass env vars if email alerts needed):

```bash
docker run -it --env SENDER_EMAIL=you@gmail.com --env SENDER_PASSWORD=app-password
```
