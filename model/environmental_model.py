from helper.storage_helper import Storage


class EnvironmentalModel(object):

    def __init__(self):
        self.storage = Storage()
        return

    def get_kpi_co2_per_km(self):
        sql = """SELECT (2.56 * (TotalFuel / TotalDistance)) as co2_per_km, DriverID FROM export_data_zf
GROUP BY DriverID ORDER BY co2_per_km"""
        results = []
        co2_per_km = self.storage.execute_query_selection(sql)
        for row in co2_per_km:
            if len(row) > 1:
                results.append({row[1]: row[0]})
        return results

    def get_kpi_co2_per_kg(self):
        #
        return

    def get_kpi_co2_emission_over_time(self):

        return

    def get_kpi_lost_energy_due_to_braking(self):

        return
