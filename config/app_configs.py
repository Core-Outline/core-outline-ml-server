columns = {"name", "amount"}

time_units = {
    "monthly": "M",
    "weekly": "W",
    "yearly": "Y"
}

date_format = "%d-%m-%Y"


customer_segments = {
    "best_customers": {
        "reference": 'RFMClass',
        "value": 444,
    },
    "churning_customers": {
        "reference": 'R_Quartile',
        "value": 2,
    },
    "lost_customers": {
        "reference": 'RFMClass',
        "value": 111,
    },
    "loyal_customers": {
        "reference": 'F_Quartile',
        "value": 3,
    },
    "high_mrr": {
        "reference": 'MRR_Quartile',
        "value": 4,
    },
    "low_mrr": {
        "reference": 'MRR_Quartile',
        "value": 1,
    },

}
