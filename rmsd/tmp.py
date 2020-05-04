lis = []
n_geom = 3
for i_geom in range(n_geom):
    for j_geom in range(i_geom):
        lis.append([i_geom,j_geom])
print lis
for i in range(n_geom*(n_geom-1)/2):
    print lis[i][0]
