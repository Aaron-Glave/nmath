class CustomMod(int):
    """Lets you run modulo operations with other starting points other than 0.
    Pass the keyword argument
    For example, if you pass -2, 8 mod 7 is -1."""
    def __new__(cls, *args, **kwargs):
        start_mod = 0
        assert "start_mod" in kwargs.keys()
        rest_kwargs = {k: v for k, v in kwargs.items() if k != "start_mod"}
        to_return = super().__new__(cls, *args, **rest_kwargs)
        start_mod = kwargs["start_mod"]
        to_return.start_mod = start_mod
        return to_return
        

    def __mod__(self, other: int):
        x = int(self)
        result = CustomMod ((x - self.start_mod) % (other-self.start_mod) + self.start_mod, start_mod=self.start_mod)
        #print("Debug", int(result))
        while int(result) < self.start_mod:
            print(result)
            result = CustomMod(super().__add__(int(self.start_mod)), start_mod=self.start_mod)
            print(type(result))
        return result
     
    def __add__(self, other: int):
         #print("add", other)
         added = CustomMod(super().__add__(int(other)), start_mod=self.start_mod)
         return added
    
    def __sub__(self, other: int):
         subbed = CustomMod(super().__sub__(int(other)), start_mod=self.start_mod)
         return subbed
     
    def __init__(self, *args, **kwargs):
         """Note: This class requires a start_mod keyword argument."""
         #print("Making...")
         self.start_mod = kwargs["start_mod"]
         


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if CustomMod(1, start_mod=1) % 7 == CustomMod(1, start_mod=2):
        print(type(CustomMod(1, start_mod=1)), "Checks out.")
    _x = CustomMod(7, start_mod=7)
    print("Type of CustomMod:", type(_x+_x))
    print("Range from 7 to 15 (15 excluded):")
    for _a in range(0, 17):
        _p = (_x+_a)%15
        print(_p)
    print("That going backwards:")
    for _b in range(0, 17):
        _q = (_x-_b)%15
        print(_q)
    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
