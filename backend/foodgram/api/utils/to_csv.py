import csv

def data_to_csv(data, filename):
    with open(filename, 'w') as file:
        w = csv.writer(file)
        w.writerow(data[0].keys())
        for item in data:
            w.writerow(item.values())

