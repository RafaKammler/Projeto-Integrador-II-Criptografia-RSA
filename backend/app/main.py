import math
import random
from flask import Flask, request, jsonify
from base64 import b64encode, b64decode
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
prime = set()
PRIVATE_KEY_PATH = 'private_key.txt'
PUBLIC_KEY_PATH = 'public_key.txt'
N_PATH = 'n.txt'

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

public_key, _, n = load_keys()

@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    generate_keys()
    public_key, private_key, _ = load_keys()
    return jsonify({'public_key': public_key, 'private_key': private_key})

@app.route('/get_public_key_input', methods=['GET'])
def get_public_key_input_route():
    data = request.get_json()
    public_key = data.get('public_key')
    private_key = data.get('private_key')
    
    return jsonify({'message': 'Keys received successfully', 'public_key': public_key, 'private_key': private_key})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.json
    message = data['message']
    with open(N_PATH, 'r') as f:
        n = int(f.read())

    encrypted_message = [pow(ord(char), public_key, n) for char in message]

    encrypted_message_bytes = b''.join(int.to_bytes(num, (num.bit_length() + 7) // 8, 'big') for num in encrypted_message)
    encrypted_message_b64 = b64encode(encrypted_message_bytes).decode('utf-8')
    
    return jsonify({'encrypted_text': encrypted_message_b64})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    global private_key
    data = request.json
    encrypted_text = b64decode(data['encrypted_text'])
    with open(N_PATH, 'r') as f:
        n = int(f.read())

    decrypted_message = ''.join(chr(pow(int.from_bytes(encrypted_text[i:i+256], 'big'), private_key, n)) for i in range(0, len(encrypted_text), 256))
    
    return jsonify({'decrypted_text': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)