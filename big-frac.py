if __name__ == '__main__':
    num = 1
    denom = 2
    a_sum = 0
    steps = 20
    print("Starting at", a_sum)
    for step in range(1, 1+steps):
        print("Adding 1 /", f"({num * denom})")
        a_sum += (1 /
                  (num * denom))
        num = denom
        denom += 1
        print("So far:", a_sum)
    print("Never passes 1. Σ_(n=1->∞)(1/(n(n+1))) = 1")