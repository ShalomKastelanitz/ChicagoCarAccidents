import csv
from datetime import datetime

from database.connect import accidents,injuries
from Repository.load_data_to_db import insertManyDocuments

def parse_date(date_str: str):
    # חותך את המחרוזת של התאריך כך שתכלול רק את החלק של התאריך
    date_str = date_str.split(' ')[0]  # לוקח רק את החלק הראשון, כלומר את התאריך בלבד
    date_format = '%m/%d/%Y'  # פורמט של תאריך בלבד
    return datetime.strptime(date_str, date_format)

# נרמול הנתונים עם הפרטים החשובים בלבד
def normalize_data(csv_file):
    crashes = []
    injuries = []

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # יצירת רשומת תאונה עם נתונים רלוונטיים בלבד
            crash = {
                "crash_record_id": row["CRASH_RECORD_ID"],
                "crash_date":parse_date(row["CRASH_DATE"]) ,
                "posted_speed_limit": row["POSTED_SPEED_LIMIT"],
                "traffic_control_device": row["TRAFFIC_CONTROL_DEVICE"],
                "weather_condition": row["WEATHER_CONDITION"],
                "first_crash_type": row["FIRST_CRASH_TYPE"],
                "street_name": row["STREET_NAME"],
                "lane_cnt": row["LANE_CNT"],
                "light_condition": row["LIGHTING_CONDITION"],
                "prim_contributory_cause": row["PRIM_CONTRIBUTORY_CAUSE"],
                "sec_contributory_cause": row["SEC_CONTRIBUTORY_CAUSE"]
            }
            crashes.append(crash)

            # יצירת רשומת פציעות רלוונטיות
            injury = {
                "crash_record_id": row["CRASH_RECORD_ID"],
                "injuries_total": row["INJURIES_TOTAL"],
                "injuries_fatal": row["INJURIES_FATAL"],
                "injuries_incapacitating": row["INJURIES_INCAPACITATING"],
                "injuries_non_incapacitating": row["INJURIES_NON_INCAPACITATING"]
            }
            injuries.append(injury)

    return crashes, injuries

# טעינת נתוני ה-CSV עם עמודות רלוונטיות בלבד
def load_csv_to_mongo(csv_file):
    accidents_to_db, injuries_to_db = normalize_data(csv_file)
    print(len(accidents_to_db))
    # הכנסת נתוני תאונות ופציעות
    insertManyDocuments("injuries", injuries_to_db)
    insertManyDocuments("accidents",accidents_to_db)



if __name__ == "__main__":
    load_csv_to_mongo('../data/Traffic_Crashes_-_Crashes - 20k rows.csv')
    print("Data successfully loaded into MongoDB")
