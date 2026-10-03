import random
import pandas as pd
from faker import Faker

fake = Faker("en_IN")
rows = [{
    "loan_id": i,
    "customer_name": fake.name(),
    "loan_amount": random.choice([50000, 100000, 250000, 500000, 1000000]),
    "interest_rate": round(random.uniform(8, 18), 2),
    "status": random.choice(["Approved", "approved", "REJECTED", "Disbursed", None]),
    "application_date": fake.date_between("-2y", "today"),
} for i in range(1, 5001)]

df = pd.DataFrame(rows)
df = pd.concat([df, df.sample(50)]).reset_index(drop=True)      # 50 duplicate rows
df.loc[df.sample(30).index, "loan_amount"] = -1                  # 30 invalid amounts
df.to_csv("data/loans_raw.csv", index=False)
print("Rows written:", len(df))