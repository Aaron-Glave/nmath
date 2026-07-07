from math import factorial

def nCr(num_items: int, *nums_to_pick: int) -> int:
    """Number of ways to select  """
    if num_items < 0:
        raise ValueError("n can't be negative")
    sum_items_to_pick = sum(nums_to_pick)
    if sum_items_to_pick > num_items:
        raise ValueError("r can't be greater than n")
    if len(nums_to_pick) < 1:
        raise ValueError("You have to select at least one group of items in the set.")
    if num_items == 0:
        return 1
    n = factorial(num_items)
    divisor = 1
    items_not_picked = num_items
    for num in nums_to_pick:
        divisor *= factorial(num)
        items_not_picked -= num
    divisor *= factorial(items_not_picked)
    return n//divisor

if __name__ == "__main__":
    '''example usage:'''#LATER