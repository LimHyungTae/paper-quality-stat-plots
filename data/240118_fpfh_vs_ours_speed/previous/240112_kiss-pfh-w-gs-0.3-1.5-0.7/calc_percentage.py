import os
import pandas as pd

def calculate_percentage(algorithm, dataset):
    if dataset == "mulran":
        base_dirs = ['DCC01', 'DCC02', 'DCC03', 'Riverside01', 'Riverside02', 'Riverside03', 'KAIST02', 'KAIST03']
    elif dataset == "kitti":
        base_dirs = ['00', '02', '05', '06', '07', '08']
    sub_dirs = ['2_to_6', '6_to_10', '10_to_12']
    total_lines = 1000

    result = dict()

    for base in base_dirs:
        result[base] = dict()
        for sub in sub_dirs:
            path = os.path.join(base, sub, algorithm+'_failure.txt')
            if os.path.exists(path):
                with open(path, 'r') as file:
                    lines = file.readlines()
                failure_percentage = (total_lines - len(lines)) / total_lines * 100
                result[base][sub] = failure_percentage
            else:
                result[base][sub] = 'N/A'

    df = pd.DataFrame(result)
    return df

# algorithms = ['RANSAC1K', 'FGR', 'TEASER', 'Quatro']
algorithms = ['Quatro']

for alg in algorithms:
    print(f"\nAlgorithm: {alg}")
    print(calculate_percentage(alg, "kitti"))
    print(calculate_percentage(alg, "mulran"))
