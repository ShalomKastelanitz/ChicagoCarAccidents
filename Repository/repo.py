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
def get_accidents_by_cause(cause):
    return list(accidents.find({"prim_contributory_cause": cause}, {"_id": 0}))

# פונקציה לשליפת סטטיסטיקות פציעות לפי אזור
def get_injury_statistics_by_area(area):
    total_injuries = injuries.count_documents({"street_name": area})
    fatal_injuries = injuries.count_documents({"street_name": area, "injuries_fatal": {"$gt": 0}})
    non_fatal_injuries = injuries.count_documents({"street_name": area, "injuries_fatal": 0})
    return {
        "total_injuries": total_injuries,
        "fatal_injuries": fatal_injuries,
        "non_fatal_injuries": non_fatal_injuries
    }
