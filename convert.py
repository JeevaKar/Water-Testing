from PIL import Image
import csv
import math
import os
from pathlib import Path

dir = os.getcwd()

#Import images here. Use full pathways to indicate.

landImages = [os.path.join(dir, 'Images', 'Land 1.jpg'),
          os.path.join(dir, 'Images', 'Land 2.jpg'),
          os.path.join(dir, 'Images', 'Land 3.jpg'),
          os.path.join(dir, 'Images', 'Land 4.jpg'),
          os.path.join(dir, 'Images', 'Land 6.jpg'),
          os.path.join(dir, 'Images', 'Land 5.jpg'),
          os.path.join(dir, 'Images', 'Land 7.jpg'),
          os.path.join(dir, 'Images', 'Land 8.jpg')]

waterImages = [os.path.join(dir, 'Images', 'Water 1.jpg'),
               os.path.join(dir, 'Images', 'Water 4.jpg'),
               os.path.join(dir, 'Images', 'Water 3.jpg'),
               os.path.join(dir, 'Images', 'Water 2.jpg')]

CSVData = []

FACTOR = 256**(1/255)

#scaleup, scaledown, removeDuplicateLists, and removeConflictLists are to configure data. 

def scaleUp(value: int, flag = True):
    if round(value) > 255 and flag:
        raise ValueError("Input is greater than 255. Current input is:"+str(value))
    return math.log((value+1), FACTOR) 

def scaleDown(value: int, flag = True):
    if round(value) > 255 and flag:
        raise ValueError("Input is greater than 255. Current input is:"+str(value))
    return (FACTOR**value)-1

def removeDuplicateLists(input_list):
    seen = set()
    result = []
    for inner_list in input_list:
        # Convert the inner list to a tuple (hashable) to check for duplicates
        inner_tuple = tuple(inner_list)
        if inner_tuple not in seen:
            result.append(inner_list)
            seen.add(inner_tuple)
    return result

def removeConflictLists(input_list):
    seen = {}
    conflicting_keys = set()

    for inner_list in input_list:
        # Create a key based on the first three integers
        key = tuple(inner_list[:3])
        if key in seen:
            # If the key already exists and the fourth integer is different, mark the key as conflicting
            if seen[key] != inner_list[3]:
                conflicting_keys.add(key)
        else:
            # Record the fourth integer for this key
            seen[key] = inner_list[3]

    # Create a new list excluding all entries with conflicting keys
    result = [inner_list for inner_list in input_list if tuple(inner_list[:3]) not in conflicting_keys]
    return removeDuplicateLists(result)

for file in landImages: #formatting land images for model, model requires RGB format
    image = Image.open(file)
    image = image.convert('RGB')
    width, height = image.size
    hex_colors = [] #initializing list

    for x in range(width): #recording the RGB values for pixels in land images
        for y in range (height):
            r, g, b = image.getpixel((x, y))
            # hex_color = [scaleUp(r), scaleDown(g), scaleDown(b)]
            hex_color = [r, g, b]
            hex_colors.append(hex_color)
    
    for row in hex_colors:
        row.append('0')
        CSVData.append(row)

for file in waterImages: #formatting water images for model, model requires RGB format
    image = Image.open(file)
    image = image.convert('RGB')
    width, height = image.size
    hex_colors = [] #initializing list

    for x in range(width): #recording the RGB values for pixels in water images
        for y in range (height):
            r, g, b = image.getpixel((x, y))
            # hex_color = [scaleUp(r), scaleDown(g), scaleDown(b)]
            hex_color = [r, g, b]
            hex_colors.append(hex_color)
    
    for row in hex_colors:
        row.append('1')
        CSVData.append(row)

CSVData = removeConflictLists(CSVData) #creating final data file

with open(os.path.join(dir, r'testdata.csv'), 'w', newline='') as csvfile: #storing CSV file with data. add your own pathway to store file.
    hexWriter = csv.writer(csvfile, delimiter=',', quotechar="|")
    for row in CSVData:
        hexWriter.writerow(row)