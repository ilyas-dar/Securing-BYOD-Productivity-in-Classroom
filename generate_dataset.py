""" This script generates my BYOD productivity dataset.
 I'm using it for my project "Securing BYOD Productivity in Classroom".
 Feel free to modify the apps, probabilities, or labeling logic."""


import numpy as np
import pandas as pd

# I’m keeping the dataset size flexible (you can change this to 1000–1500 if needed)
n_rows = 1200

# Just to make sure I get the same random values each time I run it
np.random.seed(42)

# =======**============**=========**===========
# 1. BASIC INFO (IDs, devices, and app choices)
# ========*===========**====================

# Random student IDs (not unique on purpose)
user_ids = np.random.randint(1, 201, size=n_rows)

# Device types with probabilities (more mobiles than laptops/tablets)
device_types = np.random.choice(
    ['mobile', 'laptop', 'tablet'],
    size=n_rows,
    p=[0.5, 0.35, 0.15]
)

# Apps I’m considering "productive"
productive_apps = [
    'Google Classroom', 'Notion', 'VSCode', 'Jupyter',
    'Google Docs', 'PDF Reader', 'LeetCode', 'Moodle',
    'Zoom', 'MS Teams'
]

# Apps that are usually distractions
non_productive_apps = [
    'Instagram', 'Snapchat', 'BGMI', 'Spotify',
    'YouTube', 'WhatsApp', 'Netflix', 'Chrome',
    'Facebook', 'Telegram'
]

apps = []
categories = []

# Deciding which app each row gets
for _ in range(n_rows):
    # Roughly 60% productive, 40% non-productive
    if np.random.rand() < 0.6:
        app = np.random.choice(productive_apps)
        apps.append(app)
        categories.append(np.random.choice(['education', 'coding', 'notes', 'lms']))
    else:
        app = np.random.choice(non_productive_apps)
        apps.append(app)
        categories.append(np.random.choice(['social_media', 'gaming', 'entertainment', 'browsing']))

# -------**-------------**------**------------------**----------------
# 2. USAGE PATTERNS (duration, subject, time slot, switching)
# --------*---------------**--------------**---------*--------------

# App usage time (using exponential so small durations are more common)
duration_min = np.round(np.random.exponential(scale=20, size=n_rows)).astype(int)
duration_min = np.clip(duration_min, 1, 90)

# Random subjects that might be happening during the usage
class_subjects = np.random.choice(
    ['DSA', 'Math', 'English', 'Physics', 'Chemistry', 'AI-ML', 'OS', 'DBMS'],
    size=n_rows
)

# Most classes happen earlier in the day, so weights are adjusted
time_slots = np.random.choice(
    ['morning', 'afternoon', 'evening'],
    size=n_rows,
    p=[0.5, 0.4, 0.1]
)

# Number of times user switched tabs (simulating distraction)
tab_switch_count = np.random.poisson(lam=8, size=n_rows)
tab_switch_count = np.clip(tab_switch_count, 0, 40)

# --------*-----------*-----------------------*------------------
# 3. LABELING (simple rules to decide productive or not)
# -------------------------------*-----------------------------

labels = []
for app, cat, dur, tabs in zip(apps, categories, duration_min, tab_switch_count):

    # Start by assuming the usage is productive
    label = 1

    # Most social media/gaming apps are distractions
    if cat in ['social_media', 'gaming', 'entertainment', 'browsing']:
        label = 0

    # Apps that are almost always distractions
    if app in ['Instagram', 'Snapchat', 'BGMI', 'Netflix', 'Facebook']:
        label = 0

    # Productive categories override the above
    if cat in ['education', 'coding', 'notes', 'lms']:
        label = 1

    # Some apps (YouTube, Chrome, etc.) can be both
    # If used for too long → probably distraction
    if app in ['YouTube', 'Chrome', 'Spotify', 'WhatsApp', 'Telegram'] and dur > 20:
        label = 0

    # Excessive tab switching usually means not focused
    if tabs > 25:
        label = 0

    labels.append(label)

# -================*=======================
# 4. BUILDING THE FINAL DATAFRAME
# ===========================*============

df = pd.DataFrame({
    'user_id' : user_ids,
    'device_type': device_types,
    'app_name': apps,
    'app_category' : categories,
    'duration_min': duration_min,
    'class_subject' : class_subjects,
    'time_slot': time_slots,
    'tab_switch_count': tab_switch_count,
    'is_productive' : labels
})

print("Dataset shape: ", df.shape)
print(df.head() )

# ------------------------------------------------------------
# 5. SAVE TO CSV
# ------------------------------------------------------------

file_name = "byod_productivity_dataset.csv"
df.to_csv(file_name, index=False)
print(f"Saved dataset as: {file_name}")

