import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

Data = pd.read_csv(r'./usdjpy.csv')
Data['Datetime'] = pd.to_datetime(Data.time)
Data['Date'] = Data.Datetime.apply(lambda x:x.date())
Data['Time'] = Data.Datetime.apply(lambda x:x.time())
Data['Weekday'] = Data.Datetime.apply(lambda x:x.weekday())

DDD = []

for DT in Data.Date.drop_duplicates():
    Weekday = DT.weekday()
    if Weekday==0:
        DT_Start = datetime.datetime.combine(DT+timedelta(days=-1), datetime.time(0,0,0))
        DT_End = datetime.datetime.combine(DT, datetime.time(21,0,0))
        High = Data.high[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].max()
        Low = Data.low[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].min()
        DDD += [[DT,High,Low]]
    if Weekday==4:
        DT_Start = datetime.datetime.combine(DT+timedelta(days=-1), datetime.time(21,0,0))
        DT_End = datetime.datetime.combine(DT+timedelta(days=1), datetime.time(0,0,0))
        High = Data.high[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].max()
        Low = Data.low[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].min()
        DDD += [[DT,High,Low]]
    if (Weekday>=1)&(Weekday<=3):
        DT_Start = datetime.datetime.combine(DT+timedelta(days=-1), datetime.time(21,0,0))
        DT_End = datetime.datetime.combine(DT, datetime.time(21,0,0))
        High = Data.high[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].max()
        Low = Data.low[(Data.Datetime>=DT_Start)&(Data.Datetime<DT_End)].min()
        DDD += [[DT,High,Low]]

DF = pd.DataFrame(DDD,columns=['Date','High','Low'])
DF.to_csv(r'./usdjpy_data.csv',index=False)