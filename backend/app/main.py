from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography import generate_keys, load_keys, encoder, decoder, undo_joined_message


app = Flask(__name__)
CORS(app)


N_PATH = 'Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/n.txt'
PUBLIC_KEY_INPUT = "Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/public_key_input.txt"
PRIVATE_KEY_INPUT = "Projeto-Integrador-II-Criptografia-RSA/backend/app/keys/private_key_input.txt"


_, _, n = load_keys()


@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    generate_keys()
    public_key, private_key, _ = load_keys()
    return jsonify({'public_key': public_key, 'private_key': private_key})


@app.route('/get_public_key_input', methods=['POST'])
def get_public_key_input_route():
    data = request.get_json()
    public_key = int(data.get('public_key'))

    with open(PUBLIC_KEY_INPUT, 'w') as f:
        f.write(str(public_key))


    return jsonify({'message': 'Keys received successfully', 'public_key': public_key})

@app.route('/get_private_key_input', methods=['POST'])
def get_private_key_input_route():
    data = request.get_json()
    private_key = int(data.get('private_key'))

    with open(PRIVATE_KEY_INPUT, 'w') as f:
        f.write(str(private_key))


    return jsonify({'message': 'Keys received successfully', 'private_key': private_key})

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.json
    message = data['message']

    with open(N_PATH, 'r') as f:
        n = int(f.read())
    with open(PUBLIC_KEY_INPUT, 'r') as f:
        public_key = int(f.read())

    message_crypto = encoder(message, public_key, n)
    encrypted_message = (' '.join(str(p) for p in message_crypto))


    return jsonify({'encrypted_text': encrypted_message})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    data = request.json
    message = data['encryptedText']
    with open(N_PATH, 'r') as f:
        n = int(f.read())
    with open(PRIVATE_KEY_INPUT, 'r') as f:
        private_key = int(f.read())
    message_original = undo_joined_message(message)
    decrypted_message = decoder(message_original, private_key, n)
    return jsonify({'decrypted_message': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True)