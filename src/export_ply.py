import numpy as np
import pandas as pd
import pcl
from pyntcloud import PyntCloud

points = pcl.main()
colors = np.empty(shape=(0,3))

print(points.shape)
for i in range(48000):
    colors = np.vstack((colors,[255,0,0]))
print(colors.shape)

cloud = PyntCloud(pd.DataFrame(
     # same arguments that you are passing to visualize_pcl
    data=np.hstack((points, colors)),
    columns=["x", "y", "z", "red", "green", "blue"]))

cloud.to_file("output.ply")