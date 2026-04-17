import json
import random
from collections import defaultdict

# Load data
with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# Ensure week 45 and 46 are there. If not, add them back.
week_45 = next((w for w in schedule if w["week"] == "45"), None)
if not week_45:
    schedule.append({
        "week": "45",
        "saturday_date": "07.08.2027",
        "sunday_date": "08.08.2027",
        "fields": "Cts: \nPaz: ",
        "saturday_course": "—",
        "sunday_course": "—",
        "teachers": "Cts: \nPaz: ",
        "planned_hours": "8"
    })
week_46 = next((w for w in schedule if w["week"] == "46"), None)
if not week_46:
    schedule.append({
        "week": "46",
        "saturday_date": "14.08.2027",
        "sunday_date": "15.08.2027",
        "fields": "Cts: \nPaz: ",
        "saturday_course": "—",
        "sunday_course": "—",
        "teachers": "Cts: \nPaz: ",
        "planned_hours": "8"
    })

with open("src/data/teachers.json", "r", encoding="utf-8") as f:
    teachers_data = json.load(f)

teachers = { t["name"]: {"course": t["course"], "field": t["field"], "count": int(t["total_hours"])} for t in teachers_data }

# Available slots
weeks = []
for w in schedule:
    sat_date = w.get("saturday_date")
    if not sat_date: continue
    
    month = sat_date.split(".")[1]
    
    sat_valid = w.get("saturday_course") not in ["Ders yok", "Ara dönem"]
    sun_valid = w.get("sunday_course") not in ["Ders yok", "Ara dönem", None]
    
    # We opened up w31 saturday (1 May), w44 sunday, w45, w46
    if w["week"] in ["44", "45", "46"]:
        sat_valid = True
        sun_valid = True
        
    if w["week"] == "31":
        sat_valid = True
    
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
    for attempt in range(50000):
        assignment = {w["week"]: {"saturday": None, "sunday": None} for w in weeks}
        teacher_months = defaultdict(set)
        teacher_counts = defaultdict(int)
        
        # 1. Sabri & Süleyman at end of months: 5, 9, 18, 26, 35
        ss_weeks = ["5", "9", "18", "26", "35"]
        success = True
        for w in ss_weeks:
            week_obj = next(wk for wk in weeks if wk["week"] == w)
            assignment[w]["saturday"] = sabri
            assignment[w]["sunday"] = suleyman
            teacher_months[sabri].add(week_obj["month"])
            teacher_months[suleyman].add(week_obj["month"])
            teacher_counts[sabri] += 1
            teacher_counts[suleyman] += 1
            
        # 2. Necmettin & Harun in 5 same weeks, unique months
        available_nh_weeks = [w for w in weeks if w["week"] not in ss_weeks and len(w["slots"]) == 2]
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
        
        possible = True
        for week_num, month, day in remaining_slots:
            assigned = False
            for i, t in enumerate(remaining_teachers):
                if month not in teacher_months[t]:
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
    print("Could not find a valid schedule.")
else:
    print("Found a valid schedule!")
    
    for w in schedule:
        week_num = w["week"]
        if week_num in ans:
            for day in ["saturday", "sunday"]:
                valid = False
                if day == "saturday" and w.get("saturday_course") not in ["Ders yok", "Ara dönem"]: valid = True
                if day == "sunday" and w.get("sunday_course") not in ["Ders yok", "Ara dönem", None]: valid = True
                if week_num in ["31", "44", "45", "46"]:
                    if week_num == "31" and day == "saturday": valid = True
                    if week_num in ["44", "45", "46"]: valid = True
                
                if valid:
                    t = ans[week_num][day]
                    if not t: continue
                    t_data = teachers[t]
                    
                    w[f"{day}_course"] = t_data["course"]
                    
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
    print("Schedule successfully rewritten!")
