-- Reads the 2,000-row taxi sample. Swap the file name to test the faulted copy.
select * from read_csv_auto('{{ var("trips_file", "../trips_sample.csv") }}')
