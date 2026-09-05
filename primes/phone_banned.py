"""A simple exception class to prevent inappropriate phone usage."""
class PhoneBanned(Exception):
    """No arguments required."""
    def __init__(self):
        super().__init__("Illegal to use this function on a phone.")
