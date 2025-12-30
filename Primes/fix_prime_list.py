""""The goal of this program is to re-write your prime list,
 to guarantee that it's in proper order."""
import sys
from collections import deque
import os

import main

#File I save the fixed sprimelist.txt file to.
#Check it before you rename it to main.SPRIMELIST
FIXED_ISH_NAME = "fix_ish_sprimelist.txt"


def write_backupfile():
    """Writes a copy of the prime list to FIXED_ISH_NAME, skipping prime numbers we've already seen.
    Dad recommended to use the sort() function instead."""
    input_line_number = 0
    output_line_number = 0
    #set_prime_nums has the last 64 tuples (nth_prime, prime)
    set_prime_nums = deque()

    with open(FIXED_ISH_NAME, "w", encoding='ascii') as f:
        for nth_prime, prime in main.yield_and_write_primes(
                upto=main.get_last_prime()[1], list_all=True):
            if nth_prime <= 25:
                continue

            #Now we know we're reading lines from the file.
            input_line_number += 1  #We're gonna start at line 1.
            repeated_prime = False
            for found_already in set_prime_nums:
                if prime == found_already[1]:
                    print(f"Error: Found {found_already[1]} at line {input_line_number},",
                          f"but already found at line {found_already[0]}")
                    repeated_prime = True
                    break
            if repeated_prime:
                continue

            #ADD NEW PRIME TO DEQUE AND FIXED_ISH_NAME FILE
            if len(set_prime_nums) >= 25:
                set_prime_nums.popleft()
            set_prime_nums.append((nth_prime, prime))
            f.write(f"{nth_prime} {prime}\n")
            output_line_number += 1
            if output_line_number % 10000 == 0:
                print(f"Written {output_line_number} lines")


if __name__ == "__main__":
    if FIXED_ISH_NAME in os.listdir():
        print(f"Somewhat fixed {FIXED_ISH_NAME} exists.")
        should_rewrite = input("Do you want to rewrite that file? (y/n) ")
        if should_rewrite != "y":
            sys.exit()
    write_backupfile()
