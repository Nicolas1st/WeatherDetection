import pickle
import cv2
import KNN
import os
import numpy as np

data = []

os.chdir('C:/Users/nicol/Desktop')

for label, part in enumerate(['Sky', 'Cloud', 'Sun']):

    os.chdir(f'C:/Users/nicol/Desktop/{part}Segments')
    files = os.listdir()

    for file in files:
        image = cv2.imread(file)
        hist = KNN.get_histogram(image)
        print()
        data.append((hist, label))

print(data)
os.chdir('C:/Users/nicol/Desktop')

with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)
