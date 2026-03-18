import numpy as np

data = np.loadtxt("/home/gunhee/qbench/240114_i9_kiss-pfh-w-gs-0.3-1.5-0.9/00/2_to_6_KISS-PFH_extraction_and_matching.txt")
print(np.mean(data, axis=0))
