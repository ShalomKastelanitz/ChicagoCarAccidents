# /app/repo.py
from pymongo import MongoClient
from datetime import datetime
from database.connect import accidents ,injuries
# חיבור ל-MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chicago_accidents"]

# פונקציה לשליפת תאונות לפי אזור
def get_total_accidents_by_area(area):
    return accidents.count_documents({"street_name": area})

# פונקציה לשליפת תאונות לפי אזור ותקופה (יום/שבוע/חודש)
def get_total_accidents_by_area_and_period(area, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    return accidents.count_documents({
        "street_name": area,
        "crash_date": {"$gte": start_date, "$lte": end_date}
    })

# פונקציה לשליפת תאונות לפי סיבה עיקרית
def get_accidents_grouped_by_cause(street_name):
    pipeline = [
        {
            "$match": {
                "street_name": street_name  # סינון לפי שם האזור
            }
        },
        {
            "$group": {
                "_id": "$prim_contributory_cause",  # קיבוץ לפי הסיבה העיקרית
                "accidents": {
                    "$push": {
                        "crash_record_id": "$crash_record_id",
                        "crash_date": "$crash_date",
                        "street_name": "$street_name",
                        "posted_speed_limit": "$posted_speed_limit",
                        "traffic_control_device": "$traffic_control_device",
                        "weather_condition": "$weather_condition",
                        "first_crash_type": "$first_crash_type",
                        "lane_cnt": "$lane_cnt",
                        "light_condition": "$light_condition"
                    }
                },
                "count": {"$sum": 1}  # ספירת מספר התאונות בכל קבוצה
            }
        },
        {
            "$sort": {"count": -1}  # מיון לפי מספר התאונות בכל קבוצה (יורד)
        }
    ]

    # ביצוע השאילתה במסד הנתונים והחזרת התוצאות
    grouped_accidents = list(accidents.aggregate(pipeline))
    return grouped_accidents

# פונקציה לשליפת סטטיסטיקות פציעות לפי אזור
def get_injury_statistics_by_area(area):
    crash_record_id=accidents.find({{"street_name": area}},{"crash_record_id":1 ,"_id": 0})
    total_injuries = injuries.count_documents({"crash_record_id": crash_record_id})
    fatal_injuries = injuries.count_documents({"crash_record_id": crash_record_id, "injuries_fatal": {"$gt": 0}})
    non_fatal_injuries = injuries.count_documents({"crash_record_id": crash_record_id, "injuries_fatal": 0})
    return {
        "total_injuries": total_injuries,
        "fatal_injuries": fatal_injuries,
        "non_fatal_injuries": non_fatal_injuries
    }
