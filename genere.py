import os
from bip_utils import (
    Bip39SeedGenerator,
    Bip39MnemonicValidator,
    Bip44,
    Bip44Coins,
    Bip44Changes
)

# ===== CONFIG =====
ENV_VAR = "TRON_MNEMONIC"
START_INDEX = 0
COUNT = 5  # nombre d'adresses à générer
# ==================

def load_seed():
    mnemonic = os.getenv(ENV_VAR)

    if not mnemonic:
        raise Exception(f"{ENV_VAR} non définie")

    # Validation stricte BIP39
    Bip39MnemonicValidator().Validate(mnemonic)

    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    return seed_bytes


def generate_addresses(seed_bytes, start_index, count):
    bip44 = Bip44.FromSeed(seed_bytes, Bip44Coins.TRON)
    addresses = []

    for i in range(start_index, start_index + count):
        acct = (
            bip44
            .Purpose()
            .Coin()
            .Account(0)
            .Change(Bip44Changes.CHAIN_EXT)  # ✅ CORRECTION ICI
            .AddressIndex(i)
        )

        addresses.append({
            "index": i,
            "address": acct.PublicKey().ToAddress(),
            "private_key_hex": acct.PrivateKey().Raw().ToHex()
        })

    return addresses


def main():
    print("Chargement de la seed...")
    seed = load_seed()
    print("Seed OK\n")

    print("Génération des adresses TRON :\n")
    wallets = generate_addresses(seed, START_INDEX, COUNT)

    for w in wallets:
        print(f"Index {w['index']}")
        print(f"Adresse : {w['address']}")
        print(f"Clé privée (HEX) : {w['private_key_hex']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
