# Python on Mac OS X Tips

# Installing Modules with pip

## cryptography

Depends on libffi and openssl: `brew install libffi openssl`

### Error: can't find openssl/aes.h

* Solution: `env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" pip install cryptography`
* Found at: <https://github.com/pyca/cryptography/issues/2350>