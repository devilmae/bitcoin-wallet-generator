import unittest
from src.wallet_generator import generate_mnemonic, generate_wallet

class TestWalletGenerator(unittest.TestCase):

    def test_generate_mnemonic(self):
        mnemonic = generate_mnemonic()
        self.assertIsInstance(mnemonic, str)
        self.assertGreaterEqual(len(mnemonic.split()), 12)

    def test_generate_wallet(self):
        mnemonic = generate_mnemonic()
        wallet = generate_wallet(mnemonic)
        self.assertIsNotNone(wallet)
        self.assertIn("private_key", wallet)
        self.assertIn("addresses", wallet)

if __name__ == "__main__":
    unittest.main()
