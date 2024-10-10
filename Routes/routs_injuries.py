# /app/routes/injuries.py
from flask import Blueprint, jsonify, request
from Repository import repo
injuries_bp = Blueprint('injuries', __name__)

# סטטיסטיקה על פציעות לפי אזור
@injuries_bp.route("/injuries/injury_statistics_by_area", methods=["GET"])
def get_injury_statistics_by_area():
    area = request.args.get("street_name")
    stats = repo.get_injury_statistics_by_area(area)
    return jsonify({
        "area": area,
        "total_injuries": stats["total_injuries"],
        "fatal_injuries": stats["fatal_injuries"],
        "non_fatal_injuries": stats["non_fatal_injuries"]
    })
