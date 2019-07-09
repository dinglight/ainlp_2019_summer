import pickle
import networkx as nx

def load_graph():
    #graph = defaultdict(list)
    f = open('nj_metro.defaultdict', 'rb')
    graph = pickle.load(f)
    f.close()
    return graph

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


def find_all_path(start, end, graph):
    pathes = []

    visited={}
    for f, t in graph.edges():
        if f in visited:
            visited[f].update({t: False})
        else:
            visited.update({f:{t: False}})
        if t in visited:
            visited[t].update({f: False})
        else:
            visited.update({t:{f: False}})

    stack=[]
    stack.append(start)
    while stack:
        curr = stack[-1]
        if curr == end:
            pathes.append(stack.copy());
            stack.pop()
        else:
            next = None
            for nb, eattr in graph[curr].items():
                if (nb not in stack) and (not visited[curr][nb]):
                    next = nb
                    break
            if None == next:
                stack.pop()
                for nb, eattr in graph[curr].items():
                    visited[curr][nb] = False
            else:
                stack.append(next)
                visited[curr][next] = True
    return pathes

def search_by_way(station_from, station_to, graph, by_way):
    new_pathes = []
    pathes = find_all_path(station_from, station_to, graph)
    for path in pathes:
        if set(by_way) <= set(path):
            new_pathes.append(path)
    return new_pathes

if __name__ == '__main__':
    G = load_graph()
    #print(graph)
    print(search('百家湖', '南京站', G, transfer_line_less_first))
    print(search('百家湖', '南京站', G, shortest_path_first))
    print(search_by_way('百家湖', '云锦路', G, ['铁心桥']))
