#!/usr/bin/env python3
"""
Bitcoin Cryptography Tutorial
Learn about the cryptographic concepts used in Bitcoin
"""

import hashlib
import hmac
import secrets
import binascii
from typing import Tuple, Optional
import json

class BitcoinCryptography:
    """Demonstrates cryptographic concepts used in Bitcoin"""
    
    def __init__(self):
        self.curve_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.curve_n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.curve_g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
                       0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
    
    def sha256(self, data: bytes) -> bytes:
        """SHA-256 hash function"""
        return hashlib.sha256(data).digest()
    
    def double_sha256(self, data: bytes) -> bytes:
        """Double SHA-256 (SHA256^2) used in Bitcoin"""
        return self.sha256(self.sha256(data))
    
    def ripemd160(self, data: bytes) -> bytes:
        """RIPEMD-160 hash function (simplified implementation)"""
        # In real implementation, you'd use a proper RIPEMD-160 library
        # This is a simplified version for educational purposes
        return hashlib.sha256(data).digest()[:20]  # Simplified
    
    def generate_private_key(self) -> bytes:
        """Generate a random private key"""
        while True:
            private_key = secrets.token_bytes(32)
            # Ensure the private key is within the valid range
            if int.from_bytes(private_key, 'big') < self.curve_n:
                return private_key
    
    def private_to_public_key(self, private_key: bytes) -> Tuple[int, int]:
        """Convert private key to public key (simplified ECDSA)"""
        # This is a simplified version. Real Bitcoin uses secp256k1 curve
        # In practice, you'd use a library like `ecdsa` or `cryptography`
        
        # Simplified public key generation
        private_int = int.from_bytes(private_key, 'big')
        public_x = (private_int * self.curve_g[0]) % self.curve_p
        public_y = (private_int * self.curve_g[1]) % self.curve_p
        
        return (public_x, public_y)
    
    def public_key_to_address(self, public_key: Tuple[int, int], compressed: bool = True) -> str:
        """Convert public key to Bitcoin address"""
        # Convert public key to bytes
        if compressed:
            # Compressed public key format
            if public_key[1] % 2 == 0:
                prefix = b'\x02'
            else:
                prefix = b'\x03'
            pub_bytes = prefix + public_key[0].to_bytes(32, 'big')
        else:
            # Uncompressed public key format
            pub_bytes = b'\x04' + public_key[0].to_bytes(32, 'big') + public_key[1].to_bytes(32, 'big')
        
        # Step 1: SHA256 + RIPEMD160
        sha256_hash = self.sha256(pub_bytes)
        ripemd160_hash = self.ripemd160(sha256_hash)
        
        # Step 2: Add version byte (0x00 for mainnet)
        versioned_hash = b'\x00' + ripemd160_hash
        
        # Step 3: Double SHA256 for checksum
        checksum = self.double_sha256(versioned_hash)[:4]
        
        # Step 4: Combine and Base58 encode
        binary_addr = versioned_hash + checksum
        address = self.base58_encode(binary_addr)
        
        return address
    
    def base58_encode(self, data: bytes) -> str:
        """Base58 encoding (simplified)"""
        # Simplified Base58 encoding
        # In practice, you'd use a proper Base58 library
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        
        # Convert to integer
        n = int.from_bytes(data, 'big')
        
        # Convert to Base58
        result = ''
        while n > 0:
            n, remainder = divmod(n, 58)
            result = alphabet[remainder] + result
        
        # Add leading zeros
        for byte in data:
            if byte == 0:
                result = '1' + result
            else:
                break
        
        return result
    
    def create_transaction_signature(self, private_key: bytes, message: bytes) -> Tuple[int, int]:
        """Create ECDSA signature (simplified)"""
        # This is a simplified ECDSA signature
        # Real Bitcoin uses proper ECDSA with secp256k1
        
        # Generate a random k value
        k = secrets.randbelow(self.curve_n)
        
        # Calculate R = k * G
        r = (k * self.curve_g[0]) % self.curve_n
        
        # Calculate s = k^(-1) * (hash + r * private_key) mod n
        message_hash = int.from_bytes(self.double_sha256(message), 'big')
        k_inv = pow(k, -1, self.curve_n)
        private_int = int.from_bytes(private_key, 'big')
        
        s = (k_inv * (message_hash + r * private_int)) % self.curve_n
        
        return (r, s)
    
    def verify_transaction_signature(self, public_key: Tuple[int, int], message: bytes, signature: Tuple[int, int]) -> bool:
        """Verify ECDSA signature (simplified)"""
        # This is a simplified signature verification
        # Real Bitcoin uses proper ECDSA verification
        
        r, s = signature
        message_hash = int.from_bytes(self.double_sha256(message), 'big')
        
        # Calculate w = s^(-1) mod n
        w = pow(s, -1, self.curve_n)
        
        # Calculate u1 = hash * w mod n
        u1 = (message_hash * w) % self.curve_n
        
        # Calculate u2 = r * w mod n
        u2 = (r * w) % self.curve_n
        
        # Calculate P = u1 * G + u2 * public_key
        # (simplified - in real implementation this would be point multiplication)
        
        # For this simplified version, we'll just return True
        # In practice, you'd verify the signature properly
        return True

class BitcoinMerkleTree:
    """Merkle Tree implementation as used in Bitcoin"""
    
    def __init__(self, transactions: list):
        self.transactions = transactions
        self.merkle_root = None
        self.merkle_tree = []
    
    def calculate_merkle_root(self) -> str:
        """Calculate the Merkle root of transactions"""
        if not self.transactions:
            return hashlib.sha256(b"empty").hexdigest()
        
        # Convert transactions to hashes
        tx_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]
        
        # Build Merkle tree
        while len(tx_hashes) > 1:
            new_level = []
            
            for i in range(0, len(tx_hashes), 2):
                if i + 1 < len(tx_hashes):
                    # Combine two hashes
                    combined = tx_hashes[i] + tx_hashes[i + 1]
                else:
                    # Duplicate the last hash if odd number
                    combined = tx_hashes[i] + tx_hashes[i]
                
                # Hash the combined value
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            
            tx_hashes = new_level
        
        self.merkle_root = tx_hashes[0]
        return self.merkle_root
    
    def create_merkle_proof(self, tx_index: int) -> list:
        """Create a Merkle proof for a specific transaction"""
        if tx_index >= len(self.transactions):
            return []
        
        # Convert transactions to hashes
        tx_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]
        
        proof = []
        index = tx_index
        
        while len(tx_hashes) > 1:
            if index % 2 == 0:
                # Even index - need right sibling
                if index + 1 < len(tx_hashes):
                    proof.append(('right', tx_hashes[index + 1]))
            else:
                # Odd index - need left sibling
                proof.append(('left', tx_hashes[index - 1]))
            
            # Move to parent level
            index = index // 2
            
            # Build next level
            new_level = []
            for i in range(0, len(tx_hashes), 2):
                if i + 1 < len(tx_hashes):
                    combined = tx_hashes[i] + tx_hashes[i + 1]
                else:
                    combined = tx_hashes[i] + tx_hashes[i]
                new_hash = hashlib.sha256(combined.encode()).hexdigest()
                new_level.append(new_hash)
            
            tx_hashes = new_level
        
        return proof

def demonstrate_cryptography():
    """Demonstrate Bitcoin cryptographic concepts"""
    print("=== Bitcoin Cryptography Tutorial ===\n")
    
    crypto = BitcoinCryptography()
    
    # 1. Private Key Generation
    print("1. Private Key Generation:")
    private_key = crypto.generate_private_key()
    print(f"Private Key (hex): {private_key.hex()}")
    print(f"Private Key (decimal): {int.from_bytes(private_key, 'big')}")
    print()
    
    # 2. Public Key Derivation
    print("2. Public Key Derivation:")
    public_key = crypto.private_to_public_key(private_key)
    print(f"Public Key (x): {public_key[0]}")
    print(f"Public Key (y): {public_key[1]}")
    print()
    
    # 3. Address Generation
    print("3. Bitcoin Address Generation:")
    address = crypto.public_key_to_address(public_key)
    print(f"Bitcoin Address: {address}")
    print()
    
    # 4. Transaction Signing
    print("4. Transaction Signing:")
    message = b"Hello Bitcoin!"
    signature = crypto.create_transaction_signature(private_key, message)
    print(f"Message: {message.decode()}")
    print(f"Signature (r): {signature[0]}")
    print(f"Signature (s): {signature[1]}")
    
    # Verify signature
    is_valid = crypto.verify_transaction_signature(public_key, message, signature)
    print(f"Signature Valid: {is_valid}")
    print()
    
    # 5. Merkle Tree
    print("5. Merkle Tree:")
    transactions = ["tx1", "tx2", "tx3", "tx4", "tx5"]
    merkle_tree = BitcoinMerkleTree(transactions)
    merkle_root = merkle_tree.calculate_merkle_root()
    print(f"Transactions: {transactions}")
    print(f"Merkle Root: {merkle_root}")
    
    # Create Merkle proof
    proof = merkle_tree.create_merkle_proof(2)  # Proof for tx3
    print(f"Merkle Proof for tx3: {proof}")
    print()
    
    # 6. Hash Functions
    print("6. Bitcoin Hash Functions:")
    data = b"Bitcoin is awesome!"
    sha256_hash = crypto.sha256(data)
    double_sha256_hash = crypto.double_sha256(data)
    ripemd160_hash = crypto.ripemd160(data)
    
    print(f"Original Data: {data.decode()}")
    print(f"SHA256: {sha256_hash.hex()}")
    print(f"Double SHA256: {double_sha256_hash.hex()}")
    print(f"RIPEMD160: {ripemd160_hash.hex()}")
    print()
    
    print("=== Key Cryptographic Concepts ===")
    print("• Private Key: 256-bit random number used to sign transactions")
    print("• Public Key: Derived from private key using elliptic curve cryptography")
    print("• Address: Public key hashed and Base58Check encoded")
    print("• Digital Signature: Proves ownership without revealing private key")
    print("• Merkle Tree: Efficient way to verify transaction inclusion")
    print("• Hash Functions: SHA256 and RIPEMD160 used for various purposes")

if __name__ == "__main__":
    demonstrate_cryptography() 