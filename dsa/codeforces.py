import sys
import threading


def main():
    import sys

    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        n = int(input())

        ans = 0
        arr = list(map(int, input().split()))

        for tmp in arr:
            ans += tmp + (tmp == 0)

        print(ans)


if __name__ == "__main__":
    threading.Thread(target=main).start()
