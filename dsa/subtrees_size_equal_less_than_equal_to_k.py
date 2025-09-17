from collections import defaultdict


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


class Solution:
    def __init__(self, K) -> None:
        self.result = 0
        self.k = K

    def count_subtrees(self, root):
        def dfs(node):
            # count[k] = number of connected subtrees rooted at `node` with size `k`
            count = defaultdict(int)
            count[1] = 1  # A single node itself is a valid subtree of size 1

            for child in node.children:
                child_count = dfs(child)

                # Combine current `count` and `child_count`
                new_count = defaultdict(int)

                for size1 in count:
                    for size2 in child_count:
                        if size1 + size2 <= self.k:
                            new_count[size1 + size2] += (
                                count[size1] * child_count[size2]
                            )

                # Merge new_count into count
                for size in new_count:
                    count[size] += new_count[size]

            # Add all subtree counts rooted at this node to global result
            for size in count:
                if size <= self.k:
                    self.result += count[size]

            return count

        dfs(root)
        return self.result


root = TreeNode(1)
child1 = TreeNode(2)
child2 = TreeNode(3)

root.children = [child1, child2]
# child1.children = [child3]

K = 2
sol = Solution(K)
print(sol.count_subtrees(root))
