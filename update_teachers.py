import json

with open("src/data/teachers.json", "r", encoding="utf-8") as f:
    teachers = json.load(f)

# Add new teacher
new_teacher = {
    "name": "Dr. Abdülaziz KIRANŞAL",
    "field": "İlahiyat",
    "course": "Aile ve Gençliğin Sorunları ve Çözüm Önerileri",
    "total_hours": "5"
}
# prevent duplicate if ran multiple times
if not any(t["name"] == new_teacher["name"] for t in teachers):
    teachers.append(new_teacher)

first_names = ["Musa", "Harun", "Necmettin", "İbrahim"]
last_names = ["Sabri", "Süleyman"]

def get_order(t):
    name = t["name"]
    # Check first
    for i, fn in enumerate(first_names):
        if fn in name:
            return i
            
    # Check last
    for i, ln in enumerate(last_names):
        if ln in name:
            return 1000 + i
            
    # Middle
    return 100

teachers.sort(key=get_order)

with open("src/data/teachers.json", "w", encoding="utf-8") as f:
    json.dump(teachers, f, ensure_ascii=False, indent=2)

# Add to schedule.json
with open("src/data/schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

lessons_to_place = 5

if not any("Abdülaziz" in str(w.get("teachers", "")) for w in schedule):
    for w in schedule:
        if w["week"] == "44" and w.get("sunday_course") == "—":
            w["sunday_course"] = new_teacher["course"]
            fields = w.get("fields", "").split("\n")
            if len(fields) == 1:
                w["fields"] = fields[0] + "\nPaz: " + new_teacher["field"]
            w["teachers"] = w.get("teachers", "") + "\nPaz: " + new_teacher["name"]
            lessons_to_place -= 1

    if lessons_to_place > 0:
        schedule.append({
            "week": "45",
            "saturday_date": "07.08.2027",
            "sunday_date": "08.08.2027",
            "fields": f"Cts: {new_teacher['field']}\nPaz: {new_teacher['field']}",
            "saturday_course": new_teacher["course"],
            "sunday_course": new_teacher["course"],
            "teachers": f"Cts: {new_teacher['name']}\nPaz: {new_teacher['name']}",
            "planned_hours": "8"
        })
        lessons_to_place -= 2

    if lessons_to_place > 0:
        schedule.append({
            "week": "46",
            "saturday_date": "14.08.2027",
            "sunday_date": "15.08.2027",
            "fields": f"Cts: {new_teacher['field']}\nPaz: {new_teacher['field']}",
            "saturday_course": new_teacher["course"],
            "sunday_course": new_teacher["course"],
            "teachers": f"Cts: {new_teacher['name']}\nPaz: {new_teacher['name']}",
            "planned_hours": "8"
        })
        lessons_to_place -= 2

    with open("src/data/schedule.json", "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

print("Updated teachers and schedule.")
