import pandas as pd

# Select a data set
crime_data = pd.read_csv('datasets/Chicago_control_2018_2019.csv')  # treatment group
crime_data.dtypes

import datetime

cols_to_remove = list(crime_data)

# Separating the date column into month, day, year, and time columns
Months = []
Days   = []
Years  = []
Hours  = []
MDY    = []

for row in crime_data['Date']:
    d = datetime.datetime.strptime(row, '%m/%d/%Y %I:%M:%S %p')
    Months.append(d.month)
    Days.append(d.day)
    Years.append(d.year)
    Hours.append(d.hour)
    MDY.append(datetime.datetime.strptime(row[:10], '%m/%d/%Y'))
    
crime_data['Month'] = Months
crime_data['Day'] = Days
crime_data['Year_'] = Years
crime_data['Hour'] = Hours
crime_data['MDY'] = MDY

# 1-hot encoding for: Arrest, Location Description, Domestic, District, Primary Type
discrete_variables = "Arrest, Location Description, Domestic, District, Primary Type".split(", ")
print(discrete_variables)
for variable in discrete_variables:
    for dtype in crime_data[variable].dropna().unique():
        if (dtype != "nan"):
            crime_data[variable+"_"+str(dtype)]  = 1*(crime_data[variable] == dtype)

crime_data = crime_data.drop(columns=cols_to_remove)

# pre-intervention and post-intervention
pre_intervention_data = (crime_data[crime_data['Year_']==2018]).copy(deep=True)
intervention_data = (crime_data[crime_data['Year_']==2019]).copy(deep=True)
intervention_data = (intervention_data[intervention_data['Month']<5])

post_intervention_data = (crime_data[crime_data['Year_']==2019]).copy(deep=True)
post_intervention_data = (post_intervention_data[post_intervention_data['Month']>=5])
# post_intervention_data = (crime_data[crime_data['Year_']==2020 and (not(crime_data[crime_data['Month'] in [1,2,3,4]]))]).copy(deep=True)

print(intervention_data.dtypes)

# calculate rate of crime reports to arrest
pre_intervention_d_rates = {} 
intervention_d_rates = {}
post_intervention_d_rates = {}

for row in pre_intervention_data['MDY'].unique():
    pre_intervention_d_rates[row] = pre_intervention_data[pre_intervention_data['MDY']==row]['Arrest_True']

for row in intervention_data['MDY'].unique():
    intervention_d_rates[row] = intervention_data[intervention_data['MDY']==row]['Arrest_True']    

for row in post_intervention_data['MDY'].unique():
    post_intervention_d_rates[row] = post_intervention_data[post_intervention_data['MDY']==row]['Arrest_True']
#     if not(day in post_intervention_d_rates):
#         post_intervention_d_rates[day] = [post_intervention_data['Arrest_True'][k]]
#     else:
#         post_intervention_d_rates[day].append(post_intervention_data['Arrest_True'][k])

#print(post_intervention_data['Day'][0])

pre_intervention_rates = [] 
intervention_rates = []
post_intervention_rates = []

for i in pre_intervention_d_rates.keys():
    arrests = sum(pre_intervention_d_rates[i])
    reports = len(pre_intervention_d_rates[i])
    pre_intervention_rates.append(float(arrests)/float(reports))
    
for i in intervention_d_rates.keys():
    arrests = sum(intervention_d_rates[i])
    reports = len(intervention_d_rates[i])
    intervention_rates.append(float(arrests)/float(reports))
    
for i in post_intervention_d_rates.keys():
    arrests = sum(post_intervention_d_rates[i])
    reports = len(post_intervention_d_rates[i])
    post_intervention_rates.append(float(arrests)/float(reports))

import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

x1=pre_intervention_d_rates.keys()
y1=pre_intervention_rates
x2=intervention_d_rates.keys()
y2=intervention_rates
x3=post_intervention_d_rates.keys()
y3=post_intervention_rates

def mean(l):
    s = sum(float(x) for x in l)
    length = float(len(l))
    m = s/length
    print(m)
    return m

import csv
with open('clean_chicago_data_ctrl1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["date", "rate of arrest"])
    x1 = list(x1)
    for i in range(len(x1)):
        writer.writerow(["pre",str(x1[i])[:10],y1[i]])
    x2 = list(x2)
    for i in range(len(x2)):
        writer.writerow(["treatment",str(x2[i])[:10],y2[i]])
    x3 = list(x3)
    for i in range(len(x3)):
        writer.writerow(["post",str(x3[i])[:10],y3[i]])
    
