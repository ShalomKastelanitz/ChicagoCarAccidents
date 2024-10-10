from pymongo import MongoClient
from database.connect import accidents,injuries


# יצירת אינדקסים רק על שדות רלוונטיים לשאילתות
accidents.create_index([("crash_date", 1)])
accidents.create_index([("street_name", 1)])
injuries.create_index([("crash_record_id", 1)])

print("Indexes created successfully")