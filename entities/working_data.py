

class ImprovementRecommendation(object):

    def __init__(self, action=None, improvement=None, improvement_unit=None, current_value=None):
        self.action = action
        self.improvement = improvement
        self.improvement_unit = improvement_unit
        self.current_value = current_value
        return


class KPIMetrics(object):

    def __init__(self, value=None, unit=None):
        self.value = value
        self.value_unit = unit
        return


class VehicleCondition(object):

    def __init__(self, status=None):
        self.status = status
        return
