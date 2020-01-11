import pandas as pd

namelist = ['name', 'timestamp', 'count']
    
df = pd.read_csv("../uatu.csv", index_col=False, names=namelist)

print(namelist)
df2 = df.fillna(0)
print(df2['camera_count'].max())
camera_names = df['name'].unique()
print(camera_names)
for camera_name in camera_names:
    print(df['name'] == camera_name)

