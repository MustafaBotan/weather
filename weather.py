import matplotlib as mpl
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure
import numpy as np 
import pandas as pd
def extreme_temperature_plot(year1, year2):
    
    #Weather stations in Denmark recorded high and low temp per day from 1950 to 2021
    df = pd.read_csv('2573058.csv')
    dfm=pd.read_csv('2573193.csv')

    df['TMAX']=(df['TMAX']-32)*(5/9)
    df['TAVG']=(df['TAVG']-32)*(5/9)
    df['TMIN']=(df['TMIN']-32)*(5/9)

    df=pd.concat([df,dfm],keys='DATE')
    df['DATE']=pd.to_datetime(df['DATE'])
    df=df.reset_index()
    df=df[['NAME','DATE','TMAX','TMIN','TAVG']]
    
    dfmax=df.groupby('DATE').agg(np.max)[['TMAX']]
    dfmax.dropna(inplace=True)
    dfmin=df.groupby('DATE').agg(np.min)[['TMIN']]
    dfmin.dropna(inplace=True)
    dfmin.reset_index(inplace=True)
    dfmax.reset_index(inplace=True)

    dfmax2015=dfmax[(dfmax['DATE'].dt.year>=year1)]
    dfmax=dfmax[np.invert(dfmax['DATE'].dt.year>=year1)]
    dfmax=dfmax[np.invert(dfmax['DATE'].dt.year<year2)]
    dfmin2015=dfmin[(dfmin['DATE'].dt.year>=year1)]
    dfmin=dfmin[np.invert(dfmin['DATE'].dt.year>=year1)]
    dfmin=dfmin[np.invert(dfmin['DATE'].dt.year<year2)]

    dfmax['date']=dfmax['DATE'].dt.strftime('%m/%d')
    dfmax['month']=dfmax['DATE'].dt.month
    dfmax['day']=dfmax['DATE'].dt.day
    dfmax2015['month']=dfmax2015['DATE'].dt.month
    dfmax2015['day']=dfmax2015['DATE'].dt.day
    dfmax2015=dfmax2015.groupby(['month','day']).agg(np.max)

    dfmax=dfmax.groupby(['month','day']).agg(np.max)
    dfmax.drop(index=(2,29),inplace=True)
    dfmax['2015']=dfmax2015['TMAX']

    dfmin['date']=dfmin['DATE'].dt.strftime('%m/%d')
    dfmin['month']=dfmin['DATE'].dt.month
    dfmin['day']=dfmin['DATE'].dt.day
    dfmin2015['month']=dfmin2015['DATE'].dt.month
    dfmin2015['day']=dfmin2015['DATE'].dt.day
    dfmin2015=dfmin2015.groupby(['month','day']).agg(np.min)
    dfmin=dfmin.groupby(['month','day']).agg(np.min) #lowest of all days
    dfmin.drop(index=(2,29),inplace=True)
    dfmin2015.drop(index=(2,29),inplace=True)
    dfmin['2015']=dfmin2015['TMIN'] #lowest 2015

    dfmax.reset_index(inplace=True)
    dfmax2015t=dfmax[dfmax['TMAX']<dfmax['2015']][['DATE','2015']]
    dfmax2015t['DATE']=dfmax2015t['DATE'].map(lambda i: i.replace(year=year2))
    
    dfmin.reset_index(inplace=True)
    dfmin2015t=dfmin[dfmin['TMIN']>dfmin['2015']][['DATE','2015']]
    dfmin['m']=dfmin['DATE'].map(lambda i: i.strftime("%b"))

    
    #plot
    import matplotlib.dates as mdates
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(dfmin['DATE'],dfmax['TMAX'],'-',c='blue',alpha=0.5)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    months = mdates.MonthLocator()
    ax.xaxis.set_major_locator(months)
    plt.scatter(dfmax2015t['DATE'],dfmax2015t['2015'],c='red',s=15)
    plt.scatter(dfmin2015t['DATE'],dfmin2015t['2015'],c='red',s=15)
    plt.locator_params(axis='x', nbins=12)
    plt.xlabel('Month')
    plt.ylabel('Temperature ($c$)')
    plt.title('Record Breaking Temperatures from {year} Denmark'.format(year=year1))
    # add a legend with legend entries (because we didn't have labels when we plotted the data series)
    plt.legend(['Extreme {yearF}-{yearL}'.format(yearL=year1-1,yearF=year2), 'From {yearL}'.format(yearL=year1)], loc = 'lower right', frameon=False)
    plt.plot(dfmin['DATE'],dfmin['TMIN'],'-',c='blue',alpha=0.5)
    plt.gca().fill_between(dfmin['DATE'], 
                        dfmax['TMAX'], dfmin['TMIN'], 
                        facecolor='blue', 
                        alpha=0.25, where=dfmin['DATE'])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    return plt.show()
#Function requires two years between 2021 and 1950
extreme_temperature_plot(2010,1975)
