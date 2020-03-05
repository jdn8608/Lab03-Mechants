"""
CSAPX Lab 3: Merchants of Venice

This program will read in a list of Merchants and created tuples of these Merchants.
Then depending on the determined runtime in the call of this program from the command line, the program will
run algorithms to find the median value of the list of merchants. This median merchant is the optimal location
that minimizes the distance travel to other locations.

$ python3 merchants.py [slow|fast] input-file

Author: Jdn8608 @ rit.edu
Author: Joseph Nied
Section: R3
Date/Time: 9/18/19 10:21 PM
"""

import collections      # namedtuple
import sys              # arg
import time             # clock
import random           # random

from typing import List # List
def main() -> None:
    """
    The main function.
    :return: None
    """
    args=sys.argv           #retrieves commmand line args
    filename = args[2]      #retrieves the filename from command line arguement
    sum = 0                 #initliaizes the sum var to calc the sum of the distances away from the median
    start, end = 0,0        #initliazes the start and end vars that help calculate the time for quicksort/quickselect
    median = None           #initliazes the median var which will be the Merchant that is in the center of a sorted list of merchants

    Merchant = collections.namedtuple('Merchant', ('name', 'location')) #creates the namedtuple with fields of name and location
    Merchants=[] #initlializes the merhcants list that will be filled with merchant named tuple

    #Read the file and make Merchants
    with open( filename ) as p:
        for line in p:
            fields = line.split() #Splits the line so that we can seperate the name and location
            Merchants.append(Merchant(name=fields[0], location=int(fields[1]))) #Fills Merchants with created Merchant tuples

    #The defualt and also the fast runtime in which quickselect is utilized to find the median
    if (len(args) == 2 or args[1] == 'fast'):
        start = time.perf_counter()
        sorted_Merchants = quick_select(Merchants, len(Merchants)//2)
        end = time.perf_counter()
        median = sorted_Merchants[len(sorted_Merchants) // 2]

    #The slow run time in which quicksort is utilized to find the median
    elif (args[1] == 'slow'):
        start = time.perf_counter()
        sorted_Merchants = quick_sort(Merchants)
        end = time.perf_counter()
        median = sorted_Merchants[len(sorted_Merchants) // 2]

    #Error in arguements passed
    else:
        print("Non allowed entry for speed parameter of program. Ending Program...")
        exit()


    #Calculates the sum of the distances the median is away from other locations
    for i in range(len(Merchants)):
        sum += abs((Merchants[i].location) - median.location)


    #PRINT DATA
    print("Search type: " + args[1])
    print("Number of merchants: " + str(len(Merchants)))
    print("Elapsed time: " + str(end - start) + " Seconds")
    print("Optimal store location: " + str(median))
    print("Sum of distances:  " + str(sum))





def _partition(data: List[int], pivot: int) :
    """
    Three way partition the data into smaller, equal and greater lists,
    in relationship to the pivot
    :param data: The data to be sorted (a list)
    :param pivot: The value to partition the data on
    :return: Three list: smaller, equal and greater
    """
    less, equal, greater = [], [], []
    for element in data:
        if element.location < pivot.location:
            less.append(element)
        elif element.location > pivot.location:
            greater.append(element)
        else:
            equal.append(element)
    return less, equal, greater

def quick_sort(data: List[int]) -> List[int]:
    """
    Performs a quick sort and returns a newly sorted list
    :param data: The data to be sorted (a list)
    :return: A sorted list
    """
    if len(data) == 0:
        return []
    else:
        pivot = data[0]
        less, equal, greater = _partition(data, pivot)
        return quick_sort(less) + equal + quick_sort(greater)

def quick_select(data: List[int], k):
    """

    :param data: A list of Objects, in this case, Merchants, that will be traversed in a fashion to find the kth term in
     the list as if it were sorted
    :param k: The term in the list of data that you are looking for as if data was sorted
    :return: a semi-sorted list in which the Kth term is positioned correctly in the list
    """
    if len(data) == 0:
        return []
    else:
        pivot = data[random.randint(1,len(data))-1]     #sets pivot to a random integer to improve the BigO
        less, equal, greater = _partition(data, pivot)
        m = len(less)                                   #m is the length of the lesser partition
        count = len(equal)                              #count is the length of the equal partition
        #1.)If k is between m and m+count, the k-th element has been found. It’s the pivot
        if(m < k and k < (m + count)):
            return less + equal + greater
        #2.) If m > K then the Kth element is in lesser and needs to be furthered partitioned
        elif(m > k):
            return quick_select(less, k ) + equal + greater
        #3.) If other params are not true, then the Kth term is in the greater section and k needs to change according to our algorithm in class
        else:
            return less+ equal + quick_select(greater, k-m-count)


if __name__ == '__main__':
    main()