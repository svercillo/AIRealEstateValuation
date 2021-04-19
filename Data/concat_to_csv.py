import json


class DynamoModel:

	def __init__(self):
		db = boto3.resource('dynamodb')
        self.table = db.Table('AIPropertyData')

    def insert_item(self, item):
        
        
		self.table.put_item(
		Item ={'address': item['address'],
			'longitude' : item['longitude'],
			'latitude' : item['latitude'],
			"data" : item
		})


db = DynamoModel()
lines = "" 

for i in range(1, 2):
    try:
        f = open(f"data{i}.txt", "r", encoding="utf8")
        lines  += f.read()
    except:
        print(i)
        # raise
print(lines)


