# schedule_data.py

# Representative Daily Schedule for real-time activity tracking.
DAILY_SCHEDULE = {
    "weekday": [
        {"start": "00:00", "end": "06:00", "activity": "Sleep",
         "description": "Essential rest period, focus on deep sleep for recovery."},
        {"start": "06:00", "end": "07:00", "activity": "Personal Care",
         "description": "Morning routine including hygiene, dressing, and quick personal prep."},
        {"start": "07:00", "end": "08:30", "activity": "Kid Morning Prep/Drop-off",
         "description": "Prepare breakfast, get kids ready, pack lunches, drive to school."},
        {"start": "08:30", "end": "12:00", "activity": "Study & Coursework",
         "description": "Focused academic work, lectures, readings, and assignments. Minimize distractions."},
        {"start": "12:00", "end": "13:00", "activity": "Personal Care (Lunch/Chore)",
         "description": "Lunch break, short rest, or quick house tidying. Recharge for the afternoon."},
        {"start": "13:00", "end": "15:25", "activity": "Study & Coursework",
         "description": "Continued academic work and project development. Maintain focus."},
        {"start": "15:25", "end": "15:45", "activity": "Kid Pick-up",
         "description": "Drive to school/daycare. Must leave on time."},
        {"start": "15:45", "end": "20:00", "activity": "Afternoon Coordination",
         "description": "Manage homework, after-school activities, play time, and prepare for dinner."},
        {"start": "20:00", "end": "21:00", "activity": "Kid Bedtime/Quick Tidy",
         "description": "Evening routine for kids, including story time and light cleanup."},
        {"start": "21:00", "end": "23:00", "activity": "Study/Chores/Personal Time",
         "description": "Flexible time for self-improvement, household tasks, or relaxation."},
        {"start": "23:00", "end": "23:59", "activity": "Sleep",
         "description": "Wind-down and prepare for bed. Aim for consistent sleep schedule."}
    ],
    # --- NEW: Specific schedule for Wednesdays ---
    "wednesday": [
        {"start": "00:00", "end": "06:00", "activity": "Sleep",
         "description": "Essential rest period, focus on deep sleep for recovery."},
        {"start": "06:00", "end": "07:00", "activity": "Personal Care",
         "description": "Morning routine including hygiene, dressing, and quick personal prep."},
        {"start": "07:00", "end": "08:30", "activity": "Kid Morning Prep/Drop-off",
         "description": "Prepare breakfast, get kids ready, pack lunches, drive to school."},
        {"start": "08:30", "end": "12:00", "activity": "Study & Coursework",
         "description": "Focused academic work, lectures, readings, and assignments. Minimize distractions."},
        {"start": "12:00", "end": "13:00", "activity": "Personal Care (Lunch/Chore)",
         "description": "Lunch break, short rest, or quick house tidying. Recharge for the afternoon."},
        {"start": "13:00", "end": "13:30", "activity": "Study & Coursework", # Shortened study block
         "description": "Final wrap-up of academic work before pickup."},
        {"start": "13:30", "end": "13:50", "activity": "Kid Pick-up (Early)", # The new event
         "description": "Drive to school/daycare for early pickup."},
        {"start": "13:50", "end": "20:00", "activity": "Afternoon Coordination", # Starts earlier
         "description": "Manage homework, after-school activities, play time, and prepare for dinner."},
        {"start": "20:00", "end": "21:00", "activity": "Kid Bedtime/Quick Tidy",
         "description": "Evening routine for kids, including story time and light cleanup."},
        {"start": "21:00", "end": "23:00", "activity": "Study/Chores/Personal Time",
         "description": "Flexible time for self-improvement, household tasks, or relaxation."},
        {"start": "23:00", "end": "23:59", "activity": "Sleep",
         "description": "Wind-down and prepare for bed. Aim for consistent sleep schedule."}
    ],
    "weekend": [
        {"start": "00:00", "end": "07:00", "activity": "Sleep", "description": "Extended rest and recuperation."},
        {"start": "07:00", "end": "08:00", "activity": "Personal Care", "description": "Morning routine, typically at a relaxed pace."},
        {"start": "08:00", "end": "13:00", "activity": "Family/Chores", "description": "Quality time, kid's activities, or household tasks."},
        {"start": "13:00", "end": "14:00", "activity": "Lunch/Family Time", "description": "Enjoy lunch with family."},
        {"start": "14:00", "end": "19:00", "activity": "Family Activities/Study/Chores", "description": "Family outings, personal study, or larger chores."},
        {"start": "19:00", "end": "21:00", "activity": "Dinner/Evening Kidcare", "description": "Dinner prep and meal, oversee kid's evening activities."},
        {"start": "21:00", "end": "23:00", "activity": "Personal/Partner Time", "description": "Time for hobbies, unwinding, or connecting with a partner."},
        {"start": "23:00", "end": "23:59", "activity": "Sleep", "description": "Prepare for the next day."}
    ]
}