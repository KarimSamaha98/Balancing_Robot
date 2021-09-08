#This file logs the relevant data in csv format
import pandas as pd
import csv
import random
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def WriteData(filename, data, labels):
    #filename = Name of the file to be written in string format
    #Data = Data stream including the 'Time' and 'Signal' in a numpy array
    tresh = 500 #maximum number of instances in the csv file
    try:
        df = pd.read_csv(filename, header=None)
        Labels = np.array(df.iloc[0])
        Data = np.array(df.iloc[1:])
        Data = np.vstack((Data, data))
    except:
        print('[INFO] Could not read the csv file')
        Data = data
        Labels = np.array(labels)

    shape = np.shape(Data)
    if shape[0] > tresh:
        Data = Data[-tresh:,:]
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(Labels)
        try:
            shape[1] #Check if array or not
            writer.writerows(Data)
        except:
            writer.writerow(Data)
        

if __name__ == "__main__":
    for i in range(10):
        data = np.random.rand(1,4)
        WriteData('Data/gyroscope.csv', data, ['Time', 'Gyro_x', 'Gyro_y', 'Gyro_z'])