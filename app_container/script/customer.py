from statistics import quantiles
import pandas as pd
from datetime import date, datetime


def getUserRFMScore(recency, frequency, monetary_value, df, service):
    RFM_Segment = createRFMTable(df)
    R_Quartile = R_Class(recency, "recency", quantiles)
    F_Quartile = FM_Class(frequency, "frequency", quantiles)
    M_Quartile = FM_Class(monetary_value, "monetary_value", quantiles)

    RFMClass = str(R_Quartile) + str(F_Quartile) + str(M_Quartile)

    RFMScore = R_Quartile + F_Quartile + M_Quartile

    # Score_cut = pd.qcut(RFM_Segment["RFMScore"].unique().rank(pct=True), q=4, labels=Level)
    # RFM_Segment["Level"] = Score_cut
    # print(RFM_Segment['Level'].values.unique)

    # return determineCuts(RFMScore,RFM_Segment), RFM_Segment
    return RFMScore, RFMClass


def determineCuts(score, df):
    lower_advanced = df[df['Level'] == "Advanced"].sort_values(
        by='RFMScore', ascending=True)["RFMScore"].min()
    lower_standard = df[df['Level'] == "Standard"].sort_values(
        by='RFMScore', ascending=True)["RFMScore"].min()
    lower_basic = df[df['Level'] == "Basic"].sort_values(
        by='RFMScore', ascending=True)["RFMScore"].min()

    if (score > lower_advanced):
        return "Advanced"
    if (score > lower_standard):
        return "Standard"
    if (score > lower_basic):
        return "Basic"
    else:
        return "Subpar"


def createRFMTable(df, name_col, amount_col, date_col):
    df = df[[name_col, amount_col, date_col]]
    df[date_col] = pd.to_datetime(df[date_col])
    df["recency"] = df[date_col]
    latest = df.sort_values(by='recency', ascending=False)['recency']
    today = datetime.now()
    RFM_table = pd.DataFrame()
    RFM_table = df.groupby(name_col).agg({"recency": lambda x: (today - x.max()).days, date_col: lambda x: len(x.unique()),
                                          amount_col: lambda x: x.sum()})
    RFM_table = RFM_table.reset_index()
    RFM_table.rename(columns={date_col: "frequency",
                     amount_col: "monetary_value"}, inplace=True)
    quantiles = RFM_table.quantile(q=[0.25, 0.5, 0.75]).to_dict()

    RFM_Segment = RFM_table.copy()

    RFM_Segment["R_Quartile"] = RFM_Segment["recency"].apply(
        R_Class, args=("recency", quantiles,))

    RFM_Segment["F_Quartile"] = RFM_Segment["frequency"].apply(
        FM_Class, args=("frequency", quantiles,))

    RFM_Segment["M_Quartile"] = RFM_Segment['monetary_value'].apply(
        FM_Class, args=("monetary_value", quantiles,))

    RFM_Segment["RFMClass"] = RFM_Segment.R_Quartile.map(str) \
        + RFM_Segment.F_Quartile.map(str) \
        + RFM_Segment.M_Quartile.map(str)
    RFM_Segment['RFMScore'] = RFM_Segment[[
        'R_Quartile', 'F_Quartile', 'M_Quartile']].sum(axis=1)

    return RFM_Segment


def createRRtable(df, name_col, amount_col, date_col):
    df = df[[name_col, amount_col, date_col]]
    df[date_col] = pd.to_datetime(df[date_col])


def R_Class(x, p, d):

    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.5]:
        return 3
    elif x <= d[p][0.75]:
        return 2
    else:
        return 1


def FM_Class(x, p, d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.5]:
        return 2
    elif x <= d[p][0.75]:
        return 3
    else:
        return 4


def MRR_Class(x, p, d):
    print(x)
    print(p)
    print(d)
    if x <= d[0.25]:
        return 1
    elif x <= d[0.5]:
        return 2
    elif x <= d[0.75]:
        return 3
    else:
        return 4

# Some comment


def displayAccLevels(df):
    acc_df = df["acc_level"].value_counts()
    labels = acc_df.index
    values = acc_df.values


def displayDistribution(df):
    df = df["monetary_value"]


def bestCustomers(df):
    df_best = df[df["RFMClass"] == "444"].sort_values(
        "monetary_value", ascending=False)
    return df_best


def churningCustomers(df):
    df_churn = df[df['R_Quartile'] <= 2].sort_values(
        "monetary_value", ascending=False)
    df_churn


def lostCustomers(df):
    df_lost = df[df['RFMClass'] == '111'].sort_values(
        'recency', ascending=False)
    return df_lost


def loyalCustomers(df):
    df_loyal = df[df["F_Quartile"] >= 3].sort_values(
        "monetary_value", ascending=False).head(10)
    df_loyal = df_loyal[df_loyal["R_Quartile"] >= 3].sort_values(
        "monetary_value", ascending=False)

    return df_loyal
