def calculateArea(x, y):
 
    # Declare value of pi
    pi = 3.1415926536
 
    # Calculate area of outer circle
    arx = pi * x * x
 
    # Calculate area of inner circle
    ary = pi * y * y
 
    # Difference in areas
    return arx - ary

def area(x):
 
    # Declare value of pi
    pi = 3.1415926536
 
    # Calculate area of outer circle
    arx = pi * x * x
 
    return arx
 
# Driver Code
x = 4
y = 2

print(area(y)) 
print(calculateArea(x, y))
 
# This code is contributed