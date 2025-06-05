import json
import firebase_admin
from firebase_admin import credentials, auth

# ===== 1) אתחול Firebase Admin =====
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

# ===== 2) טען את קובץ ה-JSON שיצרנו קודם =====
with open("firebase_mock_50_users_large.json", "r", encoding="utf-8") as f:
    data = json.load(f)

PASSWORD = "someone"        # סיסמה אחידה (לפחות 6 תווים)

# ===== 3) צור או עדכן כל משתמש =====
for uid, user in data["users"].items():
    try:
        # אם המשתמש כבר קיים – רק עדכן סיסמה (לא חובה, אבל בטוח)
        auth.update_user(uid, password=PASSWORD,
                         display_name=user["name"], email=user["email"])
        print(f"Updated {uid}")
    except auth.UserNotFoundError:
        # אם אינו קיים – צור משתמש חדש עם UID קבוע
        auth.create_user(uid=uid,
                         email=user["email"],
                         password=PASSWORD,
                         display_name=user["name"])
        print(f"Created {uid}")

print("Finished!")
