import os
import json
import csv

#import numpy as np
#import matplotlib.pyplot as plt

def write_time(infile):
    student = []

    start_time_holder = 0
    end_time_holder = 0

    #bins to hold the total amount of time
    syntax_time = 0
    type_time = 0
    success_time = 0
    temp_time = 0

    # 0 represents success, 1 represents type error, 
    # -1 represents syntax error, this is a flag
    error_type_holder = 0

    with open(infile) as inf:
        for line in inf:
            item = eval(line)

            #to deal with error event, record its time
            if item['type'] == "error" and item['session']!= 0:


                # set the flag to check which bin it should locate to
                if item['error'] == "Syntax error":
                    error_type_holder = -1
                elif item['error'] == "Type error":
                    error_type_holder = 1
                else:
                    error_type_holder = 0

                
                # add the time to the error's bin: start time - current time
                # and set the end time to be the error's time
                if error_type_holder == 0:
                    success_time = success_time + item['time'] - start_time_holder + temp_time
                elif error_type_holder == 1:
                    type_time = type_time + item['time'] - start_time_holder + temp_time
                else:
                    syntax_time = syntax_time + item['time'] - start_time_holder + temp_time

                temp_time = 0
                start_time_holder = item['time']

            # to deal with session event, use its end field to 
            # minus the last start field, and store its start field
            # then add this to the category of the error time, or
            # code_writing time

            # deal with time session events
            else:

                end_time_holder = item['end']

                #for the first case, just record the start time
                if item['end'] == 0 or item['session'] == 0: 
                    start_time_holder = item['start']
                    continue


                #for every other case, use end time minus previous start time
                #to calculate out the session time, and add it to the bin it 
                # belongs to 
                temp_time = end_time_holder - start_time_holder

                start_time_holder = item['start']
    
    print("succ:")
    print(success_time)
    print("type:")
    print(type_time)

    student = [syntax_time/60, type_time/60, success_time/60]
    #write the data to a .csv file
    with open('test.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(student)
    csvfile.close()
    inf.close()
    

################################################################################################### Main

dir = os.path.dirname('__file__')
infile = os.path.join(dir, 'homework1-withtag')
student = []

# homework 1 problems
errors = ['success','type','syntax']

#print hw1
# for q in errors:
#     with open('test.csv','a') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(q)
#     csvfile.close

for i in os.listdir(infile):
    write_time(os.path.join(infile,i))
