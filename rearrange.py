import json

with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

def get_day_info(week_idx, day_key):
    # day_key is 'saturday' or 'sunday'
    w = schedule[week_idx]
    course = w[f"{day_key}_course"]
    
    # parse fields "Cts: X\nPaz: Y"
    fields_split = w["fields"].split("\n") if w.get("fields") else []
    field = ""
    for f_str in fields_split:
        if day_key == "saturday" and f_str.startswith("Cts:"): field = f_str.replace("Cts: ", "")
        if day_key == "sunday" and f_str.startswith("Paz:"): field = f_str.replace("Paz: ", "")
        
    # parse teachers
    teachers_split = w["teachers"].split("\n") if w.get("teachers") else []
    teacher = ""
    for t_str in teachers_split:
        if day_key == "saturday" and t_str.startswith("Cts:"): teacher = t_str.replace("Cts: ", "")
        if day_key == "sunday" and t_str.startswith("Paz:"): teacher = t_str.replace("Paz: ", "")
        
    return {"course": course, "field": field, "teacher": teacher}

def set_day_info(week_idx, day_key, info):
    w = schedule[week_idx]
    w[f"{day_key}_course"] = info["course"]
    
    # set fields
    fields_split = w["fields"].split("\n") if w.get("fields") else ["Cts: ", "Paz: "]
    if len(fields_split) < 2:
        fields_split = ["Cts: ", "Paz: "]
    
    # reconstruct
    cts_f = fields_split[0].replace("Cts: ", "") if fields_split[0].startswith("Cts:") else ""
    paz_f = fields_split[1].replace("Paz: ", "") if len(fields_split)>1 and fields_split[1].startswith("Paz:") else ""
    
    if day_key == "saturday": cts_f = info["field"]
    if day_key == "sunday": paz_f = info["field"]
    
    w["fields"] = f"Cts: {cts_f}\nPaz: {paz_f}"
    
    # set teachers
    teachers_split = w["teachers"].split("\n") if w.get("teachers") else ["Cts: ", "Paz: "]
    if len(teachers_split) < 2:
        teachers_split = ["Cts: ", "Paz: "]
        
    cts_t = teachers_split[0].replace("Cts: ", "") if teachers_split[0].startswith("Cts:") else ""
    paz_t = teachers_split[1].replace("Paz: ", "") if len(teachers_split)>1 and teachers_split[1].startswith("Paz:") else ""
    
    if day_key == "saturday": cts_t = info["teacher"]
    if day_key == "sunday": paz_t = info["teacher"]
    
    w["teachers"] = f"Cts: {cts_t}\nPaz: {paz_t}"

def swap(w1, d1, w2, d2):
    i1 = next(i for i, w in enumerate(schedule) if w["week"] == str(w1))
    i2 = next(i for i, w in enumerate(schedule) if w["week"] == str(w2))
    
    info1 = get_day_info(i1, d1)
    info2 = get_day_info(i2, d2)
    
    set_day_info(i1, d1, info2)
    set_day_info(i2, d2, info1)

# Fix week 1 teacher prefix first:
# "Paz: Doç. Dr. Süleyman AKDEMİR\nPaz: Prof. Dr. Sabri TEKİR"
# -> "Cts: Doç. Dr. Süleyman AKDEMİR\nPaz: Prof. Dr. Sabri TEKİR"
w1 = next(w for w in schedule if w["week"] == "1")
w1["teachers"] = "Cts: Doç. Dr. Süleyman AKDEMİR\nPaz: Prof. Dr. Sabri TEKİR"

# 1. Sabri & Süleyman pairs:
# Sabri is at:
# W9 (Cts), W17 (Cts), W28 (Paz), W37 (Paz)
# Süleyman is at:
# W5 (Paz), W25 (Cts), W34 (Cts), W41 (Paz)

# Swap Süleyman into Sabri's weeks:
# Süleyman in W5(Paz) <-> W9(Paz) [Necmettin]
swap(5, "sunday", 9, "sunday")
# Süleyman in W25(Cts) <-> W17(sunday) [Necmettin]
swap(25, "saturday", 17, "sunday")
# Süleyman in W34(Cts) <-> W28(saturday) [Muhammed Maruf]
swap(34, "saturday", 28, "saturday")
# Süleyman in W41(Paz) <-> W37(saturday) [Muhammed Maruf]
swap(41, "sunday", 37, "saturday")

# 2. Necmettin & Harun pairs:
# Necmettin is now at:
# W5 (Paz), W25 (Cts), W29 (Cts), W38 (Cts)
# Harun is at:
# W10 (Paz), W18 (Paz), W30 (Cts), W39 (Cts)

# Swap Harun into Necmettin's weeks:
# Harun in W10(Paz) <-> W5(saturday) [Musa Budak]
swap(10, "sunday", 5, "saturday")
# Harun in W18(Paz) <-> W25(sunday) [Recai Tekin]
swap(18, "sunday", 25, "sunday")
# Harun in W30(Cts) <-> W29(sunday) [Musa Öztük]
swap(30, "saturday", 29, "sunday")
# Harun in W39(Cts) <-> W38(sunday) [Musa Öztük]
swap(39, "saturday", 38, "sunday")

with open("src/data/schedule.json", "w", encoding="utf-8") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

print("Schedule updated!")
