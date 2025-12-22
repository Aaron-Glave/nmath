#Returns tuple(int, tuple(int, int))
def two_in_down(left: int, right: int):
    decreased = False
    if left <= 0 and right <= 0:
        decreased = True
    my_nums = (left, right)
    positive_after_decreased = False
    prev = None
    while True:
        current = my_nums[0]*my_nums[1]
        if prev is not None:
            if (current < prev) and not decreased:
                decreased = True
            elif decreased:
                if current > prev:
                    positive_after_decreased = True
        yield current, (my_nums[0], my_nums[1])
        if positive_after_decreased:
            return
        prev = current
        my_nums = (my_nums[0]-1, my_nums[1]-1)

if __name__ == '__main__':
    lowest = None
    debug = False
    for i in two_in_down(111,7):
        if lowest is None:
            lowest = i
        elif i < lowest:
            lowest = i
        print(i)
    if debug:
        for i in two_in_down(0, 0):
            print(i)
        for i in two_in_down(7, 1):
            print(i)
    print("Lowest in series of decreasing products of 111 and 7 with both decreasing is", lowest)