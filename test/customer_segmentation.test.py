
import pandas as pd

metric = {
    "data": {
        "__v": [
            0,
            0,
            0
        ],
        "_id": [
            "62dd2ee89ed4e5198766955d",
            "62dd30cfd411030174895903",
            "62dd30cfd411030174895903"
        ],
        "amount": [
            300,
            180,
            120
        ],
        "user_id": [
            "1234",
            "1234",
            "1234"
        ],
        "date": [
            "30-06-2023",
            "22-02-2023",
            "22-02-2023"
        ]
    },
    "time_units": "monthly",
    "name_column": "_id",
    "date_column": "date",
    "amount_column": "amount",
    "metric_type": "customer_segmentation"
}

indices = [i for i, name in enumerate(
    metric['data'][metric['name_column']]) if name == "62dd30cfd411030174895903"]

print([metric['data'][metric['name_column']][i] for i in indices])
