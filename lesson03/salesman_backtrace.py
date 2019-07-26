latitudes  = [-8, -94, 23, -73, -85, 10, 78, -72, 31, 74]
longitudes = [-47, -68, 36, -9, -68, 27, -52, 56, -59, 12]

n = len(latitudes)
distance = [[((latitudes[u]-latitudes[v])**2 + (longitudes[u]-longitudes[v])**2)**0.5 for u in range(n)] for v in range(n)]
costOfPartialTour = 0
bestTourSoFar = []
costOfBestTourSoFar = float('inf')
partialTour = [i for i in range(n)]

def swap(alist, i, j):
    t = alist[i]
    alist[i] = alist[j]
    alist[j] = t

def tsp(currentLevel):
    global costOfPartialTour
    global bestTourSoFar
    global costOfBestTourSoFar
    global partialTour
    if (currentLevel == n-1):
        if (costOfPartialTour + distance[partialTour[n-2]][partialTour[n-1]] + distance[partialTour[n-1]][partialTour[0]]) < costOfBestTourSoFar :
            costOfBestTourSoFar = costOfPartialTour + distance[partialTour[n-2]][partialTour[n-1]] + distance[partialTour[n-1]][partialTour[0]]
            bestTourSoFar = partialTour.copy()
    else:
        for j in range(currentLevel, n):
            if (costOfPartialTour + distance[partialTour[currentLevel-1]][partialTour[currentLevel]]) < costOfBestTourSoFar :
                swap(partialTour, currentLevel, j)
                costOfPartialTour += distance[partialTour[currentLevel-1]][partialTour[currentLevel]]
                tsp(currentLevel+1)
                costOfPartialTour -= distance[partialTour[currentLevel-1]][partialTour[currentLevel]]
                swap(partialTour, currentLevel, j)

def saleman():
    tsp(1)
    print(bestTourSoFar)
    print(costOfBestTourSoFar)

saleman()
