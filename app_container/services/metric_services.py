import pandas as pd
import numpy as np
from datetime import datetime
from app_container.repositories.pandas import convert_dict_to_df, convert_df_to_dict
from config.app_configs import time_units, date_format


class MetricService():
    def __init__(self) -> None:
        pass

    def recurringRevenue(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.dropna()
        df = df.rename(
            columns={metric['date_column']: "date", metric['amount_column']: "amount"})
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).mean()
        df = df.reset_index()

        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        return convert_df_to_dict(df)

    def lifetimeValue(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.dropna()
        df = df.rename(
            columns={metric['identifier_column']: "identifier",
                     metric['amount_column']: "amount"}
        )
        df.groupby('identifier').amout.sum()
        df = df.reset_index()
        return convert_df_to_dict(df)
