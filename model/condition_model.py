from entities.working_data import VehicleCondition
from helper.storage_helper import Storage


class ConditionModel(object):

    lifetime_estimations = {
        "gearbox": 200000,
        "breaks": 50000,
        "tires": 150000
    }

    def __init__(self):
        self.storage = Storage()
        return

    def evaluate_condition_image(self, image):

        return True

    def evaluate_vehicle_condition(self, vehicle_id):
        breakdown_possibilities = self.storage.load_time_until_breakdown()
        for row in breakdown_possibilities:
            if len(row) > 1 and row[1] == vehicle_id:
                vehicle_runtime = row[0]
                for k in self.lifetime_estimations.keys():
                    maintenance_probability = self.calc_probability_estimation(vehicle_runtime,
                                                                               self.lifetime_estimations[k])
                    return VehicleCondition(status=maintenance_probability)
        return

    def calc_probability_estimation(self, runtime, estimated_total_runtime):
        life_percentage = runtime / estimated_total_runtime
        if life_percentage < 0.5:
            return -1
        if 0.5 < life_percentage < 0.87:
            return 0
        return 1
