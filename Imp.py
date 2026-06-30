import math
 
print(math.sqrt(36))
# Pattern 2: Import specific items from a module
from math import sqrt, pi

# Now use: sqrt(16)

# Import entire module
import random

# Use module functions
number = random.randint(1, 10)
choice = random.choice(["apple", "banana", "orange"])
print(number , choice)

# Date and time
import datetime
today = datetime.date.today()
print(today)  # 2024-01-15

# Operating system
import os
current_dir = os.getcwd()
print(current_dir)

# JSON data
import json
data = {"name": "Alice", "age": 30}
json_string = json.dumps(data)