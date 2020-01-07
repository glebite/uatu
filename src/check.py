import pandas as pd

df = pd.read_csv("../uatu.csv", index_col=False, header=None)

df2 = df.fillna(0)
for column in range(2,73,3):
    print("*"*int(df2[column].max()))
