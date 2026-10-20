"""
Tests for HeartInsight Flask Web Application
============================================
Tests all routes, views, JSON APIs, and risk calculation logic.
"""

import pytest
from webapp.app import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_landing_page(client):
    """Test index route loads with KPI statistics."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Heart Disease Analysis" in resp.data or b"HeartInsight" in resp.data


def test_dashboard_routes(client):
    """Test Tableau dashboard and story route fallbacks."""
    resp = client.get("/dashboard")
    assert resp.status_code == 200

    resp = client.get("/story")
    assert resp.status_code == 200


def test_data_and_analysis_routes(client):
    """Test data table and analysis pages."""
    resp = client.get("/data")
    assert resp.status_code == 200

    resp = client.get("/analysis")
    assert resp.status_code == 200


def test_pipeline_view(client):
    """Test pipeline status and execution view."""
    resp = client.get("/pipeline")
    assert resp.status_code == 200
    assert b"Pipeline" in resp.data


def test_datasets_view(client):
    """Test benchmark datasets catalog view."""
    resp = client.get("/datasets")
    assert resp.status_code == 200
    assert b"Benchmark Datasets" in resp.data


def test_calculator_view(client):
    """Test interactive risk calculator page."""
    resp = client.get("/calculator")
    assert resp.status_code == 200
    assert b"Medical Disclaimer" in resp.data or b"Risk" in resp.data


def test_api_stats(client):
    """Test /api/stats endpoint."""
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_patients" in data
    assert "disease_rate" in data
    assert data["total_patients"] > 0


def test_api_pipeline_status(client):
    """Test /api/pipeline-status endpoint."""
    resp = client.get("/api/pipeline-status")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "status" in data


def test_api_analytics(client):
    """Test /api/analytics DuckDB endpoint."""
    resp = client.get("/api/analytics")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "success"
    assert "queries" in data


def test_api_calculate_risk(client):
    """Test /api/calculate-risk heuristic scoring."""
    payload = {
        "age": 62,
        "trestbps": 150,
        "chol": 260,
        "fbs": 1,
        "exang": 1,
        "oldpeak": 2.5,
        "ca": 2
    }
    resp = client.post("/api/calculate-risk", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["score"] >= 8
    assert data["risk_level"] in ["High Risk", "Very High Risk"]
    assert "disclaimer" in data
