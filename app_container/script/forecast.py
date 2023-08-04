import pandas as pd
import itertools
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA, ARIMAResults
import warnings
warnings.filterwarnings('ignore')

def make_forecast(df, steps):
    p=d=q = range(0,2)
    pdq = list(itertools.product(p,d,q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq] 
    model = sm.tsa.statespace.SARIMAX(
        df,  
        order=pdq[0], 
        seasonal_order= seasonal_pdq[0], 
        enforce_invertibility=False
    )
    model = model.fit()
    minAIC, minBIC, minHQIC = model.aic, model.bic, model.hqic

    best_pdq = None
    best_seasonal_pqd = None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                model = sm.tsa.statespace.SARIMAX(df, order=param, seasonal_order = param_seasonal, enforce_invertibility= False)
                model = model.fit()
                if(model.aic < minAIC):
                    minAIC = model.aic
                    minBIC = model.bic
                    minHQIC = model.hqic
                    best_pdq = param
                    best_seasonal_pqd = param_seasonal
            except Exception as e:
                continue
    
    model = sm.tsa.statespace.SARIMAX(df, order=best_pdq, seasonal_order = best_seasonal_pqd, enforce_invertibility= False)
    model = model.fit()

    forecast = model.get_forecast(steps=steps)
    forecast_df = forecast.conf_int()
    forecast_df['amount'] = (forecast_df[f'upper amount'] + forecast_df['lower amount'])/2 
    return forecast_df
