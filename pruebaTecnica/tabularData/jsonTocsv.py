import json
import pandas as pd

file = open('sample_tech_test.json').read()

data = json.loads(file)

fields = list(data.keys())[:3]

dict = {fields[0]:data[fields[0]], fields[1]:data[fields[1]], fields[2]:data[fields[2]]}

df = pd.DataFrame(dict) 

df.to_csv('FlightData.csv', index=False) 