from main import pred_ci
from baseClass.baseMysql import MysqlConn

mc = MysqlConn("localhost", "root", "root", "jikong", "utf8")
for index, row in pred_ci.iterrows():
    print(index, row)
sql = '''insert into ifd_forecast_cal(CAL_YEAR, CAL_MONTH, QUARTER_DATE, MAX_FORECAST_COUNT, MIN_FORECAST_COUNT) 
            values()
    
    '''
