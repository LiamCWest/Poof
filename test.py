dict1 = {"a": 1}
dict2 = {"a": dict1["a"] for _ in range(1)}
print(dict2["a"])

print(dict2["a"])
dict1["a"] = 2
print(dict2["a"])