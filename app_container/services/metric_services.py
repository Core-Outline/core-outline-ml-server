import pandas as pd
import numpy as np
import copy
from datetime import datetime, timedelta
from app_container.repositories.pandas import convert_dict_to_df, convert_df_to_dict
from config.app_configs import time_units, date_format, customer_segments
from app_container.scripts.customer import createRFMTable, MRR_Class
from app_container.scripts.forecast import make_forecast


class MetricService():
    def __init__(self) -> None:
        pass

    def recurringRevenue(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date", metric['amount_column']: "amount"})
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).sum()
        df = df.reset_index()

        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        return convert_df_to_dict(df)

    def lifetimeValue(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['identifier_column']: "identifier",
                     metric['amount_column']: "amount"}
        )
        df.groupby('identifier').amout.sum()
        df = df.reset_index()
        return convert_df_to_dict(df)

    def customerSegmentation(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.dropna()
        RFM_Segment = createRFMTable(
            df=df, name_col=metric['name_column'], date_col=metric['date_column'], amount_col=metric['amount_column'])
        customers = [
            i for i in RFM_Segment[metric['name_column']].value_counts().index]

        for customer in customers:
            data = metric['data'].copy()
            print(customer)
            indices = [i for i, name in enumerate(
                metric['data'][metric['name_column']]) if name == customer]
            for key in data.keys():
                data[key] = [data[key][i] for i in indices]
            cust_df = convert_dict_to_df(data)
            cust_df = cust_df.rename(
                columns={metric['date_column']: "date", metric['amount_column']: "amount"})
            cust_df.groupby("date").amount.sum().reset_index()
            cust_df['date'] = [datetime.strptime(dt, date_format)
                               for dt in cust_df['date']]
            cust_df['date'] = pd.to_datetime(cust_df['date'])
            cust_df = cust_df.set_index('date')
            cust_df = cust_df.amount.resample(
                time_units[metric['time_units']]).mean()
            cust_df = cust_df.reset_index()

            cust_df['date'] = [datetime.strptime(np.datetime_as_string(
                dt, unit='D'), '%Y-%m-%d') for dt in cust_df['date'].values]
            cust_df['date'] = cust_df['date'].astype("str")

            RFM_Segment.loc[RFM_Segment[metric['name_column']]
                            == customer, 'MRR'] = cust_df['amount'].mean()

            quantiles = RFM_Segment['MRR'].quantile(
                q=[0.25, 0.5, 0.75]).to_dict()
            RFM_Segment['MRR']
            RFM_Segment["MRR_Quartile"] = RFM_Segment['MRR'].apply(
                MRR_Class, args=("MRR", quantiles,))

        if ('focus_segment' in metric.keys()):
            reference = customer_segments[metric['focus_segment']]['reference']
            value = customer_segments[metric['focus_segment']]['value']
            RFM_Segment = RFM_Segment.loc[RFM_Segment[reference] == value]
        return convert_df_to_dict(RFM_Segment)

    def expenses(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date",
                     metric['amount_column']: "amount"}
        )
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).sum()
        df = df.reset_index()

        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        return convert_df_to_dict(df)

    def revenueGrowthRate(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date",
                     metric['amount_column']: "amount"}
        )
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).sum()
        df = df.reset_index()
        df = df.sort_values('date')
        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        df = df.loc[df['amount'] > 0]
        valueGrowth = []
        percentageGrowth = []
        amount = df['amount'].values
        # print(amount)
        for i in range(len(amount)):
            if (i == 0):
                continue
            print("--------------------------------->",
                  amount[i] - amount[i-1])
            valueGrowth.append(amount[i] -
                               amount[i-1])
            percentageGrowth.append(
                ((amount[i] - amount[i-1]) / amount[i-1])*100)
        df = pd.DataFrame()
        df['RevenueGrowth'] = valueGrowth
        df['PercentageRevenueGrowth'] = percentageGrowth

        return convert_df_to_dict(df)

    def revenuePerProduct(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={
                metric['amount_column']: "amount",
                metric['product_column']: "product"}
        )
        df = df[['amount', 'product']]
        df = df.groupby("product").amount.sum().reset_index()
        return convert_df_to_dict(df)

    def totalRevenue(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['amount_column']: "amount"}
        )
        df = df[['amount']]
        totalRevenue = sum(df['amount'].values)
        return {totalRevenue}

    def growthRate(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date",
                     metric['amount_column']: "amount"}
        )
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).sum()
        df = df.reset_index()
        df = df.sort_values('date')
        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        if (len(df) <= 1):
            return {'growth_rate': 0, 'average_growth_rate': 0}
        growthRate = (df['amount'].values[-1] - df['amount'].values[-2]
                      )*100 / (df['amount'].values[len(df)-2])
        averageGrowthRate = (
            (df['amount'].values[len(df)-1] - df['amount'].values[0]) / len(df)) - 1
        return {
            'growth_rate': growthRate if (df['amount'].values[len(df)-2]) > 0 else float('inf'),
            'average_growth_rate': averageGrowthRate
        }

    def contractionRecurringRevenue(self, metric):
        data = self.recurringRevenue(metric=metric)
        df = convert_dict_to_df(data)

    def growthPeriod(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date",
                     metric['amount_column']: "amount"}
        )
        df.groupby("date").amount.sum().reset_index()
        df['date'] = [datetime.strptime(dt, date_format)
                      for dt in df['date']]
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.amount.resample(time_units[metric['time_units']]).sum()
        df = df.reset_index()
        df = df.sort_values('date', ascending=False)
        df['date'] = [datetime.strptime(np.datetime_as_string(
            dt, unit='D'), '%Y-%m-%d') for dt in df['date'].values]
        df['date'] = df['date'].astype("str")
        curr = df['amount'].values[0]

        for amt, dt in zip(df['amount'].values[1:], df['date'].values[1:]):
            if (amt > curr):
                return {"growth_period": str(((df['date'].values[0] - dt).astype('timedelta64[D]')))}
            else:
                curr = amt

        return {"growth_period": str(((df['date'].values[0] - df['date']).astype('timedelta64[D]')))}

    def forecast(self, metric):
        df = convert_dict_to_df(metric['data'])
        df = df.rename(
            columns={metric['date_column']: "date",
                     metric['amount_column']: "amount"}
        )
        df = df[['date', 'amount']]
        df['date'] = pd.DatetimeIndex(df['date'])
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values("date", ascending=True)
        df = df.set_index('date')
        df = make_forecast(df, metric['steps'])
        df.to_csv("2.csv")
        return convert_df_to_dict(df)
