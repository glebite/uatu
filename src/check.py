import pandas as pd

namelist = list()
for camera_number in range(1,25):
    camera_name = "camera_{}".format(camera_number)
    camera_time = "camera_time_{}".format(camera_number)
    camera_count = "camera_count_{}".format(camera_number)
    namelist.append(camera_name)
    namelist.append(camera_time)
    namelist.append(camera_count)
    
df = pd.read_csv("../uatu.csv", index_col=False, names=namelist)
print(namelist)
df2 = df.fillna(0)
for camera_number in range(1,25):
    print(camera_number, df2['camera_count_{}'.format(camera_number)].max())
