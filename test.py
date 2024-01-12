from intervaltree import IntervalTree, Interval
import math

tree = IntervalTree([Interval(0, 1), Interval(0.5, 1)])
print(tree.at(math.nextafter(tree.end(), float("-inf"))))