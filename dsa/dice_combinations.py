import sys
import threading


def main():
    import math
    from collections import defaultdict, deque, Counter
    from bisect import bisect_left, bisect_right
    from heapq import heappush, heappop
    from functools import lru_cache

    MOD = 10**9 + 7

    sys.setrecursionlimit(10**6)
    input = sys.stdin.readline

    n = int(input())

    def solve():
        coins = [1, 2, 3, 4, 5, 6]
        dp = [0] * (n + 1)
        dp[0] = 1

        for s in range(1, n + 1):
            for coin in coins:
                if s >= coin:
                    dp[s] = (dp[s] + dp[s - coin]) % MOD

        print(dp[n])

    solve()


# For faster execution in large input cases
if __name__ == "__main__":
    threading.Thread(target=main).start()
