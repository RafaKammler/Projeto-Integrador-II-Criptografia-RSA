import React, { useState } from 'react';

function App() {
  const [publicKeyGenerated, setPublicKeyGenerated] = useState('');
  const [publicKeyInput, setPublicKeyInput] = useState('');
  const [privateKeyInput, setPrivateKeyInput] = useState('');
  const [privateKeyGenerated, setPrivateKeyGenerated] = useState('');
  const [message, setMessage] = useState('');
  const [encryptedText, setEncryptedText] = useState('');
  const [decryptedText, setDecryptedText] = useState('');
  const [data, setData] = useState('');

  const generateKeys = async () => {
    try {
      const response = await fetch('http://localhost:5000/generate_keys', { method: 'POST' });
      const data = await response.json();
      setPublicKeyGenerated(data.public_key);
      setPrivateKeyGenerated(data.private_key);
    } catch (error) {
      console.error('Error generating keys:', error);
    }
  };

  const sendInputPublicKey = async (publicKey) => {
    try {
      const response = await fetch('http://localhost:5000/get_public_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ public_key: publicKey })
      });
      const data = await response.json();
      setData(data);
      return data;
    } catch (error) {
      console.error('Error sending public key:', error);
    }
  };

  const sendInputPrivateKey = async (privateKey) => {
    try {
      const response = await fetch('http://localhost:5000/get_private_key_input', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ private_key: privateKey })
      });
      const data = await response.json();
      setData(data);
      return data;
    } catch (error) {
      console.error('Error sending private key:', error);
    }
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
    try {
      const response = await fetch('http://localhost:5000/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({encryptedText})
      });
      const data = await response.json();
      setDecryptedText(data.decrypted_message);
    } catch (error) {
      console.error('Error decrypting message:', error);
    }
  };

  const handleEncryptClick = async () => {
    await sendInputPublicKey(publicKeyInput);
    await encryptMessage();
  };

  const handleDecryptClick = async () => {
    await sendInputPrivateKey(privateKeyInput);
    await decryptMessage();
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
          type="text"
          value={publicKeyInput}
          onChange={(e) => setPublicKeyInput(e.target.value)}
          placeholder="Enter public key"
        />
        <button onClick={handleEncryptClick}>Encrypt</button>
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
          type="text"
          value={privateKeyInput}
          onChange={(e) => setPrivateKeyInput(e.target.value)}
          placeholder="Enter private key"
        />
        <button onClick={handleDecryptClick}>Decrypt</button>
        <p>Decrypted Text: {decryptedText}</p>
      </div>
    </div>
  );
}

export default App;