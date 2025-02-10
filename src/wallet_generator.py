import logging
import concurrent.futures
import base58
from hdwallet import HDWallet
from hdwallet.cryptocurrencies import Bitcoin as BTC
from hdwallet.derivations import IDerivation
from hdwallet.hds import BIP32HD
from hdwallet.mnemonics import BIP39Mnemonic
from mnemonic import Mnemonic
from src.utils import save_wallet_to_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Mnemonic Generator
mnemo = Mnemonic("english")

def pvk_to_wif(key_hex: str) -> str:
    """Convert private key in hex format to Wallet Import Format (WIF)."""
    return base58.b58encode_check(b'\x80' + bytes.fromhex(key_hex)).decode()

def generate_mnemonic(strength=128) -> str:
    """Generate a new mnemonic phrase."""
    return mnemo.generate(strength=strength)

def generate_wallet(mnemonic: str):
    """Generate Bitcoin wallet address and private key from a mnemonic phrase."""
    try:
        # Create HD Wallet instance
        hdwallet = HDWallet(cryptocurrency=BTC, hd=BIP32HD)
        hdwallet.from_mnemonic(mnemonic=BIP39Mnemonic(mnemonic=mnemonic))

        # Use SegWit (P2SH) derivation path
        derivation_path = "m/49'/0'/0'/0/0"
        hdwallet.from_derivation(IDerivation(derivation_path))

        # Extract private key and addresses
        private_key = hdwallet.private_key()
        address_types = ["P2PKH", "P2SH", "P2TR", "P2WPKH"]
        addresses = {atype: hdwallet.address(atype) for atype in address_types}

        # Convert private key to WIF format
        wif_key = pvk_to_wif(private_key)

        # Save wallet information
        wallet_info = {
            "mnemonic": mnemonic,
            "private_key": private_key,
            "wif_key": wif_key,
            "addresses": addresses
        }
        save_wallet_to_file(wallet_info)
        
        logger.info(f"Wallet generated: {wallet_info}")
        return wallet_info

    except Exception as e:
        logger.error(f"Error generating wallet: {e}")
        return None

def generate_wallets_parallel(num_wallets=10):
    """Generate multiple wallets in parallel."""
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        mnemonics = [generate_mnemonic() for _ in range(num_wallets)]
        executor.map(generate_wallet, mnemonics)

if __name__ == "__main__":
    generate_wallets_parallel(5)
