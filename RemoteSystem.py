from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import csv
id1=[]
temperature=[]
humid=[]
airp=[]
alt=[]
slp=[]
lgt=[]
rain=[]
size=0
with open(r"C:\Users\Prakhar Bhatnagar\Desktop\feeds(1).csv") as f:
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        id1.append(row[1])
        temperature.append(row[2])
        humid.append(row[3])
        airp.append(row[4])
        alt.append(row[5])
        slp.append(row[6])
        lgt.append(row[8])
        rain.append(row[7])
        size=size+1
linear_mod=linear_model.LinearRegression()
id1=np.reshape(id1,(len(id1),1)).astype(np.float)
temperature=np.reshape(temperature,(len(temperature),1)).astype(np.float)
humid=np.reshape(humid,(len(humid),1)).astype(np.float)
airp=np.reshape(airp,(len(airp),1)).astype(np.float)
alt=np.reshape(alt,(len(alt),1)).astype(np.float)
slp=np.reshape(slp,(len(slp),1)).astype(np.float)
lgt=np.reshape(lgt,(len(lgt),1)).astype(np.float)
rain=np.reshape(rain,(len(rain),1)).astype(np.float)
val=int(input("enter the value at which the weather conditions are needed to be predcited : "))
#temp predict
linear_mod.fit(id1,temperature)
predicted_temperature=linear_mod.predict(size)
print("Temperature for the required readings in degree celsius")
print (predicted_temperature[0][0])
plt.scatter(val,predicted_temperature[0][0])
plt.xlabel("ID")
plt.ylabel("Temprature")
#plt.show()
sleep(60)
#humid predict
linear_mod.fit(id1,humid)
predicted_humid=linear_mod.predict(size)
print("Huimidity for the required readings in percentage")
print (predicted_humid[0][0])
plt.scatter(val,predicted_humid[0][0])
plt.xlabel("ID")
plt.ylabel("Humidity")
plt.show()
#airp prediction
linear_mod.fit(id1,airp)
predicted_airp=linear_mod.predict(size)
print("Air Pressure for the required readings in Pascal")
print (predicted_airp[0][0])
plt.scatter(val,predicted_airp[0][0])
plt.xlabel("ID")
plt.ylabel("Air pressure")
plt.show()
#lgt predict
plt.figure(4)
linear_mod.fit(id1,lgt)
predicted_lgt=linear_mod.predict(size)
print("Light Intensity for the required readings according to binary scale")
print (predicted_lgt[0][0])
plt.scatter(val,predicted_lgt[0][0])
plt.xlabel("ID")
plt.ylabel("Light")
plt.show()