import pandas as pd
import json


def convert_dict_to_df(obj):
    return pd.DataFrame(obj)


def convert_df_to_dict(df):
    return json.loads(df.to_json(orient='records'))
