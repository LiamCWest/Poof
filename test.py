def func():
    try:
        func.x += 1
    except:
        func.x = 0
    return func.x

print(func())
print(func())
print(func())
print(func())