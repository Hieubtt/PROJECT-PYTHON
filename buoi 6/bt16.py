# Cho dictionary biểu diễn đồ thị (key là node, value là list các node kề). 
# Viết hàm tìm tất cả đường đi từ node A đến node B mà không đi qua node nào quá 1 lần.
# # Test 
graph = { 
    'A': ['B', 'C'], 
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'], 
    'E': ['B', 'F'], 
    'F': ['C', 'E'] 
}

for keys,values in graph.items():
    print(keys, ' ' ,values )
    for values in graph[keys]:
        print('Giá trị trong dict ',values )


def func_find_node(graph,start,end):
    path_all = [] #luu duong dan node tim dc
    visited = set() #luu cac node da di qua

    def dfs(node,path):
        path.append( node)
        visited.add( node)
        print('path ' , path)
        print('visited '  , visited)
        if node == end:
                path_all.append(path.copy())
        else:
            for nodes in graph[node]:
                if nodes not in visited:    
                    dfs(nodes,path)

        path.pop()
        visited.remove(node)

    dfs(start, [])
    return path_all


paths = func_find_node(graph, 'A', 'C')
print(paths)
for p in paths:
    print(p)

    