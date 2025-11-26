""" This script generates my BYOD productivity dataset.
 I'm using it for my project "Securing BYOD Productivity in Classroom".
 Feel free to modify the apps, probabilities, or labeling logic. keep in mind the dataset generated 
 is totally mimicking the real world """


"""
Realistic-ish BYOD dataset generator for:
"Securing BYOD Productivity in Classroom"

This version tries to feel more like the real world:
- Students have different behaviour types (focused / average / easily distracted)
- Some social media usage can still be marked productive (e.g., class group)
- Some "good" apps can still be unproductive (open but not paying attention)
- Time of day, subject, duration, tab switches all influence the label
- There's random noise, so it's not perfectly predictable

Result: the data has patterns, but it's not "clean math".
"""

import numpy as np
import pandas as pd

# how many rows you want
n_rows = 1200
np.random.seed(42)

# ------------------------------------------------
# 1. Student-level behaviour (latent, not in CSV)
# ------------------------------------------------

n_students = 200
student_ids = np.arange(1, n_students + 1)

# assign each student a "behaviour profile"
profiles = np.random.choice(
    ["focused", "average", "distracted"],
    size=n_students,
    p=[0.3, 0.5, 0.2]  # most are average, fewer extreme types
)

# map user_id -> profile
student_profile_map = {sid: prof for sid, prof in zip(student_ids, profiles)}

# ------------------------------------------------
# 2. Sampling basic columns
# ------------------------------------------------

# draw random student for each row
user_ids = np.random.choice(student_ids, size=n_rows)

device_types = np.random.choice(
    ["mobile", "laptop", "tablet"],
    size=n_rows,
    p=[0.55, 0.35, 0.10]
)

productive_apps = [
    "Google Classroom", "Notion", "VSCode", "Jupyter",
    "Google Docs", "PDF Reader", "LeetCode", "Moodle",
    "Zoom", "MS Teams"
]

non_productive_apps = [
    "Instagram", "Snapchat", "BGMI", "Spotify",
    "YouTube", "WhatsApp", "Netflix", "Chrome",
    "Facebook", "Telegram"
]

apps = []
categories = []

for dev in device_types:
    # on laptop, more likely to be "work" apps, on mobile more mixed
    if np.random.rand() < (0.65 if dev == "laptop" else 0.45):
        app = np.random.choice(productive_apps)
        apps.append(app)
        categories.append(np.random.choice(["education", "coding", "notes", "lms"]))
    else:
        app = np.random.choice(non_productive_apps)
        apps.append(app)
        categories.append(np.random.choice(["social_media", "gaming", "entertainment", "browsing"]))

# duration of use (long tail, more short sessions than long ones)
duration_min = np.round(np.random.exponential(scale=18, size=n_rows)).astype(int)
duration_min = np.clip(duration_min, 1, 120)

class_subjects = np.random.choice(
    ["DSA", "Math", "English", "Physics", "Chemistry", "AI-ML", "OS", "DBMS"],
    size=n_rows
)

time_slots = np.random.choice(
    ["morning", "afternoon", "evening"],
    size=n_rows,
    p=[0.5, 0.35, 0.15]
)

tab_switch_count = np.random.poisson(lam=8, size=n_rows)
tab_switch_count = np.clip(tab_switch_count, 0, 50)

# ------------------------------------------------
# 3. Build a "productivity score" from many factors
#    (instead of hard if-else = label)
# ------------------------------------------------

labels = []

for uid, dev, app, cat, dur, subj, slot, tabs in zip(
    user_ids, device_types, apps, categories,
    duration_min, class_subjects, time_slots, tab_switch_count
):
    profile = student_profile_map[uid]

    # start from profile baseline
    if profile == "focused":
        score = 0.7
    elif profile == "average":
        score = 0.5
    else:  # distracted
        score = 0.3

    # subject effect: some subjects require more attention
    if subj in ["DSA", "AI-ML", "OS", "DBMS"]:
        score += 0.05  # typically more demanding
    else:
        score += 0.0

    # time of day: evenings tend to be a bit less productive
    if slot == "morning":
        score += 0.05
    elif slot == "evening":
        score -= 0.05

    # device: laptops often used more seriously, mobiles more mixed
    if dev == "laptop":
        score += 0.05
    elif dev == "mobile":
        score -= 0.02

    # app category: but not strictly yes/no
    if cat in ["education", "coding", "notes", "lms"]:
        score += 0.15
    if cat in ["social_media", "gaming", "entertainment", "browsing"]:
        score -= 0.15

    # specific apps adjustments (still soft, not hard rules)
    if app in ["Instagram", "Snapchat", "BGMI", "Netflix", "Facebook"]:
        score -= 0.15
    if app in ["Google Classroom", "Moodle", "Zoom", "MS Teams"]:
        score += 0.10

    # duration effect: extremely long sessions often drift off-task
    if dur > 60:
        score -= 0.1
    elif 5 <= dur <= 30:
        score += 0.05  # likely focused burst

    # tab switching: high switching → less focus
    if tabs > 25:
        score -= 0.15
    elif tabs < 4:
        score += 0.05

    # tiny random noise, so it’s never perfectly clean
    noise = np.random.normal(0, 0.08)
    score += noise

    # keep score in [0,1]
    score = max(0.0, min(1.0, score))

    # final label: threshold around 0.5
    label = 1 if score >= 0.5 else 0
    labels.append(label)

# ------------------------------------------------
# 4. Final DataFrame
# ------------------------------------------------

df = pd.DataFrame({
    "user_id": user_ids,
    "device_type": device_types,
    "app_name": apps,
    "app_category": categories,
    "duration_min": duration_min,
    "class_subject": class_subjects,
    "time_slot": time_slots,
    "tab_switch_count": tab_switch_count,
    "is_productive": labels
})

print("Dataset shape:", df.shape)
print(df.head())

# ------------------------------------------------
# 5. Save the dataset
# ------------------------------------------------

file_name = "byod_productivity_dataset.csv"
df.to_csv(file_name, index=False)



