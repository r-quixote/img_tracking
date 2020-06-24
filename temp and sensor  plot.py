# -*- coding: utf-8 -*-
"""
Created on Tue May 12 14:42:06 2020

@author: YasmineMnb
"""
from matplotlib import pyplot as plt
import numpy as np
import time
import datetime
import pandas as pd

def load_simp_file(file_path):
    time_arr = [] ; temp = []; hum = []
    cnt = 0
    with open (file_path,"r") as input_file:
        line = input_file.readline().strip().split(",")
        currr_t = float(line[2])
        for line in input_file:
            line = line.strip().split(",")
            temp.append(float(line[0]))
            hum.append(float(line[1]))
    #        if float(line[2])/1000/3600 +11>24:
    #            time.append(11+float(line[2])/1000/3600-24)
    #        else: time.append(11+float(line[2])/1000/3600)
            if float(line[2])<currr_t:
    #            print(cnt)
                currr_t = float(line[2]) + max_t
            else:
                currr_t = float(line[2])
                max_t = currr_t
            time_arr.append(currr_t)
            cnt+=1
    time_arr = np.array(time_arr)
    temp = np.array(temp)
    hum = np.array(hum)
    return time_arr, temp, hum

def load_simp_file_from_pi(file_path):
    time_arr = [] ; temp = []; hum = []
    with open (file_path,"r") as input_file:
        header_line = input_file.readline().strip().split(",")
        for line in input_file:
            line = input_file.readline().strip().split(",")
            for i in range(len(line)):
                line[i] =  line[i].strip("\t")
            hum.append(float(line[0]))
            temp.append(float(line[1]))
            time_elem = time.mktime(time.strptime(line[2], '%Y/%m/%d-%H:%M'))
            time_arr.append(datetime.datetime.fromtimestamp(time_elem))
    return time_arr; temp; hum


def load_exp_file(file_path, arduino_start_time):
    #%
    file_path_clean = file_path.strip(".txt") + "_cleaned.txt"
    with open(file_path_clean, "w") as out:
        with open(file_path, "r") as file:
            for line in file:
                if len(line.split(","))==7:
                    out.write(line)
    df = pd.read_csv(file_path_clean)
    df.columns = ["temp", "hum", "s1","s2","s3","s4", "millis"]
    #%
    ## add datetime formated time
    time_str_arr = []
    for i, t in enumerate(df["millis"]):
        time_ep = convert_millis_time(arduino_start_time, t)
        time_str_arr.append(datetime.datetime.fromtimestamp(time_ep))
    time_str_arr = np.array(time_str_arr)
    df = df.astype(float)
    df["datetime"] = time_str_arr
    #%
    return df

def convert_millis_time(arduino_start_time, time_millis):
    """
    convert time from arduino-time to time-since-epoch, given a start time
    arduino_start_time format - 20-05-17 10:44
    """
    start_time = time.strptime(arduino_start_time, '%y-%m-%d %H:%M')
    epoch_start_time = time.mktime(start_time)
    time_sec = time_millis/1000
    return int(epoch_start_time + time_sec)

def convert_to_datetime(arduino_start_time, millis_time_array):
    time_str_arr = []
    for i, t in enumerate(millis_time_array):
        time_ep = convert_millis_time(arduino_start_time, t)
        time_str_arr.append(datetime.datetime.fromtimestamp(time_ep))
    return np.array(time_str_arr)
#%%
def load_ophir_log_file(file_path = r"C:\Users\YasmineMnb\Desktop\june exp\ophir_flicker_test\1(L)\200618_ophir_testing_flicker_clean_data.txt"):
    #%%
    with open(file_path, "r") as input_file:
        for line in input_file:
            line = line.strip()
            print(line.split("\t"))
            break
    #%%
    file_path = r"C:\Users\YasmineMnb\Desktop\june exp\ophir_flicker_test\1(L)\200618_2_ophir_testing_flicker_clean_data.txt"
    df = pd.read_csv(file_path, delimiter="\t")
    plt.plot(df[df.columns[0]], df[df.columns[1]])

#%%
time_arr, temp, hum = load_simp_file(file_path = r"C:\Users\YasmineMnb\Desktop\logs\temp_log200525-1204.txt")
arduino_start_time = "20-05-20 09:07"
dt_time = convert_to_datetime(arduino_start_time, time_arr)
#%%
arduino_start_time = "20-06-16 11:28"
#170520_0857
file_path = r"C:\Users\YasmineMnb\Desktop\june exp\200616_contin\1606.TXT"
df = load_exp_file(file_path, arduino_start_time)

#%%         ploting
# =============================================================================
#
# max_temp = np.where(temp == temp.max())[0]
# max_temp_clean_indx = np.array([max_temp[0]])
# for i in range(1, len(max_temp)):
#     if max_temp[i]-max_temp[i-1] >1:
#         max_temp_clean_indx= np.append(max_temp_clean_indx, max_temp[i])
#
# min_temp = np.where(temp == temp.min())[0]
# min_temp_clean_indx = np.array([min_temp[0]])
# for i in range(1, len(max_temp)):
#     if max_temp[i]-max_temp[i-1] >1:
#         max_temp_clean_indx= np.append(max_temp_clean_indx, max_temp[i])
#
# =============================================================================

 #["temp", "hum", "s1","s2","s3","s4", "millis", "datetime"]

## ploting
fig =  plt.figure()
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

## add data
ax1.plot(df["datetime"][::10], df["s1"][::10], label = "sensor1")#, alpha = 0.9 )
ax1.plot(df["datetime"][::10], df["s2"][::10], label = "sensor2")#, alpha = 0.9 )
ax1.plot(df["datetime"][::10], df["s3"][::10], label = "sensor3")#, alpha = 0.9 )
ax1.plot(df["datetime"][::10], df["s4"][::10], label = "sensor4")#, alpha = 0.9 )

ax2.plot(df["datetime"], df["temp"], label = "temp")#, alpha = 0.9 )
#ax1.plot(time, hum, label = "hum")#, alpha = 0.9 )

## titles and "design"
plt.xlabel('Time [H]') # $_{[H]}$for subscript
plt.ylabel('temp [C]')
plt.title('Temp Vs. Time')
#plt.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
ax1.legend()
#plt.subplots_adjust(left=0.1, bottom=0.10, right=0.70, top=0.92, wspace=0.2, hspace=0)
plt.gcf().autofmt_xdate()
plt.show()
#%%





