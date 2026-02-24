# A better way to generate prime numbers is with [openSSL](https://openssl-library.org/). 
You can easily get a product of 2 huge prime numbers for RSA from the Git command line running `openssl genrsa 2048`. It will be a product of 2 2048-bit prime numbers, printed out in base64 format.
- You can install the Git command line here: [`https://git-scm.com/install/`](https://git-scm.com/install/)
- You can also run `openssl prime -generate -bits` followed by the number of bits in a prime number you want to generate!

Also, if you just want to find the _nth_ prime number, check out [`https://t5k.org/nthprime/`](https://t5k.org/nthprime/)!
