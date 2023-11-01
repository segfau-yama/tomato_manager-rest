import numpy as np

math = [[71, 80, 95, 52, 93, 68, 98, 30, 78, 60], [71, 80, 95, 52, 93, 68, 98, 30, 78, 60]]
english = [62, 89, 82, 95, 92, 89, 91, 72, 75, 93]

print(np.corrcoef(math, english))