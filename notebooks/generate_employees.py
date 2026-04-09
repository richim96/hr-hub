import pandas as pd
import numpy as np
import uuid
import random

random.seed(96)
np.random.seed(96)

# ── Config ────────────────────────────────────────────────────────────────────
N          = 14_999
N_MANAGERS = 630

# ── Name pools ────────────────────────────────────────────────────────────────
MALE_FIRST = [
    "James","John","Robert","Michael","William","David","Richard","Joseph","Thomas","Charles",
    "Christopher","Daniel","Matthew","Anthony","Mark","Donald","Steven","Paul","Andrew","Joshua",
    "Kenneth","Kevin","Brian","George","Timothy","Ronald","Edward","Jason","Jeffrey","Ryan",
    "Jacob","Gary","Nicholas","Eric","Jonathan","Stephen","Larry","Justin","Scott","Brandon",
    "Benjamin","Samuel","Raymond","Gregory","Frank","Alexander","Patrick","Jack","Dennis","Jerry",
    "Tyler","Aaron","Jose","Henry","Adam","Douglas","Nathan","Peter","Zachary","Kyle","Noah",
    "Alan","Carlos","Louis","Juan","Arthur","Wayne","Roy","Eugene","Dylan","Austin","Mason",
    "Lawrence","Jesse","Bryan","Joe","Billy","Jordan","Albert","Vincent","Willie","Logan","Harold",
    "Christian","Ethan","Terry","Sean","Gerald","Carl","Keith","Roger","Jeremy","Walter","Bobby",
    "Philip","Bruce","Leonard","Sebastian","Oscar","Marcus","Victor","Elijah","Owen","Luke",
]

FEMALE_FIRST = [
    "Mary","Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah","Karen",
    "Lisa","Nancy","Betty","Margaret","Sandra","Ashley","Dorothy","Kimberly","Emily","Donna",
    "Michelle","Carol","Amanda","Melissa","Deborah","Stephanie","Rebecca","Sharon","Laura","Cynthia",
    "Kathleen","Amy","Angela","Shirley","Anna","Brenda","Pamela","Emma","Nicole","Helen","Samantha",
    "Katherine","Christine","Debra","Rachel","Carolyn","Janet","Catherine","Maria","Heather","Diane",
    "Julie","Joyce","Victoria","Ruth","Virginia","Lauren","Kelly","Christina","Joan","Evelyn",
    "Olivia","Judith","Megan","Cheryl","Andrea","Hannah","Martha","Jacqueline","Frances","Gloria",
    "Teresa","Kathryn","Sara","Janice","Jean","Alice","Madison","Doris","Abigail","Julia",
    "Judy","Grace","Denise","Amber","Marilyn","Beverly","Danielle","Theresa","Sophia","Marie",
    "Diana","Brittany","Natalie","Isabella","Charlotte","Rose","Alexis","Kayla","Zoe","Lily",
]

LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
    "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
    "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
    "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
    "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts",
    "Turner","Phillips","Evans","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart",
    "Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson",
    "Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson",
    "Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price",
    "Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez","Powell",
    "Jenkins","Perry","Russell","Sullivan","Bell","Coleman","Butler","Henderson","Barnes","Gonzales",
    "Fisher","Vasquez","Simmons","Romero","Jordan","Patterson","Alexander","Hamilton","Graham","Reynolds",
]

LAPTOPS = [
    'MacBook Pro 14"', 'MacBook Pro 16"', "MacBook Air M2",
    "Dell XPS 15", "Dell Latitude 7440", "ThinkPad X1 Carbon",
    "ThinkPad T14s", "HP EliteBook 840", "Surface Laptop 5",
]

# ── Department exact headcounts (must sum to N = 14 999) ─────────────────────
DEPT_COUNTS = {
    "sales":              4140,
    "engineering":        2720,
    "support":            2229,
    "IT":                 1227,
    "product_management":  902,
    "marketing":           858,
    "r&d":                 787,
    "accounting":          767,
    "hr":                  739,
    # management is handled separately → always exactly N_MANAGERS (630)
}

# ── Gender assignment (60 % M / 40 % F) ──────────────────────────────────────
n_male   = round(N * 0.60)
n_female = N - n_male
genders  = np.array(["M"] * n_male + ["F"] * n_female)
np.random.shuffle(genders)

# ── Draw first names based on gender ─────────────────────────────────────────
first_names = np.where(
    genders == "M",
    np.random.choice(MALE_FIRST,   N),
    np.random.choice(FEMALE_FIRST, N),
)
last_names = np.random.choice(LAST_NAMES, N)

# ── Unique emails ─────────────────────────────────────────────────────────────
def build_email(first: str, last: str, suffix: str = "") -> str:
    return f"{first.lower()}.{last.lower()}{suffix}@company.com"

emails: list = []
seen:   set  = set()

for first, last in zip(first_names, last_names):
    email = build_email(first, last)
    if email in seen:
        counter = 2
        while build_email(first, last, str(counter)) in seen:
            counter += 1
        email = build_email(first, last, str(counter))
    seen.add(email)
    emails.append(email)

# ── CEO (row 0): firstname.lastname.ceo@company.com ──────────────────────────
ceo_email = f"{first_names[0].lower()}.{last_names[0].lower()}.ceo@company.com"
seen.discard(emails[0])
emails[0] = ceo_email
seen.add(ceo_email)

# ── Manager pool: rows 0 … N_MANAGERS-1 (all in "management") ────────────────
mgr_indices        = list(range(N_MANAGERS))
mgr_emails         = [emails[i] for i in mgr_indices]
non_ceo_mgr_emails = mgr_emails[1:]   # who the rest of the company reports to

# ── Departments ───────────────────────────────────────────────────────────────
departments = ["management"] * N_MANAGERS   # first N_MANAGERS rows

non_mgr_depts = np.repeat(list(DEPT_COUNTS.keys()), list(DEPT_COUNTS.values()))
np.random.shuffle(non_mgr_depts)
departments.extend(non_mgr_depts.tolist())

# ── Manager emails ────────────────────────────────────────────────────────────
mgr_set = set(mgr_indices)
manager_emails = []

for i in range(N):
    if i == 0:              # CEO → None
        manager_emails.append(None)
    elif i in mgr_set:      # every other manager → CEO
        manager_emails.append(ceo_email)
    else:                   # everyone else → random manager (excluding CEO)
        manager_emails.append(random.choice(non_ceo_mgr_emails))

# ── Hardware ──────────────────────────────────────────────────────────────────
laptops  = np.random.choice(LAPTOPS, N)
monitors = np.random.choice([True, False], N, p=[0.75, 0.25])
headsets = np.random.choice([True, False], N, p=[0.60, 0.40])

# ── Assemble DataFrame ────────────────────────────────────────────────────────
df = pd.DataFrame({
    "EmployeeID": [str(uuid.uuid4()) for _ in range(N)],
    "FirstName": first_names,
    "LastName": last_names,
    "Gender": genders,
    "Email": emails,
    "Department": departments,
    "ManagerEmail": manager_emails,
    "Laptop": laptops,
    "Monitor": monitors,
    "Headset": headsets,
})

# ── Validation ────────────────────────────────────────────────────────────────
print("=" * 55)
print(f"  Total rows          : {len(df):,}")
print(f"  Unique emails       : {df['Email'].nunique():,}")
print(f"  CEO email           : {df.loc[0, 'Email']}")
print(f"  CEO manager_email   : {df.loc[0, 'ManagerEmail']}")
print()
print("  Gender distribution:")
print(df["Gender"].value_counts(normalize=True).round(4).to_string())
print()
print("  Department count:")
print(df["Department"].value_counts().to_string())
mgr_df = df[df["Department"] == "management"]
print()
print(f"  All managers → CEO  : {(mgr_df['ManagerEmail'].dropna() == ceo_email).all()}")
print("=" * 55)

# ── Export ────────────────────────────────────────────────────────────────────
df.to_csv("../mock-cloud/storage/data/processed/employees.csv", index=False)
print("Created employees.csv  ✅")
