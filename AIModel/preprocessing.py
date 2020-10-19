import json
import csv
import pandas as pd
import numpy as np
# from sklearn.preprocessing import OneHotEncoder
# import immpo
# import requests 
# import tensorflow as tf
# import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
  host="dubhacks.cn4fnamhaswp.us-east-2.rds.amazonaws.com",
  user="dubhacks_admin",
  password="dubhacks",
  database="main"
)

mycursor = mydb.cursor()

# sql = "INSERT INTO `main`.`sold_properties` VALUES (%s, %s, %s, %s)"


# mycursor.execute(sql, val) 

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")

# with open('employee_file2.csv', mode='w', newline='') as csv_file:

file1 = open('../Data/data2.txt', 'r') 
Lines = file1.readlines() 

data = {}
data['sold_price'] =  []
data['address'] =  []
data['longitude'] = []
data['latitude'] = []
data['bedNum'] =  []
data['bathNum'] =  [] 
data['sqarefootage'] =  []
data['type'] =  []
data['style'] =  []

# prob not using this
# data['lotSize'] =  []

# elementary schools
data['firstEleDist'] = []
data['firstEleRat'] = []
data['secondEleDist'] = []
data['secondEleRat'] = [] 
data['thirdEleDist']= [] 
data['thirdEleRat'] = []

# secondary schools
data['firstSecDist'] = []
data['firstSecRat'] = []
data['secondSecDist'] = []
data['secondSecRat'] = []


# const array   
amenities = [ "Groceries",
    "Liquor Store",
    "Restaurants",
    "Coffee",
    "Bank",
    "Gas Station",
    "Health & Fitness",
    "Park",
    "Library",
    "Medical Care",
    "Pharmacy",
    "Mall",
    "Movie Theatre" ]

# fill amenities
for amenity in amenities:
    for i in range(0,3):
        data[amenity + " Distance" + str(i+1)] = []

count =0

for line in Lines:  
    count +=1 
    try:   
        row_entry = []
        # put this in a try catch for performance
        INVALID = False
        # convert each line of code to a json obj
        line = json.loads(line)
        
        
        # process sold price:
        sp = line['sold_price']
        
        #replace commas in price
        sp = sp.replace(",", "")

        # lot size, should don't think we should use this
        # data['lotSize'].append(line['Lot Size'])


        
        # # process bed nums
        s = line['bedNum']
        s.split('+')
        if len(s) > 1:
            line['bedNum'] = s[0]
            line['denNum'] = s[1]
        else:
            line['denNum'] = 0

        # process square footage
        s = line['sqarefootage']
        try:
            if s != 'n/a':
                if  '-' in s: 
                    arr = s.split("-")

                    s = str(int((int(arr[0]) + int(arr[1])) / 2) +1 )
                if '+' in s:
                    s = s[:-1]

            # else:
                # INVALID = True
                # throw error
        except: 
            print("square footage error")
            INVALID = True 



        line['sqarefootage'] = s
        data['sqarefootage'].append(s)


            





        # stop after 10 iterations
        if len(data['address']) >= 10:
            # ik dillon doesn't read these comments
            break

        line['long'] = line["longitude"]
        line['lat'] = line["latitude"]
        
        
        if not line['Amenities']:
            print("no amenities")
            INVALID = True
            # throw error

        switchD =  {0: 'firstEleDist', 1: 'secondEleDist', 
            2: 'thirdEleDist', 3: 'firstSecDist', 4: 'secondSecDist'} 

        switchR =  {0: 'firstEleRat', 1: 'secondEleRat', 
            2: 'thirdEleRat', 3: 'firstSecRat', 4: 'secondSecRat'} 


        for i in range(0,3):
            if line['Nearest Schools'][i]['type'] != "Elementary":            
                INVALID = True
                print("wrong number of schools")
                # throw error
            else:
                key1 ="es_" + str(i+1)
                key2 = key1 + "_rat"
                key1 += "_dist"
                line[key1] = line['Nearest Schools'][i]['distance'][:-3]
                line[key2] = line['Nearest Schools'][i]['rating']
                #data[switchD[i]].append(line['Nearest Schools'][i]['distance'])
                #data[switchR[i]].append(line['Nearest Schools'][i]['rating'])
            
        for i in range(3, 6):
            if line['Nearest Schools'][i]['type'] != "Secondary":
                INVALID = True
                print("wrong number of hschools")

                # throw error
            else:
                key1 ="hs_" + str(i-2)
                key2 = key1 + "_rat"
                key1 += "_dist"
                line[key1] = line['Nearest Schools'][i]['distance'][:-3]
                line[key2] = line['Nearest Schools'][i]['rating']
                # data[switchD[i]].append(line['Nearest Schools'][i]['distance'])
                # data[switchR[i]].append(line['Nearest Schools'][i]['rating'])

        ordered_list = ['address', 'sold_price', 'bedNum', 'denNum', 'bathNum', 'sqarefootage', 'soldOn', 'Type', 'Style', 
        'long', 'lat', 'pageNum', 'iterationNum', 'weblink', 'es_1_dist', 'es_1_rat', 'es_2_dist', 'es_2_rat', 'es_3_dist', 'es_3_rat',
        'hs_1_dist', 'hs_1_rat','hs_2_dist', 'hs_2_rat','hs_3_dist', 'hs_3_rat']

        abbrev = { 
        "Groceries" : "g",
        "Liquor Store" : "ls",
        "Restaurants" : "r",
        "Coffee" : "c",
        "Bank": "b",
        "Gas Station" : "gs",
        "Health & Fitness" : "hf",
        "Park" : "p",
        "Library" : "l",
        "Medical Care" : "mc",
        "Pharmacy" : "p", 
        "Mall" : "m",
        "Movie Theatre" : "mt"
        }
        for i in range(0,3):
            for amenity in amenities:
                k = abbrev[amenity] + "_" + str(i+1) + "_dist"
                val = line['Amenities'][amenity][i]
                line[k] = val[:-3]


                ordered_list.append(k)
                
                # data[amenity + " Distance" + str(i+1)].append(line['Amenities'][amenity][i])
    
        line['sold_price'] =int(line['sold_price'].replace(',', ''))
            

        # print (ordered_list)
        
        line.pop('longitude', None)
        line.pop('latitude', None)
        line.pop('Maintenance Fees', None)
        line.pop('Lease Term', None)
        line.pop('Possession', None)
        line.pop('Days on Site', None)
        line.pop('Walk Score', None)
        line.pop('All Inclusive', None)
        line.pop('Amenities', None)
        line.pop('Nearest Schools', None)
        line.pop('Lot Size', None)
        line.pop('Taxes', None)
        line.pop("Pets", None)
        line.pop('Age', None)
        line.pop('Size', None)



            
        index_map = {v: i for i, v in enumerate(ordered_list)}
        pairs =sorted(line.items(), key=lambda pair: index_map[pair[0]])
        # print(pairs )
        
        # print(line)

        for i in range(0, len(pairs)):
            row_entry.append(pairs[i][1])    
        print(row_entry)
        print(len(row_entry))


        if INVALID:
            print("Invalid row")
            break
            continue

        # row_entry.append(line['address'])
        # row_entry.append(int(sp)) # cast price to int
        # row_entry.append(line['bedNum'])
        # row_entry.append(line['bathNum'])    
        # row_entry.append(line['longitude'])
        # row_entry.append(line['latitude'])
        # row_entry.append(line['Type'])
        # row_entry.append(line['Style'])

        print(pairs)
        mycursor = mydb.cursor()

        sql = "INSERT INTO `main`.`sold_properties` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


        mycursor.execute(sql, row_entry) 

        mydb.commit()

    except:
        print("Invalid row sdfsdfsdfsdf " + str(count))
        break
        continue




fieldnames = ['sold_price',
    'address'
    'longitude'
    'latitude',
    'bedNum'
    'bathNum'
    'sqarefootage',
    'type'
    'style'
    'longitude',

    # schools 
    'firstEleDist'
    'firstEleRat'
    'secondEleDist',
    'secondEleRat'
    'thirdEleDist'
    'thirdEleRat',
    'firstSecDist'
    'firstSecRat'
    'secondSecDist',
    'secondSecRat'
    
    # amenities 
    'Groceries Distance1'
    'Groceries Distance2'
    'Groceries Distance3'
    'Liquor Store Distance1',
    'Liquor Store Distance2',
    'Liquor Store Distance3',
    'Restaurants Distance1'
    'Restaurants Distance2'
    'Restaurants Distance3'
    'Coffee Distance1'
    'Coffee Distance2'
    'Coffee Distance3'
    'Bank Distance1',
    'Bank Distance2',
    'Bank Distance3',
    'Gas Station Distance1',
    'Gas Station Distance2',
    'Gas Station Distance3',
    'Health & Fitness Distance1',
    'Health & Fitness Distance2',
    'Health & Fitness Distance3',
    'Park Distance1',
    'Park Distance2',
    'Park Distance3',
    'Library Distance1',
    'Library Distance2',
    'Library Distance3',
    'Medical Care Distance1',
    'Medical Care Distance2',
    'Medical Care Distance3',
    'Pharmacy Distance1',
    'Pharmacy Distance2',
    'Pharmacy Distance3',
    'Mall Distance1',
    'Mall Distance2',
    'Mall Distance3',
    'Movie Theatre Distance1',
    'Movie Theatre Distance2',
    'Movie Theatre Distance3']

# writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
# for row in data: 
#     writer.writerow(row)

# continue preprocessing
# print(data['firstEleDist'])



    

    # df = pd.DataFrame(data,columns=['sold_price', 'address', 
    #     'bedNum', 'bathNum','sqft', 
    #     'typeOfProperty', 'style', 'lotSize',
    #     'amenities', 'schools']) 



    # writer.writeheader()
    # writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
    # writer.writerow({'emp_name': 'Erica Meyers', 'dept': 'IT', 'birth_month': 'March'})



    # print(data[0].mean())







# # function used to get long and lat from address 
# def forward_geocode(address, city='Toronto', state = 'Ontario', country = 'Canada'):
#     # api key
#     apiKey = '3c9e96b06652f7'

#     # urlify address and add province, country
#     urledAddress = address.replace(' ', '%20') + '%20' + city + '%20' + state + '%20' + country

#     # request json continaing coordinates
#     url = 'https://us1.locationiq.com/v1/search.php?key=' + apiKey + '&q=' + urledAddress + 'newAd&format=json'
#     lon = -1
#     lat = -1
#     try:
#         response = requests.get(url)
#         data = response.json()[0]
#         lon = data['lon']
#         lat = data['lat']
        
#     except:
#         # indicates that an error in this api occured
#         return {'error' : 'API',
#                 'address' : address}
    
#     return {'lon': lon, 'lat': lat, 'address': address}


# print (forward_geocode("3 Baird Avenue"))
# print (forward_geocode("210 Oakridge Drive'"))
# print (forward_geocode("4 Strathearn Boulevard"))
# print (forward_geocode('#2009 - 3 Rowntree Road'))