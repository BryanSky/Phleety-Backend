from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities import db_objects as dbo


def import_csv_data(filepath):
    db = Storage()
    with open(filepath, "r") as f:
        all_lines = f.readlines()
    if all_lines is not None:
        for line in all_lines[1:]:
            values = line.split(",")
            ds = dbo.TruckDataPoint(TripID=values[0],
                                    DriverID=values[1],
                                    VehicleID=values[2],
                                    VehicleSegmentID=values[3],
                                    AvgFuelConsumption_per100km=values[4],
                                    TotalFuel=values[5],
                                    TotalDistance=values[6],
                                    TimeTorqueHigh70_normalized=values[7],
                                    TimeTorqueHigh50_normalized=values[8],
                                    TimeTorqueHigh30_normalized=values[9],
                                    TimeTorqueAboveThreshold_normalized=values[10],
                                    TimeIdling_normalized=values[11],
                                    TimeGreenSpot_normalized=values[12],
                                    TimeHarshAcceleration_normalized=values[13],
                                    AvgEngineTorque=values[14],
                                    AvgTachoSpeed=values[15],
                                    AvgPositionThrottle=values[16],
                                    NrUpgearChanges_per100km=values[17],
                                    MaxPositionThrottle=values[18],
                                    TimesGearsNegativeCorrect_per100KM=values[19],
                                    TimesGearsPositiveCorrect_per100km=values[20],
                                    TimeGear1_norm=values[21],
                                    TimeGear10_norm=values[22],
                                    TimeGear11_norm=values[23],
                                    TimeGear12_norm=values[24],
                                    TimeGear13_norm=values[25],
                                    TimeGear14_norm=values[26],
                                    TimeGear15_norm=values[27],
                                    TimeGear16_norm=values[28],
                                    TimeGear2_norm=values[29],
                                    TimeGear3_norm=values[30],
                                    TimeGear4_norm=values[31],
                                    TimeGear5_norm=values[32],
                                    TimeGear6_norm=values[33],
                                    TimeGear7_norm=values[34],
                                    TimeGear9_norm=values[35],
                                    TimeGear8_norm=values[36],
                                    NrStops_per100km=values[37],
                                    NrBrakes_per100km=values[38],
                                    TimeBrakes_normalized=values[39],
                                    AltitiudeUp_dm_per_km=values[40],
                                    AltitudeDown_dm_per_km=values[41],
                                    AvgFuelRate=values[42],
                                    AvgRPM=values[43],
                                    DistanceCruising_normalized=values[44],
                                    DistanceGreenSpot_normalized=values[45],
                                    DistanceNoThrottlePush_normalized=values[46],
                                    TimeAboveSpeed_normalized=values[47],
                                    TimeCruising_normalized=values[48],
                                    TimeDriving=values[49],
                                    Driver_Cluster=values[50],
                                    Trip_Cluster=values[51],
                                    NrHarshAcceleration_per100km=values[52],
                                    )
            db.add(ds)
    return


def build_new_dataset():
    return


class Storage(object):

    def __init__(self):
        self.engine = create_engine('mysql+pymysql://nnn:xxx@localhost/hz', echo=True, pool_pre_ping=True)
        self.Session = sessionmaker(bind=self.engine)
        return

    def _create_tables(self):
        dbo.Base.metadata.create_all(self.engine)
        return True

    def add(self, db_obj):
        local_session = self.Session()
        local_session.add(db_obj)
        local_session.commit()
        return

    def load_operating_cost(self):
        sql = """WITH avg_tear AS (
                SELECT AVG(TimeTorqueHigh30_normalized) as tth3, AVG(TimeTorqueHigh70_normalized) as tth7, AVG(TimeTorqueAboveThreshold_normalized) as ttat,
                   AVG(TimeIdling_normalized) as tin, AVG(TimeHarshAcceleration_normalized) as tha, AVG(AvgEngineTorque) as aet, AVG(TimesGearsNegativeCorrect_per100KM) as tgn,
                   AVG(TimesGearsPositiveCorrect_per100km) as tgp, AVG(NrBrakes_per100km) as nb, AVG(NrHarshAcceleration_per100km) as nha
            FROM export_data_zf
            )
            SELECT TotalFuel + (0.8 * edz.TotalDistance), (edz.TimeTorqueHigh30_normalized - avg_tear.tth3),  # TODO: adapt first column
                (edz.TimeTorqueHigh70_normalized - avg_tear.tth7), (edz.TimeTorqueAboveThreshold_normalized - avg_tear.ttat),
                (edz.TimeIdling_normalized - avg_tear.tin), (edz.TimeHarshAcceleration_normalized -avg_tear.tha),
                (edz.AvgEngineTorque - avg_tear.aet), (edz.TimesGearsNegativeCorrect_per100KM - avg_tear.tgn),
                (edz.TimesGearsPositiveCorrect_per100km - avg_tear.tgp), (edz.NrBrakes_per100km -avg_tear.nb),
                (edz.NrHarshAcceleration_per100km - avg_tear.nha), VehicleID FROM export_data_zf edz, avg_tear GROUP BY VehicleID;"""
        with self.engine.connect() as con:
            rs = con.execute(sql)
        result_array = []
        if rs.rowcount > 0:
            for row in rs:
                price = row[0] + row[1] * (sum(row[2:-1]) / 10)
                result_array.append([row[-1], price])
        return result_array

    def execute_query_selection(self, query):
        with self.engine.connect() as con:
            rs = con.execute(query)
        result_array = []
        print(rs.rowcount)
        if rs.rowcount > 0:
            for row in rs:
                result_array.append(row)
        return result_array

    def load_avg_transportation_time_per_driver(self):
        sql= """SELECT AVG(TimeDriving / TotalDistance) as avg_driver_time, DriverID FROM export_data_zf
GROUP BY DriverID ORDER BY avg_driver_time;"""
        return self.execute_query_selection(sql)

    def load_time_until_breakdown(self):
        sql = """SELECT SUM(TotalDistance) as lifetime_span, VehicleID FROM export_data_zf GROUP BY VehicleID ORDER BY lifetime_span"""
        return self.execute_query_selection(sql)

    def load_co2_emission_by_driver(self):
        sql = """SELECT (2.56 * (TotalFuel / TotalDistance)) as co2_per_km, DriverID FROM export_data_zf
GROUP BY DriverID ORDER BY co2_per_km;"""
        return self.execute_query_selection(sql)

    def get_suitable_drivers(self, distance, time_limit):
        sql = "SELECT "
        return

