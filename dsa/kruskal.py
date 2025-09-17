class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return False  # Already connected
        
        # Union by rank
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1
        return True

def kruskal_mst(n, edges):
    """
    :param n: Number of nodes (0 to n-1)
    :param edges: List of [u, v, weight]
    :return: (total_weight, mst_edges)
    """
    dsu = DSU(n)
    edges.sort(key=lambda x: x[2])  # Sort by weight
    mst_edges = []
    total_weight = 0
    
    for u, v, w in edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total_weight += w
            if len(mst_edges) == n - 1:
                break  # MST complete
    
    if len(mst_edges) != n - 1:
        return (float('inf'), [])  # Graph is disconnected
    
    return (total_weight, mst_edges)
