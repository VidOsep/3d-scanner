def write_ply(points,colors,filename):
    file = open(filename,'w')
    ply = ['ply','format ascii 1.0','comment 3D SCAN OF OBJECT','element vertex ' + str(points.shape[0]),'property float x','property float y','property float z','property uchar red','property uchar green','property uchar blue','end_header']
    for i in ply:
        file.write(i+'\n')
    for i in range(int(points.shape[0])):
        file.write("%d %d %d %d %d %d\n"%(points[i,0],points[i,1],points[i,2],colors[i,0],colors[i,1],colors[i,2]))