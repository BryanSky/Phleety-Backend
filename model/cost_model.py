from entities.working_data import ImprovementRecommendation
from helper.storage_helper import Storage


class CostModel(object):

    def __init__(self):
        self.storage = Storage()
        return

    def get_optimal_distribution_wih_constraints(self, distance, time_limit, strategy):
        suitable_drivers = self.storage.load_avg_transportation_time_per_driver()
        minimal_time = -1
        minimal_driver = None
        possible_drivers = []
        for row in suitable_drivers:
            if len(row) < 2:
                continue
            if row[0] < minimal_time or minimal_time == -1:
                minimal_time = row[0]
                minimal_driver = row[1]
            if row[0] * distance <= time_limit:
                possible_drivers.append(row[1])
        co2_emission_driver = self.storage.load_co2_emission_by_driver()
        if len(possible_drivers) == 0:
            possible_drivers.append(minimal_driver)
        min_co2_driver = None
        min_co2 = -1
        for row in co2_emission_driver:
            if len(row) < 2 or row[1] not in possible_drivers:
                continue
            if row[0] < min_co2 or min_co2 < 0:
                min_co2 = row[0]
                min_co2_driver = row[1]
        return ImprovementRecommendation(action="Select driver", improvement=min_co2_driver)
