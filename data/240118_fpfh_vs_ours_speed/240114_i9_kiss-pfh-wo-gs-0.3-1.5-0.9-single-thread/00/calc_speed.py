import numpy as np

data = np.loadtxt("2_to_6_KISS-PFH_extraction_and_matching.txt")
print(np.mean(data, axis=0))

