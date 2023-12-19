#compareFunc should take in 2 arguments, the first of which is toSearch
#it should return >0, 0, <0 if toSearch is greater than, equal to, or less than the other value respectively
#if toSearch is not in the list, it returns None
def strictBinarySearch(list, toSearch, compareFunc):
    startIndex = 0

    while list:
        print(list)
        midIndex = len(list) // 2
        midValue = list[midIndex]

        comp = compareFunc(toSearch, midValue)

        if comp == 0:
            return startIndex + midIndex
        elif comp > 0:
            startIndex += midIndex + 1
            list = list[midIndex + 1:]
        else:
            list = list[:midIndex]

#compareFunc should take in 2 arguments, the first of which is toSearch
#it should return >0, 0, <0 if toSearch is greater than, equal to, or less than the other value respectively
#if the toSearch is not in the list, it returns the index of the value that is smaller than it and closest to it
#if toSearch is smaller than all items in the list, it returns -1
def binarySearch(list, toSearch, compareFunc):
    startIndex = 0

    while list:
        print(list)
        midIndex = len(list) // 2
        midValue = list[midIndex]
        
        if len(list) == 2:
            if compareFunc(toSearch, list[1]) > 0:
                return startIndex + 1
            
            if compareFunc(toSearch, list[0]) < 0:
                return startIndex - 1
            
            if compareFunc(toSearch, list[0]) > 0 and compareFunc(toSearch, list[0]) < 0:
                return startIndex
        elif len(list) == 1:
            if compareFunc(toSearch, list[0]) > 0:
                return startIndex
            
            if compareFunc(toSearch, list[0]) < 0:
                return startIndex - 1

        comp = compareFunc(toSearch, midValue)

        if comp == 0:
            return startIndex + midIndex
        elif comp > 0:
            startIndex += midIndex + 1
            list = list[midIndex + 1:]
        else:
            list = list[:midIndex]