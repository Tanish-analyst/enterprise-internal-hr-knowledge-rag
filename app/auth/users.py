import os
import pandas as pd
from typing import Dict, Any

USERS_XLSX = "data/users.xlsx"
users_db: Dict[str, Dict[str, Any]] = {}

if os.path.exists(USERS_XLSX):
    try:
        df = pd.read_excel(USERS_XLSX)
        df.columns = [c.strip() for c in df.columns]

        for _, row in df.iterrows():
            email = str(row["email"]).strip()
            users_db[email] = {
                "user_id": row.get("user_id"),
                "email": email,
                "hashed_password": row.get("password_hash"),
                "role": str(row.get("role")).strip(),
                "status": str(row.get("status")).strip().lower()
            }
    except Exception as e:
        print("Could not load users.xlsx:", e)
else:
    print("Warning: users.xlsx not found")
