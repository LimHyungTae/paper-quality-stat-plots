import numpy as np

data = np.loadtxt("/home/gunhee/qbench/240114_i9_fpfh-w-gs-0.3-1.5-0.9-multi-thread/00/2_to_6_FPFH_extraction_and_matching.txt")
print(np.mean(data, axis=0))
