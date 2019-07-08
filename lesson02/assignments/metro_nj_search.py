import pickle
import networkx as nx

def load_graph():
    #graph = defaultdict(list)
    f = open('nj_metro.defaultdict', 'rb')
    graph = pickle.load(f)
    f.close()
    return graph

def search(station_from, station_to, graph, sort_candidate):
    pathes = [[station_from]]

    visitied = set()

    while pathes: # if we find existing pathes
        path = pathes.pop(0)
        froninter = path[-1]

        if froninter in visitied: continue

        successors = graph[froninter]

        for station, eattr in successors.items():
            if station in path: continue  # eliminate loop
            new_path = path + [station]
            pathes.append(new_path)
            #print(new_path)
            if station == station_to: return new_path

        visitied.add(froninter)

        pathes = sort_candidate(graph, pathes) # 我们可以加一个排序函数 对我们的搜索策略进行控制

def transfer_line_less_first(graph, pathes):
    if len(pathes) <= 1: return pathes

    def get_switch_num(path):
        switch = 0
        last_line = graph.edges[path[0], path[1]]['line']

        for i, station in enumerate(path[:-1]):
            if i == 0:
                continue
            else:
                if last_line != graph.edges[station, path[i+1]]['line']:
                    switch += 1
                    last_line = graph.edges[path[0], path[1]]['line']

        return switch

    return sorted(pathes, key=get_switch_num)


def shortest_path_first(graph, pathes):
    if len(pathes) <= 1: return pathes

    def get_path_distnace(path):
        distance = 0
        for i, station in enumerate(path[:-1]):
            distance += graph.edges[station, path[i+1]]['weight']

        return distance

    return sorted(pathes, key=get_path_distnace)

if __name__ == '__main__':
    G = load_graph()
    #print(graph)
    print(search('百家湖', '南京站', G, transfer_line_less_first))
    print(search('百家湖', '南京站', G, shortest_path_first))
