from intervaltree import IntervalTree, Interval

tree = IntervalTree([Interval(1, 2, "hi"), Interval(3, 4, "lo")])

for i in tree:
    print(i.data)