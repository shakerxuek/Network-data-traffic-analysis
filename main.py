from audioop import reverse
from cProfile import label
from heapq import merge
from http import client
from itertools import count
from mailbox import linesep
from pdb import line_prefix
from pickle import BINSTRING
from matplotlib import lines
import seaborn as sns
from re import X
from tkinter import Y
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import os
from scipy import stats
from collections import Counter

from sqlalchemy import true

def ordered(file:str):
    f=open(file)
    result=[]
    iterf=iter(f)
    for line in iterf:
        result.append(line)
    f.close()
    result.sort()
    r=open('ordered-'+file,'w')
    r.writelines(result)
    r.close

def show_graph(input:list):
    x=np.arange(0,24)
    y=input
    plt.bar(x,y,align='center',label='number of connections of 24 hours')
    plt.xlabel('time(hour)')
    plt.ylabel('number of connections')
    plt.title('Arrival time analysis')
    plt.legend(loc='best')
    plt.show()
    

def count_hour(file:str):
    result=[]
    filenames=os.listdir(file)
    for filename in filenames:
        filepath=file+'/'+filename
        f=open(filepath)
        temp=len(f.readlines())
        f.close()
        result.append(temp)
    print(result)
    return result
    
def duration_calcu(file:str):
    f=open(file)
    lines=f.readlines()
    result=[]
    for i in lines:
        temp=i.split(' ')[7]
        if temp=='SHR' or temp=='OTH' or temp=='RSTOS0' or temp=='RSTRH' or temp=='S0' or temp=='SH':
            result.append(0.0)
        else:
            trans=float(temp)
            result.append(trans)
    f.close()
    maxd=max(result)
    mind=min(result)
    me=get_mean(result)
    print('The maximum value of duration is:',maxd, '\n' 'The minimum value of duration is:',mind, '\n' 'The mean value of duration is:',me)
    arrayd=np.array(result)
    mediand=np.median(arrayd)
    standardd=np.std(arrayd,ddof=1)
    print('The median value of duration is:',mediand, '\n' 'The standard deviation of duration is:',standardd)
    normalarray=[]
    for i in arrayd:
        if i!=0:
            temp=np.log10(i)
            normalarray.append(temp)
        else:
            normalarray.append(0)
    hist, bin_edges = np.histogram(normalarray,density=True,bins=4)
    plt.plot(hist/max(hist),color='#5B9BD5',label='PDF of duration')
    cdf = np.cumsum(hist/sum(hist))
    plt.plot(cdf,'-*', color='#ED7D31',label='CDF of duration')
    plt.xlabel('Duration/s (processed by log10)')
    plt.ylabel('Normalized Density')
    plt.title('PDF and CDF of duration')
    plt.legend(loc='best')
    plt.show()
    # hist, bin_edges = np.histogram(normalarray,range=(-3000,21505))
    # width = (bin_edges[1] - bin_edges[0]) * 0.8
    # plt.figure('PDF and CDF of duration')
    # plt.bar(bin_edges[1:], hist/max(hist), width=width, color='#5B9BD5',label='PDF')
    # cdf = np.cumsum(hist/sum(hist))
    # plt.plot(bin_edges[1:], cdf, '-*', color='#ED7D31',label='CDF')
    # 
    # plt.xlim(-3000,21505)
    # plt.ylabel('Normalized Density')
    # 
    # plt.legend(loc='best')
    # plt.show()

def byte(file:str):
    f=open(file)
    lines=f.readlines()
    result=[]
    for i in lines:
        temp=i.split(' ')[10]
        trans=int(temp)
        result.append(trans)
    f.close()
    maxd=max(result)
    mind=min(result)
    me=get_mean(result)
    print('The maximum value of byte sent is:',maxd, '\n' 'The minimum value of byte sent is:',mind, '\n' 'The mean value of byte sent is:',me)
    arrayd=np.array(result)
    mediand=np.median(arrayd)
    standardd=np.std(arrayd,ddof=1)
    print('The median value of byte sent is:',mediand, '\n' 'The standard deviation of byte sent is:',standardd)
    normalarray=[]
    for i in arrayd:
        if i!=0:
            temp=np.log10(i)
            normalarray.append(temp)
        else:
            normalarray.append(0)

    f=open(file)
    lines=f.readlines()
    result2=[]
    for i in lines:
        temp=i.split(' ')[12]
        trans=int(temp)
        result2.append(trans)
    f.close()
    maxd=max(result2)
    mind=min(result2)
    me=get_mean(result2)
    print('The maximum value of byte received is:',maxd, '\n' 'The minimum value of byte received is:',mind, '\n' 'The mean value of byte received is:',me)
    arrayd2=np.array(result2)
    mediand=np.median(arrayd2)
    standardd=np.std(arrayd2,ddof=1)
    print('The median value of byte received is:',mediand, '\n' 'The standard deviation of byte received is:',standardd)
    normalarray2=[]
    for i in arrayd2:
        if i!=0:
            temp=np.log10(i)
            normalarray2.append(temp)
        else:
            normalarray2.append(0)

    hist, bin_edges = np.histogram(normalarray,density=True,bins=30)
    hist2, bin_edges2 = np.histogram(normalarray2,density=True,bins=30)
    plt.plot(hist/max(hist),color='#5B9BD5',label='PDF of byte sent')
    cdf = np.cumsum(hist/sum(hist))
    plt.plot(cdf,'-*', color='#ED7D31',label='CDF of byte sent')
    plt.plot(hist2/max(hist2),color='red',label='PDF of byte received')
    cdf2 = np.cumsum(hist2/sum(hist2))
    plt.plot(cdf2,'-*', color='#578624',label='CDF of byte received')
    plt.xlabel('byte (processed by log10)')
    plt.ylabel('Normalized Density')
    plt.title('PDF and CDF of byte sent and byte received')
    plt.legend(loc='best')
    plt.show()

def clientip(file:str):
    f=open(file)
    lines=f.readlines()
    result=[]
    dicval=[]
    for i in lines:
        temp=i.split(' ')[2]
        result.append(temp)
    f.close()
    print(len(result))
    dictx={}
    for key in result:
        dictx[key]=dictx.get(key,0)+1
    for i in dictx.values():
        dicval.append(i)
    print(len(dicval))
    dicval.sort(reverse=True)
    print(dicval)
    x=np.arange(1,2105)
    plt.plot(np.log(x),dicval,marker='o',markersize=2,label='Frequency-rank curve of the number of connections')
    plt.xlabel('Relative rank(from most connections to fewest)')
    plt.ylabel('Number of connections')
    plt.title('Frequency-rank graph for the number of connections-client')
    plt.legend(loc='best')
    plt.show()

    f=open(file)
    lines=f.readlines()
    stat={}
    stat2={}
    dicval=[]
    for i in lines:
        temp=i.split(' ')
        key=temp[2]
        value=temp[10]
        oldvalue=0
        if(stat.__contains__(key)):
            oldvalue=stat[key]
            del(stat[key])
        stat[key]=int(oldvalue)+int(value)
    for i in lines:
        temp=i.split(' ')
        key=temp[2]
        value=temp[12]
        oldvalue=0
        if(stat2.__contains__(key)):
            oldvalue=stat2[key]
            del(stat2[key])
        stat2[key]=int(oldvalue)+int(value)
    f.close()
    print(stat2)
    print(stat)
    mergestat=dict(Counter(stat)+Counter(stat2))
    print(mergestat)
    for i in mergestat.values():
        dicval.append(i)
    dicval.sort(reverse=True)
    print(dicval)
    print(len(dicval))
    x=np.arange(1,2105)
    plt.plot(np.log(x),dicval,marker='o',markersize=2,label='Frequency-rank curve of the number of byte exchanged',color='#578624')
    plt.xlabel('Relative rank(from most byte to fewest)')
    plt.ylabel('The total number of byte exchanged')
    plt.title('Frequency-rank graph for the byte exchanged-client')
    plt.legend(loc='best')
    plt.show()

def serverip(file:str):
    f=open(file)
    lines=f.readlines()
    result=[]
    dicval=[]
    for i in lines:
        temp=i.split(' ')[4]
        result.append(temp)
    f.close()
    print(len(result))
    dictx={}
    for key in result:
        dictx[key]=dictx.get(key,0)+1
    for i in dictx.values():
        dicval.append(i)
    print(len(dictx))
    dicval.sort(reverse=True)
    print(dicval)
    x=np.arange(1,16)
    plt.plot(np.log(x),dicval,marker='o',markersize=2,label='Frequency-rank curve of the number of connections')
    plt.xlabel('Relative rank(from most connections to fewest)')
    plt.ylabel('Number of connections')
    plt.title('Frequency-rank graph for the number of connections-server')
    plt.legend(loc='best')
    plt.show()

    f=open(file)
    lines=f.readlines()
    stat={}
    stat2={}
    dicval=[]
    for i in lines:
        temp=i.split(' ')
        key=temp[4]
        value=temp[10]
        oldvalue=0
        if(stat.__contains__(key)):
            oldvalue=stat[key]
            del(stat[key])
        stat[key]=int(oldvalue)+int(value)
    for i in lines:
        temp=i.split(' ')
        key=temp[4]
        value=temp[12]
        oldvalue=0
        if(stat2.__contains__(key)):
            oldvalue=stat2[key]
            del(stat2[key])
        stat2[key]=int(oldvalue)+int(value)
    f.close()
    print(stat2)
    print(stat)
    mergestat=dict(Counter(stat)+Counter(stat2))
    print(mergestat)
    for i in mergestat.values():
        dicval.append(i)
    dicval.sort(reverse=True)
    print(len(dicval))
    x=np.arange(1,16)
    plt.plot(np.log(x),dicval,marker='o',markersize=2,label='Frequency-rank curve of the number of byte exchanged',color='#578624')
    plt.xlabel('Relative rank(from most byte to fewest)')
    plt.ylabel('The total number of byte exchanged')
    plt.title('Frequency-rank graph for the byte exchanged-server')
    plt.legend(loc='best')
    plt.show()

def myanalysis(file:str):
    f=open(file)
    lines=f.readlines()
    result=[]
    dicval=[]
    dickey=[]
    for i in lines:
        temp=i.split(' ')[8]
        result.append(temp)
    f.close()
    dictx={}
    for key in result:
        dictx[key]=dictx.get(key,0)+1
    for i in dictx.values():
        dicval.append(i)
    for i in dictx.keys():
        dickey.append(i)
    print(dicval)
    print(len(dicval))
    print(dickey)
    print(len(dickey))
    plt.bar(dickey,dicval,color='purple',label='Frequency of connection state')
    plt.xlabel('Connection state')
    plt.ylabel('Frequency')
    plt.title('Frequency graph of connection state')
    plt.legend(loc='best')
    plt.show()

def mergedoc(file:str):
    filenames=os.listdir(file)
    f=open('mergedoc.txt','w')
    for filename in filenames:
        filepath=file+'/'+filename
        for line in open(filepath):
            f.writelines(line)
    f.close()

def addspace(file:str):
    f=open(file)
    c=open('addspace.txt','w')
    lines=f.readlines()
    for line in lines:
        temp=' '+line
        c.writelines(temp)
    f.close()
    c.close()

def addspace2(file:str):
    f=open(file)
    c=open('addspace.txt','w')
    lines=f.readlines()
    for i in lines:
        temp=i.split(' ')[7]
        if temp=='SHR' or temp=='OTH' or temp=='RSTOS0' or temp=='RSTRH' or temp=='S0' or temp=='SH':
            i=i.replace(temp,'0'+' '+temp)
            c.writelines(i)
        else:
            c.writelines(i)
    f.close()

def get_mean(input:list):
    sum=0
    for item in input:
        sum+=item
    return sum/len(input)

def extra(file:str):
    f=open(file,encoding='UTF-8')
    lines=f.readlines()
    result=[]
    for i in lines:
        temp=i.split(' ')[7]
        result.append(temp)
    f.close()
    print(result)

def count_minute(file:str):
    result=[]
    f=open(file)
    lines=f.readlines()
    for i in lines:
        temp=i.split(' ')[1]
        trans=float(temp)
        result.append(trans)
    f.close()
    result.sort()
    maxd=1632376800
    mind=1632290400
    axisx=np.linspace(mind,maxd,num=1441)
    axisx=axisx.tolist()
    hist,bin=np.histogram(result,bins=axisx)
    plt.plot(hist,color='#5B9BD5',label='number of connections per minute')
    plt.xlabel('minutes')
    plt.ylabel('number of connections')
    plt.title('Arrival time analysis')
    plt.legend(loc='best')
    plt.show()
    

# byte('addspace.txt')
# clientip('addspace.txt')
# serverip('addspace.txt')
# duration_calcu('addspace.txt')
# addspace2('mergedoc.txt')
# extra('1.txt')
# myanalysis('addspace.txt')
# list1=count_hour('merge')
# show_graph(list1)
count_minute('addspace.txt')


