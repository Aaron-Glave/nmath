class PhoneBanned(Exception):
    def __init__(self):
        super().__init__("Illegal to use this function on a phone.")
