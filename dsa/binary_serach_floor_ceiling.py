def find_floor_ceiling(arr, target):
    left, right = 0, len(arr) - 1
    floor, ceiling = -1, -1

    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return (arr[mid], arr[mid])  # Both floor and ceiling = target
        elif arr[mid] < target:
            floor = arr[mid]
            left = mid + 1
        else:
            ceiling = arr[mid]
            right = mid - 1

    return (floor, ceiling)
