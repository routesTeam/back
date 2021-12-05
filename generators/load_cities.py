import csv

with open('geo_objects.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Город'], row['lat'], row['lng'])