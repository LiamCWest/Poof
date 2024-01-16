#two functions for binary searching (not really needed since the bisect module exists but i didn't know about it when i wrote this)

#compareFunc should take in 2 arguments, the first of which is toSearch
#it should return >0, 0, <0 if toSearch is greater than, equal to, or less than the other value respectively
#if toSearch is not in the list, it returns None
def strictBinarySearch(list, toSearch, compareFunc): #strict binary search, returns None if toSearch is not in the list
    startIndex = 0 #the start index of the list

    while list: #while the list is not empty
        midIndex = len(list) // 2 #the middle index of the list
        midValue = list[midIndex] #the middle value of the list

        comp = compareFunc(toSearch, midValue) #compare the toSearch value to the middle value

        if comp == 0: #if the toSearch value is equal to the middle value
            return startIndex + midIndex #return the index of the middle value
        elif comp > 0: #if the toSearch value is greater than the middle value
            startIndex += midIndex + 1 #set the start index to the index after the middle index
            list = list[midIndex + 1:] #set the list to the list after the middle index
        else: #if the toSearch value is less than the middle value
            list = list[:midIndex] #set the list to the list before the middle index

#compareFunc should take in 2 arguments, the first of which is toSearch
#it should return >0, 0, <0 if toSearch is greater than, equal to, or less than the other value respectively
#if the toSearch is not in the list, it returns the index of the value that is smaller than it and closest to it
#if toSearch is smaller than all items in the list, it returns -1
def binarySearch(list, toSearch, compareFunc): #binary search, returns the index of the value that is smaller than it and closest to it if toSearch is not in the list
    startIndex = 0 #the start index of the list

    while list: #while the list is not empty
        midIndex = len(list) // 2 #the middle index of the list
        midValue = list[midIndex] #the middle value of the list
        
        if len(list) == 2: #special case for if the list has 2 items
            if compareFunc(toSearch, list[1]) > 0: #if toSearch is greater than the second item in the list
                return startIndex + 1 #return the index of the second item in the list
            
            if compareFunc(toSearch, list[0]) < 0: #if toSearch is less than the first item in the list
                return startIndex - 1 #return -1, must be smaller than all items in the list
        elif len(list) == 1: #special case for if the list has 1 item
            if compareFunc(toSearch, list[0]) > 0: #if toSearch is greater than the item in the list
                return startIndex #return the index of the item in the list
            
            if compareFunc(toSearch, list[0]) < 0: #if toSearch is less than the item in the list
                return startIndex - 1 #return -1, must be smaller than all items in the list

        comp = compareFunc(toSearch, midValue) #compare the toSearch value to the middle value

        if comp == 0: #if the toSearch value is equal to the middle value
            return startIndex + midIndex #return the index of the middle value
        elif comp > 0: #if the toSearch value is greater than the middle value
            startIndex += midIndex + 1 #set the start index to the index after the middle index
            list = list[midIndex + 1:] #set the list to the list after the middle index
        else: #if the toSearch value is less than the middle value
            list = list[:midIndex] #set the list to the list before the middle index