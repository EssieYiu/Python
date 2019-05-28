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
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
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
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
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
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
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
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    start = time.time()
    cows = load_cows("ps1_cow_data.txt")
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