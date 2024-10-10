from flask import Blueprint, jsonify, request
from Repository import repo
accidents_bp = Blueprint('accidents', __name__)

# סה"כ תאונות לפי אזור לאורך כל התקופה
@accidents_bp.route("/accidents/total_by_area", methods=["GET"])
def get_accidents_by_area():
    area = request.args.get("street_name")
    total_accidents = repo.get_total_accidents_by_area(area)
    return jsonify({"area": area, "total_accidents": total_accidents})

# סה"כ תאונות לפי אזור ולפי תקופה (יום/שבוע/חודש)
@accidents_bp.route("/accidents/total_by_area_and_period", methods=["GET"])
def get_accidents_by_area_and_period():
    area = request.args.get("street_name")
    start_date = request.args.get("start_date")  # כך זה אמור להיות- "2022-01-01"
    end_date = request.args.get("end_date")
    total_accidents = repo.get_total_accidents_by_area_and_period(area, start_date, end_date)
    return jsonify({"area": area, "total_accidents": total_accidents})

# תאונות מקובצות לפי הסיבה העיקרית לתאונה
@accidents_bp.route("/accidents/grouped_by_cause", methods=["GET"])
def get_accidents_grouped_by_cause():
    street_name = request.args.get("street_name")  # לדוגמה: Main St

    # שליפת הנתונים מהפונקציה ב-repo
    accidents_grouped_by_cause = repo.get_accidents_grouped_by_cause(street_name)

    return jsonify(accidents_grouped_by_cause)