import json
import csv



# class DynamoModel:

#     def __init__(self):
#         db = boto3.resource('dynamodb')
#         self.table = db.Table('AIPropertyData')

#     def insert_item(self, item):


#         self.table.put_item(
#             Item ={'address': item['address'],
#                 'longitude' : item['longitude'],
#                 'latitude' : item['latitude'],
#                 "data" : item
#             })  


# db = DynamoModel()

lines = "" 

rows = []
for i in range(1, 450):
    try:
        with open(f"data{i}.txt", "r", encoding="utf8") as f:
            flines = f.readlines()
            for line in flines:
                lines += line
                data = json.loads(line)
                rows.append(data)
    except:
        print(f"page {i} failed")

with open('innovators.csv', 'w', newline='') as csv_f:
    writer = csv.writer(csv_f)
    writer.writerows(rows)
# print(lines)


