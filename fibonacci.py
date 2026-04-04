a = 1
b = a
sequence = [a, b]
def add_swap():
    global a, b, sequence
    temp = a
    a = b
    b = temp + b
    sequence.append(b)

continueadding = True
print("This is the Fibonacci sequence.")
print("It starts with ", a, ", ", b, sep='', end=".\n")
print("How long do you want it to be?")
wantedlength = int(input())
length = 2
while len(sequence) < wantedlength:
    add_swap()
print("Calculated Fibonacci sequence:", sequence)