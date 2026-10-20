import sys

data = sys.stdin.read().split()
n = int(data[0])
parent = list(range(n + 1))


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


nums = data[1:]
for i in range(0, len(nums) - 1, 2):
    a, b = find(int(nums[i])), find(int(nums[i + 1]))
    if a != b:
        parent[a] = b

components = len({find(i) for i in range(1, n + 1)})
print(components - 1)
