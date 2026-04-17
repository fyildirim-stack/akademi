import json
import random
from collections import defaultdict

# Load data
with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# Ensure Sept weeks exist
sept_1 = next((w for w in schedule if w["saturday_date"] == "19.09.2026"), None)
if not sept_1:
    schedule.insert(0, {
        "week": "S1",
        "saturday_date": "19.09.2026",
        "sunday_date": "20.09.2026",
        "fields": "Cts: \nPaz: ",
        "saturday_course": "—",
        "sunday_course": "—",
        "teachers": "Cts: \nPaz: ",
        "planned_hours": "8"
    })

sept_2 = next((w for w in schedule if w["saturday_date"] == "26.09.2026"), None)
if not sept_2:
    schedule.insert(1, {
        "week": "S2",
        "saturday_date": "26.09.2026",
        "sunday_date": "27.09.2026",
        "fields": "Cts: \nPaz: ",
        "saturday_course": "—",
        "sunday_course": "—",
        "teachers": "Cts: \nPaz: ",
        "planned_hours": "8"
    })

# Remove any weeks >= 39 (to balance the 4 new slots added in Sept)
# Note: we need 79 slots.
# Sept S1 (2), Sept S2 (2) -> 4 slots.
# W1 to W37 -> 37 * 2 = 74 slots. (Total 78)
# We need 1 more slot -> W38 Saturday! (Total 79)
schedule = [w for w in schedule if w["week"] in ["S1", "S2"] or (w["week"].isdigit() and int(w["week"]) <= 38)]

# Re-number the "week" attribute for visual consistency (1 to 40)
# But wait, keeping "S1" "S2" is fine, or we can just rewrite "week" as str(idx+1)
for i, w in enumerate(schedule):
    w["week"] = str(i + 1)

with open("src/data/teachers.json", "r", encoding="utf-8") as f:
    teachers_data = json.load(f)

teachers = { t["name"]: {"course": t["course"], "field": t["field"], "count": int(t["total_hours"])} for t in teachers_data }

weeks = []
for w in schedule:
    sat_date = w.get("saturday_date")
    if not sat_date: continue
    month = sat_date.split(".")[1]
    wk_str = w["week"]
    
    sat_valid = True
    sun_valid = True
    
    # We open everything up to the end, but the VERY LAST week in the list
    # (which was W38, now it is week 40 because 38+2=40) 
    # needs to have only Saturday open to reach exactly 79.
    if wk_str == str(len(schedule)): # Last week
        sun_valid = False
        
    slots = []
    if sat_valid: slots.append("saturday")
    if sun_valid: slots.append("sunday")
    
    if slots:
        weeks.append({
            "week": w["week"],
            "month": month,
            "slots": slots
        })

sabri = "Prof. Dr. Sabri TEKİR"
suleyman = "Doç. Dr. Süleyman AKDEMİR"
necmettin = "Doç. Dr. Necmettin ÇALIŞKAN"
harun = "Prof. Dr. Harun BEKİROĞLU"

def attempt_solve():
    assignment = {w["week"]: {"saturday": None, "sunday": None} for w in weeks}
    teacher_months = defaultdict(set)
    teacher_counts = defaultdict(int)

    # We need to assign Sabri & Suleyman to end of months.
    # The months are: 09, 10, 11, 12, 01, 02, 03, 04, 05, 06.
    # Let's pick 5 months for them, e.g., 10, 12, 02, 04, 06.
    # Find the last valid week of these 5 months.
    target_months = ["10", "12", "02", "04", "06"]
    ss_weeks = []
    for tm in target_months:
        month_weeks = [w for w in weeks if w["month"] == tm and len(w["slots"]) == 2]
        if month_weeks:
            ss_weeks.append(month_weeks[-1]["week"])

    for w in ss_weeks:
        week_obj = next(wk for wk in weeks if wk["week"] == w)
        assignment[w]["saturday"] = sabri
        assignment[w]["sunday"] = suleyman
        teacher_months[sabri].add(week_obj["month"])
        teacher_months[suleyman].add(week_obj["month"])
        teacher_counts[sabri] += 1
        teacher_counts[suleyman] += 1

    available_nh_weeks = [w for w in weeks if w["week"] not in ss_weeks and len(w["slots"]) == 2]
    random.shuffle(available_nh_weeks)
    nh_weeks = []
    nh_months = set()
    for w in available_nh_weeks:
        if w["month"] not in nh_months:
            nh_weeks.append(w)
            nh_months.add(w["month"])
        if len(nh_weeks) == 5: break

    for w in nh_weeks:
        assignment[w["week"]]["saturday"] = necmettin
        assignment[w["week"]]["sunday"] = harun
        teacher_months[necmettin].add(w["month"])
        teacher_months[harun].add(w["month"])
        teacher_counts[necmettin] += 1
        teacher_counts[harun] += 1

    remaining_slots = []
    for w in weeks:
        for s in w["slots"]:
            if assignment[w["week"]][s] is None:
                remaining_slots.append((w["week"], w["month"], s))

    remaining_teachers = []
    for t, data in teachers.items():
        needed = data["count"] - teacher_counts[t]
        remaining_teachers.extend([t] * needed)

    if len(remaining_slots) != len(remaining_teachers):
        print(f"Slot mismatch! slots={len(remaining_slots)}, teachers={len(remaining_teachers)}")
        return False

    random.shuffle(remaining_teachers)

    def solve_backtrack(slot_idx):
        if slot_idx == len(remaining_slots):
            return True
            
        week_num, month, day = remaining_slots[slot_idx]
        
        tried = set()
        for i, t in enumerate(remaining_teachers):
            if t in tried: continue
            tried.add(t)
            
            if month not in teacher_months[t]:
                if assignment[week_num]["saturday"] != t and assignment[week_num]["sunday"] != t:
                    assignment[week_num][day] = t
                    teacher_months[t].add(month)
                    teacher_counts[t] += 1
                    popped = remaining_teachers.pop(i)
                    
                    if solve_backtrack(slot_idx + 1):
                        return True
                        
                    remaining_teachers.insert(i, popped)
                    teacher_counts[t] -= 1
                    teacher_months[t].remove(month)
                    assignment[week_num][day] = None
                    
        return False

    if solve_backtrack(0):
        return assignment
    return None

assignment = None
for _ in range(500):
    assignment = attempt_solve()
    if assignment: break

if assignment:
    print("Found schedule!")
    for w in schedule:
        wk_str = w["week"]
        
        # Valid logic
        sat_valid = True
        sun_valid = True
        if wk_str == str(len(schedule)): sun_valid = False
        
        if not sat_valid:
            w["saturday_course"] = "Ders yok"
        if not sun_valid:
            w["sunday_course"] = "Ders yok"
            
        if wk_str in assignment:
            for day in ["saturday", "sunday"]:
                is_valid = (day == "saturday" and sat_valid) or (day == "sunday" and sun_valid)
                if is_valid:
                    t = assignment[wk_str][day]
                    t_data = teachers[t]
                    w[f"{day}_course"] = t_data["course"]
                    w["planned_hours"] = "8" if (sat_valid and sun_valid) else "4"
                    
                    fields = w.get("fields", "").split("\n")
                    if len(fields) < 2: fields = ["Cts: ", "Paz: "]
                    if day == "saturday": fields[0] = f"Cts: {t_data['field']}"
                    if day == "sunday": fields[1] = f"Paz: {t_data['field']}"
                    w["fields"] = "\n".join(fields)
                    
                    ts = w.get("teachers", "").split("\n")
                    if len(ts) < 2: ts = ["Cts: ", "Paz: "]
                    if day == "saturday": ts[0] = f"Cts: {t}"
                    if day == "sunday": ts[1] = f"Paz: {t}"
                    w["teachers"] = "\n".join(ts)
                    
    with open("src/data/schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
else:
    print("Failed")
