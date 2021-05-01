import csv

with open('data.csv') as f:
    a = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

print(a[0])
