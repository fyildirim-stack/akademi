import json
import random
from collections import defaultdict

with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

with open("src/data/teachers.json", "r", encoding="utf-8") as f:
    teachers_data = json.load(f)

teachers = { t["name"]: {"course": t["course"], "field": t["field"], "count": int(t["total_hours"])} for t in teachers_data }

# available slots
weeks = []
for w in schedule:
    month = w["saturday_date"].split(".")[1] if w.get("saturday_date") else None
    if not month: continue
    
    # Check if week has valid slots
    sat_valid = w["saturday_course"] not in ["Ders yok", "Ara dönem"]
    sun_valid = w["sunday_course"] not in ["Ders yok", "Ara dönem", "—", None]
    
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

def solve():
    for _ in range(10000):
        # random state
        assignment = {w["week"]: {"saturday": None, "sunday": None} for w in weeks}
        teacher_months = defaultdict(set)
        teacher_counts = defaultdict(int)
        
        # 1. Sabri & Süleyman at W5, W9, W18, W26, W35
        ss_weeks = ["5", "9", "18", "26", "35"]
        success = True
        for w in ss_weeks:
            week_obj = next(wk for wk in weeks if wk["week"] == w)
            if "saturday" in week_obj["slots"] and "sunday" in week_obj["slots"]:
                assignment[w]["saturday"] = sabri
                assignment[w]["sunday"] = suleyman
                teacher_months[sabri].add(week_obj["month"])
                teacher_months[suleyman].add(week_obj["month"])
                teacher_counts[sabri] += 1
                teacher_counts[suleyman] += 1
            else:
                success = False
                break
        if not success: continue
        
        # 2. Necmettin & Harun in 5 same weeks, but not the same as Sabri/Suleyman
        available_nh_weeks = [w for w in weeks if w["week"] not in ss_weeks and len(w["slots"]) == 2]
        # Pick 5 weeks randomly such that their months are unique
        random.shuffle(available_nh_weeks)
        nh_weeks = []
        nh_months = set()
        for w in available_nh_weeks:
            if w["month"] not in nh_months:
                nh_weeks.append(w)
                nh_months.add(w["month"])
            if len(nh_weeks) == 5: break
        
        if len(nh_weeks) < 5: continue
        
        for w in nh_weeks:
            assignment[w["week"]]["saturday"] = necmettin
            assignment[w["week"]]["sunday"] = harun
            teacher_months[necmettin].add(w["month"])
            teacher_months[harun].add(w["month"])
            teacher_counts[necmettin] += 1
            teacher_counts[harun] += 1
            
        # 3. Fill the rest
        remaining_slots = []
        for w in weeks:
            for s in w["slots"]:
                if assignment[w["week"]][s] is None:
                    remaining_slots.append((w["week"], w["month"], s))
                    
        # Available teachers
        remaining_teachers = []
        for t, data in teachers.items():
            needed = data["count"] - teacher_counts[t]
            remaining_teachers.extend([t] * needed)
            
        random.shuffle(remaining_teachers)
        
        # Try to assign remaining slots
        possible = True
        for week_num, month, day in remaining_slots:
            # find a teacher who hasn't taught in this month
            assigned = False
            for i, t in enumerate(remaining_teachers):
                if month not in teacher_months[t]:
                    # Also check if this teacher is already in this week!
                    if assignment[week_num]["saturday"] == t or assignment[week_num]["sunday"] == t:
                        continue
                    
                    assignment[week_num][day] = t
                    teacher_months[t].add(month)
                    teacher_counts[t] += 1
                    remaining_teachers.pop(i)
                    assigned = True
                    break
            if not assigned:
                possible = False
                break
                
        if possible:
            return assignment
            
    return None

ans = solve()
if not ans:
    print("Could not find a valid schedule!")
else:
    print("Found schedule!")
    # Update schedule.json
    for w in schedule:
        week_num = w["week"]
        if week_num in ans:
            for day in ["saturday", "sunday"]:
                if ans[week_num][day]:
                    t = ans[week_num][day]
                    t_data = teachers[t]
                    
                    w[f"{day}_course"] = t_data["course"]
                    
                    # field update
                    fields = w.get("fields", "").split("\n")
                    if len(fields) < 2: fields = ["Cts: ", "Paz: "]
                    if day == "saturday": fields[0] = f"Cts: {t_data['field']}"
                    if day == "sunday": fields[1] = f"Paz: {t_data['field']}"
                    w["fields"] = "\n".join(fields)
                    
                    # teacher update
                    ts = w.get("teachers", "").split("\n")
                    if len(ts) < 2: ts = ["Cts: ", "Paz: "]
                    if day == "saturday": ts[0] = f"Cts: {t}"
                    if day == "sunday": ts[1] = f"Paz: {t}"
                    w["teachers"] = "\n".join(ts)
                else:
                    if w.get(f"{day}_course") not in ["Ders yok", "Ara dönem", "—", None]:
                        w[f"{day}_course"] = "—"
                        w["fields"] = ""
                        w["teachers"] = ""
                        
    with open("src/data/schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    print("Saved schedule.")
