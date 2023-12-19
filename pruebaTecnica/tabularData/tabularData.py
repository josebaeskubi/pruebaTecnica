import pandas as pd

flightData = pd.read_csv('FlightData.csv')

print(flightData.info())
print(flightData.describe())

#Remove missing values
flightData.dropna(inplace=True)

#Remove duplicates
duplicate_rows = flightData.duplicated()
print("Number of duplicate rows:", duplicate_rows.sum())
flightData.drop_duplicates(inplace=True)

#Get fligt row where the altitude of the flight is the maximun
maxAltitudePos = flightData.iloc[[flightData['ALTITUDE'].idxmax()]]
print(maxAltitudePos)

