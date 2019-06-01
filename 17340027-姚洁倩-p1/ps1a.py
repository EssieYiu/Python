###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    dic = {}
    f = open(filename,'r')
    for lines in f:
        lines = lines.strip('\n')
        data = lines.split(',')
        if dic.get(data[0],0) == 0:
            dic[data[0]] = int(data[1])
    f.close()
    return dic


# Problem 2
def greedy_cow_transport(cows,limit=10):
    my_list = [] #store the cows that still not be transported
    for key in cows:
        my_list.append((key,cows[key]))
    my_list.sort(key= lambda x:x[1],reverse = True)
    temp_list = [] #a single trip
    trip_list = [] #return value
    cur_weight = 0 #weight of a single trip
    index = 0
    while len(my_list):
        if cur_weight + my_list[index][1] <= limit:
            temp_list.append(my_list[index][0])
            cur_weight = cur_weight+my_list[index][1]
            my_list.pop(index)
        else:
            index = index + 1
        if index == len(my_list):
            trip_list.append(temp_list)
            temp_list = []
            cur_weight = 0
            index = 0
    return trip_list

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    least_trip = ([],99999)#list containing tuples of partition and its trip cost
    for partition in get_partitions(cows):
        for single_trip in partition:
            total_weight = 0
            over_weight = False
            for single_cow in single_trip:
                total_weight = total_weight + cows[single_cow]
                if total_weight > 10:
                    over_weight = True
                    break
            if over_weight == True:
                break
        if over_weight == False and len(partition)<least_trip[1]:
            least_trip = (partition,len(partition))
    return least_trip[0]
# Problem 4
def compare_cow_transport_algorithms():
    start = time.time()
    cows = load_cows("ps1_cow_data_2.txt")
    greedy = greedy_cow_transport(cows)
    end = time.time()
    print("Greedy:Time spent:",end-start)
    print("minimun number of trip:",len(greedy))
    print("solution:",greedy)

    start = time.time()
    brute = brute_force_cow_transport(cows)
    end = time.time()
    print("Brute force:Time spent:",end-start)
    print("minimun number of trip:",len(brute))
    print("solution:",brute)

compare_cow_transport_algorithms()