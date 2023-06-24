from datetime import date, datetime
import pandas as pd
date_format = "%d-%m-%Y"
time_units = {
    "monthly": "M",
    "weekly": "W",
    "yearly": "Y"
}

1688083200000000000
print(datetime.strptime("30-06-2023", date_format))
obj = {
    "data": {
        "__v": [
            0,
            0
        ],
        "_id": [
            "62dd2ee89ed4e5198766955d",
            "62dd30cfd411030174895903"
        ],
        "amount": [
            300,
            300
        ],
        "user_id": [
            "1234",
            "1234"
        ],
        "date": [
            date.today(),
            date.today()
        ]
    },
    "time_units": "monthly"
}
df = pd.DataFrame(obj["data"])
df = df.rename(columns={'date': "date", 'amount': "amount"})
df.groupby("date").amount.sum().reset_index()
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
df = df.amount.resample(time_units[obj['time_units']]).mean()
df = df.reset_index()
df['date'] = [d.strftime("%d-%m-%Y") for d in df['date']]
print(df.to_json(orient='records'))
