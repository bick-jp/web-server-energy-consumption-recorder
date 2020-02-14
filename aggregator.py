#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import time
import datetime
import glob
import matplotlib.patches as mpatches


# In[2]:
def aggregate(path):

    #this assumes only 1 ina file and 1 selenium file in directory!!!
    testDirectoryName = path #must end with a /
    testDirectoryPath = "/home/pi/Desktop/web-server-energy-consumption-recorder/" + path + "/"
    fileList = glob.glob(testDirectoryPath  + "*.csv")

    print(testDirectoryPath)
    fileList


    # In[3]:


    inaFileName = [k for k in fileList if 'ina' in k]

    inaFileName[0]


    # In[4]:


    selFileName = [k for k in fileList if 'selenium' in k]

    selFileName[0]


    # In[5]:


    #For CSV files
    inaData = pd.read_csv(inaFileName[0]).fillna(0)


    # In[6]:


    print(inaData.shape)
    inaData.head()


    # In[7]:


    #add power
    type(inaData)


    # In[8]:


    inaData.insert(2, 'watts', (inaData.mA / 1000.0) * inaData.V, True)


    # In[9]:


    inaData.head()


    # In[10]:


    #averages per second

    inaLength = inaData.shape[0]
    inaStartTime = inaData.time[0]
    inaEndTime = inaData.time[inaData.shape[0]-1]
    inaTimePeriod = inaEndTime - inaStartTime
    dataPerSecond =inaLength/inaTimePeriod

    dataPerSecond


    # In[11]:


    averagedINA = pd.DataFrame(columns=['mA','V','watts','time'])

    for av in list(range(int(inaTimePeriod))):
        avmA= inaData.loc[(15*av):((15*av)+14)]['mA'].sum()/15
        avV = inaData.loc[(15*av):((15*av)+14)]['V'].sum()/15
        avWatts = inaData.loc[(15*av):((15*av)+14)]['watts'].sum()/15
        avTime = inaData.loc[(15*av):(15*av)]['time'][inaData.loc[(15*av):(15*av)]['time'].index[0]]
        averagedINA = averagedINA.append({'mA' : avmA , 'V' : avV, 'watts': avWatts,'time': avTime},ignore_index=True)

        


    # In[12]:


    print(averagedINA.shape)
    print(averagedINA.tail())


    # In[13]:


    seleniumData = pd.read_csv(selFileName[0]).fillna(0)


    # In[14]:


    print(seleniumData.shape)
    seleniumData.tail()


    # In[15]:


    seleniumData.task.loc[0]


    # In[16]:


    # get start and stop times

    testTimes = []

    currentRound = 0
    for getT in list(range(seleniumData.shape[0])):
        
        if 'start' in seleniumData.task.loc[getT]:
            roundTimes = [seleniumData.time.loc[getT]]
        elif 'stop' in seleniumData.task.loc[getT]:
            roundTimes.append(seleniumData.time.loc[getT])
            testTimes.append(roundTimes)
            
    testTimes


    # In[17]:


    #make new data frames with power data from only test durations

    dataFrameSplits = []

    #print(averagedINA)
    for splitTests in list(range(len(testTimes))):
        dataFrameSplits.append(averagedINA.loc[(averagedINA.loc[:,'time']>=(testTimes[splitTests][0])) & (averagedINA.loc[:,'time']<=testTimes[splitTests][1])])
        #print(dataFrameSplits[splitTests])
        #print(averagedINA.loc[(averagedINA.loc[:,'time']>=(testTimes[splitTests][0])) & (averagedINA.loc[:,'time']<=testTimes[splitTests][1])])
    print(len(dataFrameSplits))

    dataFrameSplits


    # In[18]:


    #get the max and mins for each test set

    for mX in list(range(len(dataFrameSplits))):
        print('------'+str(mX)+'------')
        print ('Max:')
        print (np.max(dataFrameSplits[mX].watts))
        print ('Min:')
        print (np.min(dataFrameSplits[mX].watts))
                


    # In[19]:


    #obviously this isn't automated...

    #large average peak
    lPeakAVG =(2.6139504000000002 + 2.596789200000001 + 2.5888593333333336 + 2.6099552000000004) * 0.25

    #small overall peak
    sPeakAVG =(2.294001466666667+2.293759333333334+2.2986020000000003+2.2974821333333337)* 0.25

    print("Large Peak AVG: " + str(lPeakAVG))
    print("Small Peak AVG: " + str(sPeakAVG))

    #peak differences
    print("AVG Peak Difference: " + str(lPeakAVG-sPeakAVG))


    # In[20]:



    #graph ina219 all data
    plt.scatter(x=inaData.loc[:,'time'], y=inaData.loc[:,'watts'], color='b')


    # In[21]:


    # graph all selenium data
    plt.scatter(x=seleniumData.loc[:,'time'], y=seleniumData.loc[:,'task'], color='b')


    # In[22]:


    fig, ax = plt.subplots(dpi=300)

    x = averagedINA.loc[:,'time']
    y = averagedINA.loc[:,'V']
    ax.plot(x,y)

    ax.set(xlabel='seconds', ylabel='volts',
           title='Server Activity')

    colors = ['r','y','b','g']
    for plotNum in list(range(len(dataFrameSplits))):
        ax.scatter(x=dataFrameSplits[plotNum].loc[:,'time'], y=dataFrameSplits[plotNum].loc[:,'V'], color=colors[plotNum%2])

    redLabel = mpatches.Patch(color='red', label='large')
    blueLabel = mpatches.Patch(color='blue', label='small')
    yellowLabel = mpatches.Patch(color='yellow', label='small')
    greenLabel = mpatches.Patch(color='green', label='small image')


    plt.legend(handles=[redLabel, yellowLabel])

    #ax.grid()
    pngName1 = testDirectoryPath +"voltage_"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName1)
    fig.savefig(pngName1)
    plt.show()


    # In[23]:


    fig, ax = plt.subplots(dpi=300)

    x = averagedINA.loc[:,'time']
    y = averagedINA.loc[:,'mA']
    ax.plot(x,y)

    ax.set(xlabel='seconds', ylabel='mA',
           title='Server Activity')

    colors = ['r','y','b','g']
    for plotNum in list(range(len(dataFrameSplits))):
        ax.scatter(x=dataFrameSplits[plotNum].loc[:,'time'], y=dataFrameSplits[plotNum].loc[:,'mA'], color=colors[plotNum%2])

    redLabel = mpatches.Patch(color='red', label='large')
    blueLabel = mpatches.Patch(color='blue', label='large image')
    yellowLabel = mpatches.Patch(color='yellow', label='small')
    greenLabel = mpatches.Patch(color='green', label='small image')

    plt.legend(handles=[redLabel, yellowLabel])

    #ax.grid()
    pngName1 = testDirectoryPath +"current_"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName1)
    fig.savefig(pngName1)
    plt.show()


    # In[24]:


    fig, ax = plt.subplots(dpi=300)

    x = averagedINA.loc[:,'time']
    y = averagedINA.loc[:,'watts']
    ax.plot(x,y)

    ax.set(xlabel='seconds', ylabel='watts',
           title='Server Activity')

    colors = ['r','y','b','g']
    for plotNum in list(range(len(dataFrameSplits))):
        ax.scatter(x=dataFrameSplits[plotNum].loc[:,'time'], y=dataFrameSplits[plotNum].loc[:,'watts'], color=colors[plotNum%2])

    redLabel = mpatches.Patch(color='red', label='large')
    blueLabel = mpatches.Patch(color='blue', label='large image')
    yellowLabel = mpatches.Patch(color='yellow', label='small')
    greenLabel = mpatches.Patch(color='green', label='small image')

    plt.legend(handles=[redLabel, yellowLabel])

    #ax.grid()
    pngName1 = testDirectoryPath +"watts_"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName1)
    fig.savefig(pngName1)
    plt.show()


    # In[25]:


    overlayData = dataFrameSplits
    overlayData[2]


    # In[26]:


    list(range(len(dataFrameSplits)))


    # In[27]:


    overlayData[0]


    # In[28]:


    for overlays in list(range(len(dataFrameSplits))):
        overlayData[overlays].insert(4, 'scaled', overlayData[overlays].time - overlayData[overlays].time[overlayData[overlays].time.index[0]], True)

    #overlayData


    # In[29]:


    fig, ax = plt.subplots(dpi=300)
    '''
    x = overlayD1.loc[:,'scaled']
    y = overlayD1.loc[:,'watts']
    ax.plot(x,y, color='r')

    ax.set(xlabel='time', ylabel='watts',
           title='Overlayed Server Activity')

    '''

    colors = ['r','y','b','g']
    for plotNum in list(range(len(overlayData))):
        ax.plot(overlayData[plotNum].loc[:,'scaled'], overlayData[plotNum].loc[:,'watts'], color=colors[plotNum%2])

    ax.set(xlabel='seconds', ylabel='watts',
           title='Overlayed Server Activity')

    redLabel = mpatches.Patch(color='red', label='large')
    blueLabel = mpatches.Patch(color='blue', label='large image')
    yellowLabel = mpatches.Patch(color='yellow', label='small')
    greenLabel = mpatches.Patch(color='green', label='small image')

    plt.legend(handles=[redLabel, yellowLabel])

    #ax.grid()
    pngName2 = testDirectoryPath +"aggregator_overlay-"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName2)
    fig.savefig(pngName2)
    plt.show()


    """
    #FORGET ABOUT AVERAGE FOR NOW!!!
    # In[30]:


    #averages
    averagedData = dataFrameSplits


    # In[31]:


    averagedData[0].shape[0]


    # In[32]:


    #find the shortest length of the data sets
    dataLengths = []

    for mins in list(range(len(overlayData))):
        dataLengths.append(averagedData[mins].shape[0])
    minData = min(dataLengths)

    minData


    # In[33]:


    averagedData[2].watts.loc[averagedData[2].index[6]]


    # In[34]:


    averagedData[0].head()


    # In[35]:


    newAveragedDataL = []
    newAveragedDataS = []

    #loop through all data points
    for sumum in list(range(minData)):
        #add up that data point for each set
        summedUp = []
        for getVal in list(range(int(len(averagedData)/2))):
            summedUp.append(averagedData[(getVal*2)].watts.loc[averagedData[(getVal*2)].index[sumum]])
        newAveragedDataL.append(np.mean(summedUp))
        
        summedUp = []
        for getVal in list(range(int(len(averagedData)/2))):
            summedUp.append(averagedData[(getVal*2)+1].watts.loc[averagedData[(getVal*2)+1].index[sumum]])
        newAveragedDataS.append(np.mean(summedUp))
        
    print(newAveragedDataL)
    print(newAveragedDataS)
        


    # In[38]:


    # make a new data frame


    someAveragedData = {'large' : newAveragedDataL ,'small' : newAveragedDataS , 'time': averagedData[4].loc[:,'scaled']}

    averagedDF = pd.DataFrame(someAveragedData)


    #get subsection
    averagedDF = averagedDF.loc[(averagedDF.loc[:,'time']>= 4)  & (averagedDF.loc[:,'time'] <= 24)]

    avgLarge = np.mean(averagedDF.large)
    avgSmall = np.mean(averagedDF.small)

    print("Average power draw of large image: " + str(avgLarge))
    print("Average power draw of small image: " + str(avgSmall))

    # Declare a list that is to be converted into a column 

    averagedDF = averagedDF.assign(largeAVG=avgLarge)
    averagedDF = averagedDF.assign(smallAVG=avgSmall)

    #averagedDF

    avgTimeInterval = averagedDF.iloc[-1].time-averagedDF.iloc[0].time
    print("Time interval for averages: " + str(avgTimeInterval))

    lPower = (avgLarge*1000)/avgTimeInterval
    sPower = (avgSmall*1000)/avgTimeInterval
    print("Large energy = " + str(lPower) + " milliwatt-seconds")
    print("Small energy = " + str(sPower) + " milliwatt-seconds")
    print("Large energy = " + str(lPower/3600) + " milliwatt-hours")
    print("Small energy = " + str(sPower/3600) + " milliwatt-hours")


    # In[39]:


    fig, ax = plt.subplots(dpi=300)


    plt.plot(averagedData[4].loc[:,'scaled'], newAveragedDataL, color='b')
    plt.plot(averagedData[4].loc[:,'scaled'], newAveragedDataS, color='purple')

    plt.plot(averagedDF.loc[:,'time'], averagedDF.loc[:,'smallAVG'], color='g')
    plt.plot(averagedDF.loc[:,'time'], averagedDF.loc[:,'largeAVG'], color='g')

    ax.set(xlabel='seconds', ylabel='watts',
           title='Averaged Server Activity')

    blueLabel = mpatches.Patch(color='blue', label='avg large')
    greenLabel = mpatches.Patch(color='g', label='avg peaks')
    yellowLabel = mpatches.Patch(color='purple', label='avg small')

    plt.legend(handles=[blueLabel, yellowLabel, greenLabel])

    #ax.grid()
    pngName3 = testDirectoryPath +"aggregator_averaged-"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName3)
    fig.savefig(pngName3)
    plt.show()


    # In[40]:


    fig, ax = plt.subplots(dpi=300)

    colors = ['r','y']
    for plotNum in list(range(len(overlayData))):
        ax.plot(overlayData[plotNum].loc[:,'scaled'], overlayData[plotNum].loc[:,'watts'], color=colors[plotNum%2])

        
    ax.plot(averagedData[4].loc[:,'scaled'], newAveragedDataL, color='b')
    ax.plot(averagedData[4].loc[:,'scaled'], newAveragedDataS, color='purple')

    ax.set(xlabel='seconds', ylabel='watts',
           title='Overlayed Server Activity w/ Averages')

    #ax.scatter(x=overlayD1.loc[:,'scaled'], y=overlayD1.loc[:,'watts'], color='r')
    #ax.plot(overlayS1.loc[:,'scaled'], overlayS1.loc[:,'watts'], color='y')

    redLabel = mpatches.Patch(color='red', label='large')
    blueLabel = mpatches.Patch(color='b', label='avg large')
    yellowLabel = mpatches.Patch(color='yellow', label='small')
    purpleLabel = mpatches.Patch(color='purple', label='avg small')

    plt.legend(handles=[redLabel, blueLabel, yellowLabel, purpleLabel])

    #ax.grid()
    pngName2 = testDirectoryPath +"aggregator_overlay-"+str(datetime.date.today())+"-"+str(int(time.time()))+".png"
    print(pngName2)
    fig.savefig(pngName2)
    plt.show()
    """
