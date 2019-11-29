from model.ArimaModel import ArimaModel
import data.handFootMouth as handFootMouth
import utils.util as util
from model.HoltWinterModel import HoltWintersModel
import pandas as pd
import numpy as np
from baseClass.baseMysql import MysqlConn


def format_pred(pred):
    pred['lower'] = pred.apply(lambda x: (x['lower Count'] + x['upper Count']) / 2, axis=1)
    pydata_array = pred.index.to_pydatetime()
    date_only_array = np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(pydata_array)
    pred.index = pd.Series(date_only_array)
    return pred


def save_data(pred):
    mc = MysqlConn("localhost", "root", "root", "jikong", "utf8")
    for index, row in pred.iterrows():
        date = index.split('-')
        sql = '''insert into ifd_forecast_cal(CAL_YEAR, CAL_MONTH, QUARTER_DATE, MAX_FORECAST_COUNT, MIN_FORECAST_COUNT)
                        values(%s, %s, %s, %s, %s)''' \
              % (date[0], date[1], index, int(row['upper Count']), int(row['lower']))
        mc.add(sql)


if __name__ == '__main__':
    # plot the trend pic
    # util.plot_trend(handFootMouth.hfm_train, handFootMouth.hfm_test)

    # create the model by arima
    arima = ArimaModel(handFootMouth.hfm_train, handFootMouth.hfm_test, (2, 1, 1), (2, 1, 1, 12))

    # validate the model
    # pred_static, pred_static_ci, mse_static = arima.static_validate()
    # pred_dynamic, pred_ci_dynamic, mse_dynamic = arima.dynamic_validate()

    # generate the forecast data
    pred_ci = arima.predict(2)
    pred_results = format_pred(pred_ci)

    # save the forecastdata to database
    save_data(pred_results)

    # create the model by HoltWinter
    # holt = HoltWintersModel(handFootMouth.hfm_train, handFootMouth.hfm_test, 2)
    # holt.plot_validate()
    # x = holt.predict(3)


