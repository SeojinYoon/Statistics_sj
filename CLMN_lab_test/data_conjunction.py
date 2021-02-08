
import os
import pandas as pd

data_directory = "/Users/yoonseojin/Desktop/대학원/TM"

os.chdir(data_directory)

acc_data = []
for path in sorted(os.listdir()):
    data = pd.read_csv(path, sep="\t", header=None)
    data.columns = ["Block",
                    "Trial",
                    "f_1(Hz)",
                    "first ISI",
                    "f_2(Hz)",
                    "second ISI",
                    "Subject's decision",
                    "A time taken to make a decision",
                    "A third ISI time"]
    acc_data.append(data)

result = acc_data[0]
for d in acc_data[1:]:
    result = result.append(d)

result.to_csv("TM.csv", index=False)
