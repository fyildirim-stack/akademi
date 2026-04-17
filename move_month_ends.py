import json

with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

def get_day_info(week_idx, day_key):
    w = schedule[week_idx]
    course = w[f"{day_key}_course"]
    
    fields_split = w["fields"].split("\n") if w.get("fields") else []
    field = ""
    for f_str in fields_split:
        if day_key == "saturday" and f_str.startswith("Cts:"): field = f_str.replace("Cts: ", "")
        if day_key == "sunday" and f_str.startswith("Paz:"): field = f_str.replace("Paz: ", "")
        
    teachers_split = w["teachers"].split("\n") if w.get("teachers") else []
    teacher = ""
    for t_str in teachers_split:
        if day_key == "saturday" and t_str.startswith("Cts:"): teacher = t_str.replace("Cts: ", "")
        if day_key == "sunday" and t_str.startswith("Paz:"): teacher = t_str.replace("Paz: ", "")
        
    return {"course": course, "field": field, "teacher": teacher}

def set_day_info(week_idx, day_key, info):
    w = schedule[week_idx]
    w[f"{day_key}_course"] = info["course"]
    
    fields_split = w.get("fields", "").split("\n")
    if len(fields_split) < 2: fields_split = ["Cts: ", "Paz: "]
    cts_f = fields_split[0].replace("Cts: ", "") if fields_split[0].startswith("Cts:") else ""
    paz_f = fields_split[1].replace("Paz: ", "") if len(fields_split)>1 and fields_split[1].startswith("Paz:") else ""
    
    if day_key == "saturday": cts_f = info["field"]
    if day_key == "sunday": paz_f = info["field"]
    w["fields"] = f"Cts: {cts_f}\nPaz: {paz_f}"
    
    teachers_split = w.get("teachers", "").split("\n")
    if len(teachers_split) < 2: teachers_split = ["Cts: ", "Paz: "]
    cts_t = teachers_split[0].replace("Cts: ", "") if teachers_split[0].startswith("Cts:") else ""
    paz_t = teachers_split[1].replace("Paz: ", "") if len(teachers_split)>1 and teachers_split[1].startswith("Paz:") else ""
    
    if day_key == "saturday": cts_t = info["teacher"]
    if day_key == "sunday": paz_t = info["teacher"]
    w["teachers"] = f"Cts: {cts_t}\nPaz: {paz_t}"

def swap_full_week(w1_str, w2_str):
    i1 = next(i for i, w in enumerate(schedule) if w["week"] == w1_str)
    i2 = next(i for i, w in enumerate(schedule) if w["week"] == w2_str)
    
    s1 = get_day_info(i1, "saturday")
    su1 = get_day_info(i1, "sunday")
    
    s2 = get_day_info(i2, "saturday")
    su2 = get_day_info(i2, "sunday")
    
    set_day_info(i1, "saturday", s2)
    set_day_info(i1, "sunday", su2)
    
    set_day_info(i2, "saturday", s1)
    set_day_info(i2, "sunday", su1)

# Current Sabri & Süleyman weeks: 1, 9, 17, 28, 37
# Target end-of-month weeks: 5 (Oct), 9 (Nov), 18 (Jan), 26 (Mar), 35 (May)
swap_full_week("1", "5")
swap_full_week("17", "18")
swap_full_week("28", "26")
swap_full_week("37", "35")

with open("src/data/schedule.json", "w", encoding="utf-8") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

print("Moved to month ends!")
