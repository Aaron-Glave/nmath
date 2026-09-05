import sys

#A very big number for a computer.
def huge_number(saystuff=False):
    if saystuff:
        print(sys.maxsize)
    big_number = sys.maxsize
    #will fail
    try:
        #Store all characters of an extremely large number, but ignore the result.
        _ = str((big_number**1000))
    except ValueError:
        if saystuff:
            print("Ints need to be larger!")
        sys.set_int_max_str_digits(100000)
        if saystuff:
            print(big_number**1000)

if __name__ == '__main__':
    huge_number(saystuff=True)
