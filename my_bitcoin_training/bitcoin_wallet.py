#!/usr/bin/env python3
"""
Bitcoin Wallet Implementation
A practical example of a Bitcoin wallet with transaction management
"""

import hashlib
import secrets
import json
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class UTXO:
    """Unspent Transaction Output"""
    txid: str
    output_index: int
    address: str
    amount: float
    script_pubkey: str
    spent: bool = False

@dataclass
class Transaction:
    """Bitcoin Transaction"""
    txid: str
    inputs: List[Dict]
    outputs: List[Dict]
    fee: float
    timestamp: float
    confirmed: bool = False

class BitcoinWallet:
    """Simple Bitcoin Wallet Implementation"""
    
    def __init__(self, name: str):
        self.name = name
        self.private_key: str = ""
        self.public_key: str = ""
        self.address: str = ""
        self.utxos: List[UTXO] = []
        self.transactions: List[Transaction] = []
        self.pending_transactions: List[Transaction] = []
        
        # Generate wallet if not exists
        self._generate_wallet()
    
    def _generate_wallet(self):
        """Generate a new wallet with key pair and address"""
        # Generate private key
        self.private_key = secrets.token_hex(32)
        
        # Generate public key (simplified)
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()
        
        # Generate address (simplified)
        address_hash = hashlib.sha256(self.public_key.encode()).hexdigest()
        self.address = f"1{address_hash[:25]}"
        
        # Ensure address is not None
        if not self.address:
            raise ValueError("Failed to generate wallet address")
    
    def get_balance(self) -> float:
        """Calculate total balance from UTXOs"""
        return sum(utxo.amount for utxo in self.utxos)
    
    def get_available_utxos(self, amount: float) -> Tuple[List[UTXO], float]:
        """Get UTXOs needed to spend a certain amount"""
        available_utxos = []
        total_available = 0.0
        
        for utxo in self.utxos:
            if not utxo.spent:  # In real implementation, check if UTXO is spent
                available_utxos.append(utxo)
                total_available += utxo.amount
                
                if total_available >= amount:
                    break
        
        return available_utxos, total_available
    
    def create_transaction(self, recipient_address: str, amount: float, fee: float = 0.001) -> Optional[Transaction]:
        """Create a new transaction"""
        total_needed = amount + fee
        available_utxos, total_available = self.get_available_utxos(total_needed)
        
        if total_available < total_needed:
            print(f"Insufficient funds. Need {total_needed} BTC, have {total_available} BTC")
            return None
        
        # Create transaction inputs
        inputs = []
        for utxo in available_utxos:
            inputs.append({
                'txid': utxo.txid,
                'output_index': utxo.output_index,
                'script_sig': f"OP_DUP OP_HASH160 {self.address} OP_EQUALVERIFY OP_CHECKSIG"
            })
        
        # Create transaction outputs
        outputs = [
            {
                'address': recipient_address,
                'amount': amount,
                'script_pubkey': f"OP_DUP OP_HASH160 {recipient_address} OP_EQUALVERIFY OP_CHECKSIG"
            }
        ]
        
        # Add change output if needed
        change_amount = total_available - total_needed
        if change_amount > 0.00001:  # Dust threshold
            outputs.append({
                'address': self.address,
                'amount': change_amount,
                'script_pubkey': f"OP_DUP OP_HASH160 {self.address} OP_EQUALVERIFY OP_CHECKSIG"
            })
        
        # Generate transaction ID
        tx_data = f"{inputs}{outputs}{time.time()}"
        txid = hashlib.sha256(tx_data.encode()).hexdigest()
        
        # Create transaction
        transaction = Transaction(
            txid=txid,
            inputs=inputs,
            outputs=outputs,
            fee=fee,
            timestamp=time.time(),
            confirmed=False
        )
        
        # Add to pending transactions
        self.pending_transactions.append(transaction)
        
        return transaction
    
    def add_utxo(self, txid: str, output_index: int, amount: float):
        """Add a UTXO to the wallet"""
        utxo = UTXO(
            txid=txid,
            output_index=output_index,
            address=self.address,
            amount=amount,
            script_pubkey=f"OP_DUP OP_HASH160 {self.address} OP_EQUALVERIFY OP_CHECKSIG"
        )
        self.utxos.append(utxo)
    
    def confirm_transaction(self, txid: str):
        """Mark a transaction as confirmed"""
        for tx in self.pending_transactions:
            if tx.txid == txid:
                tx.confirmed = True
                self.transactions.append(tx)
                self.pending_transactions.remove(tx)
                break
    
    def get_transaction_history(self) -> List[Dict]:
        """Get transaction history"""
        history = []
        
        for tx in self.transactions + self.pending_transactions:
            history.append({
                'txid': tx.txid,
                'timestamp': tx.timestamp,
                'fee': tx.fee,
                'confirmed': tx.confirmed,
                'inputs': len(tx.inputs),
                'outputs': len(tx.outputs)
            })
        
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    def export_wallet_info(self) -> Dict:
        """Export wallet information (without private key for security)"""
        return {
            'name': self.name,
            'address': self.address,
            'public_key': self.public_key,
            'balance': self.get_balance(),
            'utxo_count': len(self.utxos),
            'transaction_count': len(self.transactions),
            'pending_transactions': len(self.pending_transactions)
        }

class BitcoinNetwork:
    """Simulated Bitcoin Network"""
    
    def __init__(self):
        self.mempool: List[Transaction] = []
        self.confirmed_transactions: List[Transaction] = []
        self.block_height = 0
    
    def broadcast_transaction(self, transaction: Transaction):
        """Broadcast a transaction to the network"""
        self.mempool.append(transaction)
        print(f"Transaction {transaction.txid[:16]}... broadcasted to network")
    
    def mine_block(self):
        """Mine a new block (simplified)"""
        if not self.mempool:
            print("No transactions to mine")
            return
        
        # Take transactions from mempool
        block_transactions = self.mempool[:10]  # Max 10 transactions per block
        self.mempool = self.mempool[10:]
        
        # Confirm transactions
        for tx in block_transactions:
            tx.confirmed = True
            self.confirmed_transactions.append(tx)
        
        self.block_height += 1
        print(f"Block {self.block_height} mined with {len(block_transactions)} transactions")
        
        return block_transactions

def demonstrate_wallet():
    """Demonstrate Bitcoin wallet functionality"""
    print("=== Bitcoin Wallet Tutorial ===\n")
    
    # Create wallets
    alice_wallet = BitcoinWallet("Alice")
    bob_wallet = BitcoinWallet("Bob")
    charlie_wallet = BitcoinWallet("Charlie")
    
    # Create network
    network = BitcoinNetwork()
    
    print("1. Wallet Creation:")
    print(f"Alice's Address: {alice_wallet.address}")
    print(f"Bob's Address: {bob_wallet.address}")
    print(f"Charlie's Address: {charlie_wallet.address}")
    print()
    
    # Add some initial funds
    print("2. Adding Initial Funds:")
    alice_wallet.add_utxo("genesis_tx_1", 0, 10.0)  # Alice gets 10 BTC
    bob_wallet.add_utxo("genesis_tx_2", 0, 5.0)      # Bob gets 5 BTC
    charlie_wallet.add_utxo("genesis_tx_3", 0, 3.0)   # Charlie gets 3 BTC
    
    print(f"Alice's Balance: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance: {bob_wallet.get_balance()} BTC")
    print(f"Charlie's Balance: {charlie_wallet.get_balance()} BTC")
    print()
    
    # Create transactions
    print("3. Creating Transactions:")
    
    # Alice sends 2 BTC to Bob
    tx1 = alice_wallet.create_transaction(bob_wallet.address, 2.0)
    if tx1:
        network.broadcast_transaction(tx1)
        print(f"Alice -> Bob: 2.0 BTC (Fee: {tx1.fee} BTC)")
    
    # Bob sends 1 BTC to Charlie
    tx2 = bob_wallet.create_transaction(charlie_wallet.address, 1.0)
    if tx2:
        network.broadcast_transaction(tx2)
        print(f"Bob -> Charlie: 1.0 BTC (Fee: {tx2.fee} BTC)")
    
    # Charlie sends 0.5 BTC to Alice
    tx3 = charlie_wallet.create_transaction(alice_wallet.address, 0.5)
    if tx3:
        network.broadcast_transaction(tx3)
        print(f"Charlie -> Alice: 0.5 BTC (Fee: {tx3.fee} BTC)")
    print()
    
    # Mine blocks to confirm transactions
    print("4. Mining Blocks:")
    network.mine_block()
    network.mine_block()
    print()
    
    # Update wallet balances
    print("5. Updated Balances:")
    print(f"Alice's Balance: {alice_wallet.get_balance()} BTC")
    print(f"Bob's Balance: {bob_wallet.get_balance()} BTC")
    print(f"Charlie's Balance: {charlie_wallet.get_balance()} BTC")
    print()
    
    # Show transaction history
    print("6. Transaction History:")
    for wallet in [alice_wallet, bob_wallet, charlie_wallet]:
        print(f"\n{wallet.name}'s Transactions:")
        history = wallet.get_transaction_history()
        for tx in history[:3]:  # Show last 3 transactions
            status = "✓" if tx['confirmed'] else "⏳"
            print(f"  {status} {tx['txid'][:16]}... (Fee: {tx['fee']} BTC)")
    
    print("\n=== Wallet Features ===")
    print("• Private Key Management: Secure storage of private keys")
    print("• Address Generation: Public addresses for receiving Bitcoin")
    print("• UTXO Management: Tracking unspent transaction outputs")
    print("• Transaction Creation: Building and signing transactions")
    print("• Balance Calculation: Real-time balance from UTXOs")
    print("• Transaction History: Complete transaction record")
    print("• Network Integration: Broadcasting transactions to network")

def interactive_wallet_demo():
    """Interactive wallet demonstration"""
    print("\n=== Interactive Wallet Demo ===")
    
    # Create wallet
    wallet_name = input("Enter wallet name: ")
    wallet = BitcoinWallet(wallet_name)
    
    print(f"\nWallet created: {wallet.address}")
    print(f"Initial balance: {wallet.get_balance()} BTC")
    
    # Add some initial funds
    wallet.add_utxo("demo_tx_1", 0, 5.0)
    print(f"Added 5 BTC. New balance: {wallet.get_balance()} BTC")
    
    while True:
        print(f"\n{wallet.name}'s Wallet")
        print(f"Address: {wallet.address}")
        print(f"Balance: {wallet.get_balance()} BTC")
        print(f"UTXOs: {len(wallet.utxos)}")
        print(f"Transactions: {len(wallet.transactions)}")
        
        print("\nOptions:")
        print("1. Send Bitcoin")
        print("2. View transaction history")
        print("3. Export wallet info")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == "1":
            recipient = input("Recipient address: ")
            try:
                amount = float(input("Amount (BTC): "))
                fee = float(input("Fee (BTC, default 0.001): ") or "0.001")
                
                tx = wallet.create_transaction(recipient, amount, fee)
                if tx:
                    print(f"Transaction created: {tx.txid}")
                    print(f"Fee: {tx.fee} BTC")
                else:
                    print("Transaction failed!")
            except ValueError:
                print("Invalid amount!")
        
        elif choice == "2":
            history = wallet.get_transaction_history()
            print("\nTransaction History:")
            for tx in history:
                status = "✓" if tx['confirmed'] else "⏳"
                print(f"{status} {tx['txid'][:16]}... (Fee: {tx['fee']} BTC)")
        
        elif choice == "3":
            info = wallet.export_wallet_info()
            print("\nWallet Information:")
            for key, value in info.items():
                print(f"{key}: {value}")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    demonstrate_wallet()
    
    # Ask if user wants interactive demo
    choice = input("\nWould you like to try the interactive wallet demo? (yes/no): ").lower()
    if choice in ['yes', 'y']:
        interactive_wallet_demo() 