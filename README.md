This repo is for my project “Securing BYOD Productivity in Classroom”.
I wanted to understand how students use their devices during class (especially in BYOD setups), so I created my own dataset and started building a small ML model around it.

The dataset has around 1200 rows, and each row is basically one “usage event” — like what app was being used, for how long, etc.
What the dataset contains

#Some of the columns I used:

#user_id – just a simulated ID

#device_type – mobile / laptop / tablet

#app_name – the app being used

#app_category – education, coding, notes, LMS, social media, gaming, etc.

#duration_min – how long the app was used

#class_subject – subject going on during that time

#time_slot – morning / afternoon / evening

#tab_switch_count – how often the student switched tabs

#is_productive – 1 = productive, 0 = not
