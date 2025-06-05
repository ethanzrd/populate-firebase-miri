import json, random, secrets, datetime, os, textwrap

# Hebrew data for names and notes
first_names = [
    "דוד", "יונתן", "נועם", "מאיה", "שירה", "תמר", "איתי", "ליה", "עדן", "אביב",
    "טל", "רון", "נועה", "אור", "יעל", "אורי", "גיא", "דניאל", "עמית", "סהר",
    "קרן", "הדר", "ליאור", "מיכל", "אלון"
]

last_names = [
    "לוי", "כהן", "ישראלי", "דוד", "שטרן", "בר", "קפלן", "אוחנה", "שרון", "ששון",
    "רובין", "פרידמן", "זוהר", "הראל", "חיים", "גדות", "בן דוד", "ברק", "רובינשטיין", "מרגולין"
]

expense_categories = ["מזון", "תחבורה", "בילויים", "קניות", "אחר"]
income_categories = ["עבודה", "מתנה", "אחר"]

note_options = [
    "", "קנייה בסופר", "נסיעה באוטובוס", "קבלת מתנה", "ארוחה במסעדה",
    "שכר עבודה", "מסיבה עם חברים", "דלק לרכב", "תשלום שכירות", "קניית ביגוד",
    "ביקור בקולנוע", "חופשה קצרה", "תשלום חשמל", "תשלום מים", "קניית מתנה"
]

def random_push_id():
    allowed = "-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return "-" + "".join(random.choice(allowed) for _ in range(20))

def random_uid():
    return secrets.token_urlsafe(20)[:28]

def random_date_in_month(year: int, month: int):
    # pick a random day valid for the month
    if month == 2:
        max_day = 29  # 2025 is not a leap year but Feb has 28; allow 28
        max_day = 28
    elif month in [4, 6, 9, 11]:
        max_day = 30
    else:
        max_day = 31
    day = random.randint(1, max_day)
    return datetime.date(year, month, day).isoformat()

data = {"categories": {}, "entries": {}, "users": {}}

NUM_USERS = 50
MONTHS = range(1, 7)  # January to June

for i in range(NUM_USERS):
    uid = random_uid()
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    email = f"user{i+1}@example.com"

    # Users node
    data["users"][uid] = {
        "email": email,
        "isAdmin": False,
        "name": name
    }

    # Categories node
    data["categories"][uid] = {
        "expense": expense_categories,
        "income": income_categories
    }

    # Entries node
    user_entries = {}
    for month in MONTHS:
        num_entries = random.randint(20, 35)  # ensure at least 20
        for _ in range(num_entries):
            entry_id = random_push_id()
            entry_type = random.choice(["income", "expense"])
            category = random.choice(income_categories if entry_type == "income" else expense_categories)
            amount = random.randint(500, 10000) if entry_type == "income" else random.randint(20, 3000)
            user_entries[entry_id] = {
                "amount": amount,
                "category": category,
                "date": random_date_in_month(2025, month),
                "note": random.choice(note_options),
                "type": entry_type
            }
    data["entries"][uid] = user_entries

# Save to file
output_path = "/mnt/data/firebase_mock_50_users_large.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
