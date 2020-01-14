import pandas as pd

namelist = ['name', 'timestamp', 'count']
    
df = pd.read_csv("../uatu.csv", index_col=False, names=namelist)

print(namelist)
df2 = df.fillna(0)
camera_names = df['name'].unique()
df2.sort_values(by=['name', 'count'], inplace=True)
series = df2.groupby('name')['count'].max()
print(series.to_dict()['camera_17'])
