import time


class PrimeIterator:
    MAX_SIZE = 2560000
    def __init__(self):
        self.prime_files_names = []
        self.current_size = 0
        # TODO Would it help to add a dictionary of {prime_list_name: last nth_prime in the file
        try:
            num_prime_files_file = open("Storage/num_prime_files.txt", "r")
            self.num_prime_files = int(num_prime_files_file.readline())
            num_prime_files_file.close()
        except FileNotFoundError:
            self.num_prime_files = 0
            self._new_file()
        #last = open(, "r")
        last = open(self.prime_files_names[-1], "r")

    def _new_file(self):
        self.num_prime_files += 1
        new_file_name = f"Storage/sprimelist{self.num_prime_files}.txt"
        print(f"Creating {new_file_name}.")
        open(new_file_name, mode="w", encoding='ascii').close()
        self.current_size = 0
        self.prime_files_names.append(new_file_name)
        with open("num_prime_files.txt", mode="w", encoding='ascii') as num_prime_files_file:
            num_prime_files_file.write(str(self.num_prime_files))

    def add_new_prime(self, prime: tuple[int, int]):
        """Adds a new prime to the list.
        Expected format: A tuple of 2 integers: (nth_prime, prime)
        Example arg: (26, 101)
        101 is the 26th prime number."""
        new_line = f"{prime[0]} {prime[1]}\n"
        self.current_size += len(new_line)
        if self.current_size > self.MAX_SIZE:
            self._new_file()
        _have_to_write = True
        while _have_to_write:
            try:
                with open(self.prime_files_names[-1], mode="a+", encoding='ascii') as file_to_print_to:
                    file_to_print_to.write(new_line)
                _have_to_write = False
            except PermissionError as e:
                print(e)
                time.sleep(1)


    def iterate_written_primes(self):
        for name in self.prime_files_names:
            _check = open(name, mode="r", encoding='ascii')
            for line in _check:
                nth_prime, prime = map(int, line.strip('\n').split(' '))
                yield nth_prime, prime


def import_list(filename: str) -> None:
    file = open(filename, mode="r", encoding='ascii')
    db = PrimeIterator()
    sofar = 0
    try:
        for line in file:
            nth_prime, prime = map(int, line.strip('\n').split(' '))
            sofar += 1
            if sofar % 1000 == 0:
                print(f"Wrote {sofar} primes so far. Size: {db.current_size/(1000**2)}")
            db.add_new_prime((nth_prime, prime))
    finally:
        file.close()



if __name__ == "__main__":
    primes = PrimeIterator()
    print(primes.MAX_SIZE)
