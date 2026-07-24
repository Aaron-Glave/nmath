"""Compute the number of ways to select a subset of items from a greater set,
regarding or disregarding the order of items."""
from math import factorial

def _nr_safety(num_items: int, sum_items_to_pick: int, len_group_list: int) -> None:
    if num_items < 0:
        raise ValueError("n can't be negative")
    if sum_items_to_pick > num_items:
        raise ValueError("r can't be greater than n")
    if len_group_list < 1:
        raise ValueError("You have to select at least one group of items in the set.")


def nPr(n: int, *nums_to_pick: int):
    """Number of ways to select a sequence of items from a greater set,
     paying attention to the order of selected items.
     e.g. 1,2,3 and 1,3,2 are 2 different sequences."""
    _nr_safety(n, sum(nums_to_pick), len(nums_to_pick))
    if n == 0:
        return 1
    nf = factorial(n)
    divisor = factorial(n - sum(nums_to_pick))
    return nf // divisor


def nCr(n: int, *nums_to_pick: int) -> int:
    """Number of ways to select a subset of items from a greater set,
    disregarding the order of items."""
    _nr_safety(n, sum(nums_to_pick), len(nums_to_pick))
    if n == 0:
        return 1
    divisor = 1
    for num in nums_to_pick:
        divisor *= factorial(num)
    ordered_set = nPr(n, *nums_to_pick)
    return ordered_set // divisor
