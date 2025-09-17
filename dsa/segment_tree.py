class SegmentTree:
    def __init__(self,nums:list) -> None:
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.build(nums,0,0,self.n-1)

    def build(self,nums:list,node_idx,l,r):

        if l == r:
            self.tree[node_idx] = nums[l]
            return
        
        mid = (l+r)//2

        # left idx is 2 * node_idx +1
        self.build(nums,(2 * node_idx) + 1,0,mid)
        self.build(nums,(2 * node_idx) + 2,mid+1,self.n)

        # here is the main logic for sum 
        # self.tree[node_idx] = self.tree[(2 * node_idx) + 1] + self.tree[(2 * node_idx) + 2]

        # here is the main logic for max 
        self.tree[node_idx] = max(self.tree[(2 * node_idx) + 1], self.tree[(2 * node_idx) + 2])

    def query(self, ql, qr, node=0, l=0, r=None):
        if r is None:
            r = self.n - 1
        if qr < l or ql > r:
            return 0
        if ql <= l and r <= qr:
            return self.tree[node]
        mid = (l + r) // 2
        left = self.query(ql, qr, 2 * node + 1, l, mid)
        right = self.query(ql, qr, 2 * node + 2, mid + 1, r)
        return max(left , right)

