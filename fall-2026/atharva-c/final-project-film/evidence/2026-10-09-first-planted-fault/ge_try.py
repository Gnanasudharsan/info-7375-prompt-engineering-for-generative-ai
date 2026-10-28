import great_expectations as gx

context = gx.get_context()
batch = context.data_sources.pandas_default.read_csv("trips_sample.csv")
print(batch.validate(gx.expectations.ExpectColumnValuesToNotBeNull(column="passenger_count")))
