# A better way to generate prime numbers is with [openSSL](https://openssl-library.org/). 
You can easily get a product of 2 huge prime number for RSA from the Git command line running `openssl genrsa 2048`. It will be a product of 2 2048-bit primes, printed out in base64 format.
- You can install the Git command line here: [`https://git-scm.com/install/`](https://git-scm.com/install/)
- You can also run `openssl prime -generate -bits` followed by the number of bits in a prime number you want to generate!
