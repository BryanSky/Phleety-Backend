from helper.storage_helper import Storage


class SafetyModel(object):

    def __init__(self):
        self.storage = Storage()
        return

    def kpi_get_tire_pressure(self):

        return