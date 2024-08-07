import React, { useState } from 'react';

function App() {
  const [publicKeyGenerated, setPublicKeyGenerated] = useState('');
  const [publicKeyInput, setPublicKeyInput] = useState('');
  const [privateKeyInput, setPrivateKeyInput] = useState('');
  const [privateKeyGenerated, setPrivateKeyGenerated] = useState('');
  const [message, setMessage] = useState('');
  const [encryptedText, setEncryptedText] = useState('');
  const [decryptedText, setDecryptedText] = useState('');

  const generateKeys = async () => {
    const response = await fetch('http://localhost:5000/generate_keys', { method: 'POST' });
    const data = await response.json();
    setPublicKeyGenerated(data.public_key);
    setPrivateKeyGenerated(data.private_key);
  };
  const sendInputKeys = async (publicKey, privateKey) => {
    const response = await fetch('http://localhost:5000/get_public_key_input', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            public_key: publicKey,
            private_key: privateKey
        })
    });

    const data = await response.json();
    return data;
};
  const encryptMessage = async () => {
    try {
      const response = await fetch('http://localhost:5000/encrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      setEncryptedText(data.encrypted_text);
    } catch (error) {
      console.error('Error encrypting message:', error);
    }
  };

  const decryptMessage = async () => {
    const response = await fetch('http://localhost:5000/decrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ encrypted_text: encryptedText })
    });
    const data = await response.json();
    setDecryptedText(data.decrypted_text);
  };

  return (
    <div>
      <h1>RSA Encryption Demo</h1>
      <div>
        <h2>Generate Keys</h2>
        <button onClick={generateKeys}>Generate Keys</button>
        <p>Public Key: {publicKeyGenerated}</p>
        <p>Private Key: {privateKeyGenerated}</p>
      </div>
      <div>
        <h2>Encrypt Message</h2>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter message"
        />
        <input
          type="int"
          value={publicKeyInput}
          onChange={(e) => setPublicKeyInput(e.target.value)}
          placeholder="Enter public key"
        />
        <button onClick={sendInputKeys}>Encrypt</button>
        <p>Encrypted Text: {encryptedText}</p>
      </div>
      <div>
        <h2>Decrypt Message</h2>
        <input
          type="text"
          value={encryptedText}
          onChange={(e) => setEncryptedText(e.target.value)}
          placeholder="Enter encrypted message"
        />
        <input
          type="int"
          value={privateKeyInput}
          onChange={(e) => setPrivateKeyInput(e.target.value)}
          placeholder="Enter Private key"
        />
        <button onClick={decryptMessage}>Decrypt</button>
        <p>Decrypted Text: {decryptedText}</p>
      </div>
    </div>
  );
}

export default App;