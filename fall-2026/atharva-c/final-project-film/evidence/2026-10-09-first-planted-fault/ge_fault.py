import great_expectations as gx
import pandas as pd

# Plant one known fault: blank out passenger_count in 50 rows.
df = pd.read_csv("trips_sample.csv")
df.loc[df.sample(n=50, random_state=7).index, "passenger_count"] = None
df.to_csv("trips_faulted.csv", index=False)

context = gx.get_context()
check = gx.expectations.ExpectColumnValuesToNotBeNull(column="passenger_count")
for name in ["trips_sample.csv", "trips_faulted.csv"]:
    batch = context.data_sources.pandas_default.read_csv(name)
    r = batch.validate(check)
    print(f"{name}: success={r.success} unexpected_count={r.result['unexpected_count']}")
