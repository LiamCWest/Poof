import bisect
list = [(0, 1), (1, 1), (2, 1), (3, 1)]

print(bisect.bisect_right(list, 2.5, key=lambda tup: tup[0]))