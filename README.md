# A better way to generate prime numbers is with [openSSL](https://openssl-library.org/). 
You can easily get a product of 2 huge prime numbers for RSA from the Git command line running `openssl genrsa 2048`. It will be a product of 2 2048-bit prime numbers, printed out in base64 format.
- You can install the Git command line here: [`https://git-scm.com/install/`](https://git-scm.com/install/)
- You can also run `openssl prime -generate -bits` followed by the number of bits in a prime number you want to generate!

Also, if you just want to find the _nth_ prime number, check out [`https://t5k.org/nthprime/`](https://t5k.org/nthprime/)!
# Because I'm talking about encyption anyways, here are commands you can use to generate EC public and private keys with openssl
1. `openssl ecparam -name secp521r1 -genkey -out key.pem` generates a private key with a NIST/SECG curve over a 521 bit prime field.
2. Then `openssl ec -in key.pem -pubout -out public.pem` generates a public key.
