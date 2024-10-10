# /tests/test_api.py
import pytest
import requests

BASE_URL = "http://localhost:5000"

# בדיקה עבור סה"כ תאונות לפי אזור
def test_get_accidents_by_area():
    response = requests.get(f"{BASE_URL}/accidents/total_by_area?street_name=Main St")
    assert response.status_code == 200
    data = response.json()
    assert "area" in data
    assert "total_accidents" in data
    assert data["area"] == "35TH ST"
    assert isinstance(data["total_accidents"], int)

# בדיקה עבור סה"כ תאונות לפי אזור ולפי תקופה
def test_get_accidents_by_area_and_period():
    response = requests.get(f"{BASE_URL}/accidents/total_by_area_and_period?street_name=Main St&start_date=2022-01-01&end_date=2022-12-31")
    assert response.status_code == 200
    data = response.json()
    assert "area" in data
    assert "total_accidents" in data
    assert data["area"] == "35TH ST"
    assert isinstance(data["total_accidents"], int)

# בדיקה עבור תאונות לפי סיבה עיקרית
def test_get_accidents_by_cause():
    response = requests.get(f"{BASE_URL}/accidents/total_by_cause?cause=FAILING TO REDUCE SPEED TO AVOID CRASH")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "prim_contributory_cause" in data[0]

# בדיקה עבור סטטיסטיקה על פציעות לפי אזור
def test_get_injury_statistics_by_area():
    response = requests.get(f"{BASE_URL}/injuries/injury_statistics_by_area?street_name=Main St")
    assert response.status_code == 200
    data = response.json()
    assert "area" in data
    assert "total_injuries" in data
    assert "fatal_injuries" in data
    assert "non_fatal_injuries" in data
    assert data["area"] == "35TH ST"
    assert isinstance(data["total_injuries"], int)
    assert isinstance(data["fatal_injuries"], int)
    assert isinstance(data["non_fatal_injuries"], int)
