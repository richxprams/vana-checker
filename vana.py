from web3 import Web3
from colorama import Fore, Style

# Masukin RPC URL jaringan Vana
VANA_RPC_URL = "https://rpc.vana.org"  # RPC URL jaringan Vana
web3 = Web3(Web3.HTTPProvider(VANA_RPC_URL))

# Cek koneksi
if not web3.is_connected():
    print("Gagal konek ke jaringan Vana!")
    exit()

# Baca file wallets.txt
def load_wallets(file_path):
    try:
        with open(file_path, "r") as file:
            # Strip enter, spasi, dan filter wallet kosong
            wallets = [line.strip() for line in file.readlines() if line.strip()]
        return wallets
    except FileNotFoundError:
        print(f"File {file_path} nggak ketemu!")
        return []

# Fungsi cek balance native token VANA
def check_balance(wallet_address):
    try:
        balance_wei = web3.eth.get_balance(wallet_address)
        balance_vana = web3.from_wei(balance_wei, 'ether')  # Convert ke VANA
        return float(balance_vana)
    except Exception as e:
        print(f"Error cek balance wallet {wallet_address}: {e}")
        return None

# Main program
if __name__ == "__main__":
    file_path = "wallets.txt"
    wallets = load_wallets(file_path)

    if not wallets:
        print("Daftar wallet kosong atau file nggak ada.")
        exit()

    print(f"Cek balance {len(wallets)} wallet di jaringan Vana...\n")

    for wallet in wallets:
        balance = check_balance(wallet)
        if balance is not None:
            # Warna hijau untuk balance > 0, merah untuk balance == 0
            if balance > 0:
                color = Fore.GREEN
            else:
                color = Fore.RED
            
            # Format balance supaya selalu tampil dalam desimal penuh
            balance_formatted = f"{balance:.18f}".rstrip('0').rstrip('.')  # Max 18 digit desimal
            
            print(f"{color}Wallet {wallet}: {balance_formatted} VANA{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Wallet {wallet}: Error saat cek balance{Style.RESET_ALL}")
