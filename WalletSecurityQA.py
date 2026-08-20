# WalletSecurityQA.py
import unittest
import threading
import time
from DigitalWallet import DigitalWalletSystem

class TestWalletSecurity(unittest.TestCase):

    def setUp(self):
        self.wallet = DigitalWalletSystem()
        # user1 created with a 1000.0 daily limit
        self.wallet.create_account("user1", "1234", daily_limit=1000.0)
        self.wallet.create_account("user2", "5678")
        
        # Pre-seed 2000.0 balance so balance checks pass, allowing limit/fraud checks to trigger
        self.wallet.deposit("user1", 2000.0)

    def test_normal_transaction(self):
        """Test standard valid withdrawal."""
        success, msg = self.wallet.withdraw("user1", 100.0, "1234")
        self.assertTrue(success)
        balance, _ = self.wallet.verify_balance("user1")
        self.assertEqual(balance, 1900.0)

    def test_insufficient_balance(self):
        """Test transaction failing due to low funds."""
        # Attempting to pull more than the 2000.0 seeded balance
        success, msg = self.wallet.withdraw("user1", 2500.0, "1234")
        self.assertFalse(success)
        self.assertEqual(msg, "Insufficient balance")

    def test_daily_limit(self):
        """Test transaction failing because it exceeds daily limits."""
        # user1 has 2000.0 balance but a 1000.0 daily limit. 
        # Withdrawing 1100.0 will now correctly hit the daily limit check first.
        success, msg = self.wallet.withdraw("user1", 1100.0, "1234")
        self.assertFalse(success)
        self.assertEqual(msg, "Daily transaction limit exceeded")

    def test_multiple_failed_pins(self):
        """Test block triggering after multiple wrong PIN entries."""
        self.wallet.withdraw("user1", 10.0, "9999")
        self.wallet.withdraw("user1", 10.0, "9999")
        success, msg = self.wallet.withdraw("user1", 10.0, "9999")

        # The 3rd failed attempt logs fraud
        self.assertFalse(success)

        # Attempting with correct PIN now should trigger fraud detection block
        success, msg = self.wallet.withdraw("user1", 10.0, "1234")
        self.assertFalse(success)
        self.assertEqual(msg, "Transaction flagged as suspicious: Multiple failed PIN attempts")

    def test_suspicious_transaction_frequency(self):
        """Test fraud flag when more than 5 transactions happen in rapid succession."""
        # Execute 5 fast valid deposits
        for _ in range(5):
            self.wallet.deposit("user1", 10.0)

        # 6th deposit should trigger high frequency fraud rule
        success, msg = self.wallet.deposit("user1", 10.0)
        self.assertFalse(success)
        self.assertIn("High transaction frequency", msg)

    def test_duplicate_transaction(self):
        """Test rapid identical transactions are blocked as duplicates."""
        success1, msg1 = self.wallet.withdraw("user1", 20.0, "1234")
        success2, msg2 = self.wallet.withdraw("user1", 20.0, "1234")

        self.assertTrue(success1)
        self.assertFalse(success2)
        self.assertEqual(msg2, "Duplicate transaction detected")

    def test_negative_amount(self):
        """Test that negative values are rejected."""
        success, msg = self.wallet.deposit("user1", -50.0)
        self.assertFalse(success)
        self.assertEqual(msg, "Amount must be positive")

    def test_concurrent_transactions(self):
        """Test concurrent transaction isolation handling."""
        def worker():
            self.wallet.withdraw("user1", 10.0, "1234")

        threads = []
        for _ in range(3):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        balance, _ = self.wallet.verify_balance("user1")
        self.assertLessEqual(balance, 2000.0)

if __name__ == "__main__":
    unittest.main()
