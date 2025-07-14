#!/usr/bin/env python3
"""
Bitcoin Programming Basics
Learn the fundamental concepts of Bitcoin programming
"""

import hashlib
import hmac
import secrets
from typing import List, Dict, Tuple
import json

class BitcoinAddress:
    """Simple Bitcoin address generation and validation"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.address = None
    
    def generate_private_key(self) -> str:
        """Generate a random private key (simplified)"""
        # In real Bitcoin, this would be a 256-bit random number
        self.private_key = secrets.token_hex(32)
        return self.private_key
    
    def derive_public_key(self) -> str:
        """Derive public key from private key (simplified)"""
        if not self.private_key:
            raise ValueError("Private key must be generated first")
        
        # In real Bitcoin, this uses elliptic curve cryptography (secp256k1)
        # This is a simplified version for educational purposes
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
        return self.public_key
    
    def generate_address(self) -> str:
        """Generate Bitcoin address from public key (simplified)"""
        if not self.public_key:
            self.derive_public_key()
        
        # Simplified address generation
        # Real Bitcoin addresses use Base58Check encoding
        address_hash = hashlib.sha256(self.public_key.encode()).hexdigest()
        self.address = f"1{address_hash[:25]}"  # Simplified format
        return self.address

class BitcoinTransaction:
    """Represents a Bitcoin transaction"""
    
    def __init__(self, txid: str = None):
        self.txid = txid or self._generate_txid()
        self.inputs: List[Dict] = []
        self.outputs: List[Dict] = []
        self.fee = 0
        self.timestamp = None
    
    def _generate_txid(self) -> str:
        """Generate a transaction ID (simplified)"""
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()
    
    def add_input(self, prev_txid: str, output_index: int, amount: float):
        """Add an input to the transaction"""
        self.inputs.append({
            'prev_txid': prev_txid,
            'output_index': output_index,
            'amount': amount
        })
    
    def add_output(self, address: str, amount: float):
        """Add an output to the transaction"""
        self.outputs.append({
            'address': address,
            'amount': amount
        })
    
    def calculate_fee(self) -> float:
        """Calculate transaction fee (simplified)"""
        input_total = sum(input['amount'] for input in self.inputs)
        output_total = sum(output['amount'] for output in self.outputs)
        self.fee = input_total - output_total
        return self.fee
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            'txid': self.txid,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'fee': self.fee
        }

class BitcoinBlock:
    """Represents a Bitcoin block"""
    
    def __init__(self, index: int, previous_hash: str = None):
        self.index = index
        self.timestamp = None
        self.transactions: List[BitcoinTransaction] = []
        self.previous_hash = previous_hash or "0" * 64
        self.nonce = 0
        self.hash = None
    
    def add_transaction(self, transaction: BitcoinTransaction):
        """Add a transaction to the block"""
        self.transactions.append(transaction)
    
    def calculate_merkle_root(self) -> str:
        """Calculate Merkle root of transactions (simplified)"""
        if not self.transactions:
            return hashlib.sha256("empty".encode()).hexdigest()
        
        # Simplified Merkle tree calculation
        tx_hashes = [tx.txid for tx in self.transactions]
        while len(tx_hashes) > 1:
            new_hashes = []
            for i in range(0, len(tx_hashes), 2):
                if i + 1 < len(tx_hashes):
                    combined = tx_hashes[i] + tx_hashes[i + 1]
                else:
                    combined = tx_hashes[i] + tx_hashes[i]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            tx_hashes = new_hashes
        
        return tx_hashes[0]
    
    def mine_block(self, difficulty: int = 4):
        """Mine the block (simplified proof of work)"""
        target = "0" * difficulty
        
        while True:
            block_data = f"{self.index}{self.previous_hash}{self.calculate_merkle_root()}{self.nonce}"
            self.hash = hashlib.sha256(block_data.encode()).hexdigest()
            
            if self.hash[:difficulty] == target:
                break
            
            self.nonce += 1
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'nonce': self.nonce
        }

def demonstrate_bitcoin_concepts():
    """Demonstrate basic Bitcoin concepts"""
    print("=== Bitcoin Programming Basics ===\n")
    
    # 1. Address Generation
    print("1. Bitcoin Address Generation:")
    address_gen = BitcoinAddress()
    private_key = address_gen.generate_private_key()
    public_key = address_gen.derive_public_key()
    address = address_gen.generate_address()
    
    print(f"Private Key: {private_key[:16]}...")
    print(f"Public Key: {public_key[:16]}...")
    print(f"Bitcoin Address: {address}")
    print()
    
    # 2. Transaction Creation
    print("2. Bitcoin Transaction:")
    tx = BitcoinTransaction()
    tx.add_input("abc123...", 0, 1.0)  # Previous transaction
    tx.add_output("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", 0.8)  # Recipient
    tx.add_output("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", 0.19)  # Change
    fee = tx.calculate_fee()
    
    print(f"Transaction ID: {tx.txid}")
    print(f"Inputs: {len(tx.inputs)}")
    print(f"Outputs: {len(tx.outputs)}")
    print(f"Fee: {fee} BTC")
    print()
    
    # 3. Block Mining
    print("3. Bitcoin Block Mining:")
    block = BitcoinBlock(1, "0000000000000000000000000000000000000000000000000000000000000000")
    block.add_transaction(tx)
    
    print("Mining block...")
    block.mine_block(difficulty=2)  # Lower difficulty for demo
    
    print(f"Block Hash: {block.hash}")
    print(f"Nonce: {block.nonce}")
    print(f"Transactions: {len(block.transactions)}")
    print()
    
    # 4. Blockchain Structure
    print("4. Blockchain Structure:")
    blockchain = [block]
    
    # Add another block
    block2 = BitcoinBlock(2, block.hash)
    block2.add_transaction(BitcoinTransaction())
    block2.mine_block(difficulty=2)
    blockchain.append(block2)
    
    print(f"Blockchain length: {len(blockchain)}")
    for i, b in enumerate(blockchain):
        print(f"Block {i+1}: {b.hash[:16]}...")
    
    print("\n=== Key Bitcoin Concepts ===")
    print("• Private Key: Secret key used to sign transactions")
    print("• Public Key: Derived from private key, used to generate addresses")
    print("• Address: Public identifier for receiving Bitcoin")
    print("• Transaction: Transfer of Bitcoin between addresses")
    print("• Block: Container for multiple transactions")
    print("• Mining: Process of creating new blocks through proof of work")
    print("• Blockchain: Chain of blocks containing all transaction history")

if __name__ == "__main__":
    demonstrate_bitcoin_concepts() 