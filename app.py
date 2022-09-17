from flask import Flask, request, jsonify, make_response, send_file
# This is a sample Python script.

from entities.working_data import KPIMetrics, ImprovementRecommendation
from helper.storage_helper import Storage
from model.condition_model import ConditionModel
from model.cost_model import CostModel
from model.environmental_model import EnvironmentalModel
from model.safety_model import SafetyModel

app = Flask(__name__)


@app.route('/getMetrics')
def get_metrics():
    if "page" in request.args:
        page = request.args
        if page == "environment":
            environmental_model = EnvironmentalModel()
        else:
            cost_model = CostModel();
    safety_model = SafetyModel()
    metric_co2_per_km = KPIMetrics(value=environmental_model.get_kpi_co2_per_km(), unit="kg")
    metric_co2_per_kg_transported_good = KPIMetrics(value=environmental_model.get_kpi_co2_per_kg(), unit="kg")
    metric_co2_emission_over_time = KPIMetrics(value=environmental_model.get_kpi_co2_emission_over_time(), unit="kg")
    metric_lost_energy_by_breaking = KPIMetrics(value=environmental_model.get_kpi_lost_energy_due_to_braking(), unit="€")
    metric_tire_pressure = KPIMetrics(value=safety_model.kpi_get_tire_pressure(), unit="psi")

    resp = jsonify({"data": [metric_co2_per_km.__dict__, metric_co2_per_kg_transported_good.__dict__,
                    metric_co2_emission_over_time.__dict__, metric_lost_energy_by_breaking.__dict__,
                    metric_tire_pressure.__dict__]})
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    return resp


@app.route('/addData', methods=["POST", "OPTIONS"])
def add_data():
    data = request.get_json()
    Storage().add(data)
    resp = jsonify({"module_id": "Undefined"})
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.headers.add("Access-Control-Allow-Headers", "*")
    return resp


@app.route('/checkPricingStrategy', methods=["POST", "OPTIONS"])
def check_pricing_strategy():
    # TODO: evaluate if weight or empty vehicle is more critical
    recommendation = ImprovementRecommendation(action="Price by weight", improvement=167.88, improvement_unit="€")
    return jsonify(recommendation.__dict__)


@app.route('/findOptimalDriverVehicleCombination', methods=["POST", "OPTIONS"])
def find_optimal_driver():
    data = request.get_json()
    distance = data["distance"]
    time_limit = data["time_limit"]
    strategy = data["strategy"]
    cost_model = CostModel()
    opt_configuration = cost_model.get_optimal_distribution_wih_constraints(distance=distance, time_limit=time_limit,
                                                                            strategy=strategy)
    return jsonify(opt_configuration.__dict__)


@app.route('/checkForNecessaryMaintenance', methods=["POST", "OPTIONS"])
def check_for_maintenance():
    data = request.get_json()
    vehicle_id = data["vehicleID"]
    condition_model = ConditionModel()
    vehicle_condition = condition_model.evaluate_vehicle_condition(vehicle_id)
    return jsonify(vehicle_condition.__dict__)
