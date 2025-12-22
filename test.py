import datetime
from datetime import timedelta
import numpy as np
import pandas as pd

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

P_SMA = [5,25,75]
Result = []
Columns = []

for i in range(DF.shape[0]):
    R_Sub = []
    for p in P_SMA:
        if i<(p-1):
            R_Sub += [None,None]
            if i == 0:
                Columns += ['High_'+str(p),'Low_'+str(p)]
        else:
            R_Sub += [np.round(DF.High[(i-p+1):(i+1)].mean(),4), np.round(DF.Low[(i-p+1):(i+1)].mean(),4)]

    Result += [R_Sub]

DF = pd.concat([DF,pd.DataFrame(Result,columns=Columns)],axis=1)

DF.to_csv(r'./usdjpy_sma.csv',index=False)