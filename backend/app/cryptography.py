import math
import random


PRIVATE_KEY_PATH = 'Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/private_key.txt'
PUBLIC_KEY_PATH = 'Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/public_key.txt'
N_PATH = 'Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/n.txt'
prime = set()


def primefiller():
    sieve = [True] * 250
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(250)) + 1):
        if sieve[i]:
            for j in range(i * i, 250, i):
                sieve[j] = False
    for i in range(250):
        if sieve[i]:
            prime.add(i)


def pickrandomprime():
    k = random.randint(0, len(prime) - 1)
    it = iter(prime)
    for _ in range(k):
        next(it)
    ret = next(it)
    prime.remove(ret)
    return ret


def generate_keys():
    primefiller()
    prime1 = pickrandomprime() 
    prime2 = pickrandomprime() 
    n = prime1 * prime2
    fi = (prime1 - 1) * (prime2 - 1)
    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1
    public_key = e
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1
    private_key = d
    with open(PUBLIC_KEY_PATH, 'w') as file:
        file.write(str(public_key))
    with open(PRIVATE_KEY_PATH, 'w') as file2:
        file2.write(str(private_key))
    with open(N_PATH, 'w') as file3:
        file3.write(str(n))


def load_keys():
    try:
        with open(PUBLIC_KEY_PATH, 'r') as file:
            public_key = int(file.read())
        with open(PRIVATE_KEY_PATH, 'r') as file2:
            private_key = int(file2.read())
        with open(N_PATH, 'r') as file3:
            n = int(file3.read())
        return public_key, private_key, n
    except FileNotFoundError:
        generate_keys()
        return load_keys()


def mod_exp(base, exp, mod):
    
    base = int(base)
    mod = int(mod)
    result = 1
    base = base % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result


def encrypt(message, public_key, n):
    return mod_exp(message, public_key, n)


def decrypt(encrypted_text, private_key, n):
    return mod_exp(encrypted_text, private_key, n)


def encoder(message, public_key, n):
    encoded = []
    for letter in message:
        encoded.append(encrypt(ord(letter), public_key, n))
    return encoded


def decoder(encoded, private_key, n):
    decoded = ''
    for num in encoded:
        decoded += chr(decrypt(num, private_key, n))
    return decoded


def undo_joined_message(joined_message):
    return [int(p) for p in joined_message.split()]