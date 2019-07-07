import pickle
from collections import defaultdict

def load_graph():
    #graph = defaultdict(list)
    f = open('nj_metro.defaultdict', 'rb')
    graph = pickle.load(f)
    f.close()
    return graph

def search(station_from, station_to, graph):
    pathes = [[station_from]]
    visitied = set()

    while pathes:
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        successors = graph[froninter]
        for station, distance in successors:
            if station in path: continue  # eliminate loop
            new_path = path + [station]
            pathes.append(new_path)
            #print(new_path)
            if station == station_to: return new_path

        visitied.add(froninter)

if __name__ == '__main__':
    graph = load_graph()
    #print(graph)
    print(search('百家湖', '南京站', graph))
