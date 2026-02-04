#2- lancer cette code pour detecter le paiement en litecoin
#
import requests
import time

# =========================
# CONFIGURATION
# =========================

LTC_ADDRESS = "LSYqEJAtrx4uXywaP1cmTuuPWiK8FGb2ix"

EXPECTED_AMOUNT_USD = 0.02
MIN_CONFIRMATIONS = 2
CHECK_INTERVAL = 30  # secondes

BLOCKCYPHER_API = "https://api.blockcypher.com/v1/ltc/main/addrs/"
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

# =========================
# UTILS
# =========================

def litoshi_to_ltc(value):
    return value / 100_000_000

def get_ltc_price_usd():
    params = {
        "ids": "litecoin",
        "vs_currencies": "usd"
    }
    r = requests.get(COINGECKO_API, params=params, timeout=10)
    r.raise_for_status()
    return r.json()["litecoin"]["usd"]

def get_address_info(address):
    r = requests.get(f"{BLOCKCYPHER_API}{address}", timeout=10)
    r.raise_for_status()
    return r.json()

# =========================
# CHECK PAYMENT
# =========================

def check_payment(address, min_ltc):
    data = get_address_info(address)
    txrefs = data.get("txrefs", [])

    for tx in txrefs:
        # Entrée vers l'adresse
        if tx["tx_input_n"] == -1:
            return {
                "tx_hash": tx["tx_hash"],
                "amount_ltc": litoshi_to_ltc(tx["value"]),
                "confirmations": tx.get("confirmations", 0)
            }

    return None

# =========================
# MAIN LOOP
# =========================

def main():
    print("Surveillance de l'adresse Litecoin")
    print("Adresse :", LTC_ADDRESS)

    ltc_price = get_ltc_price_usd()
    min_ltc = EXPECTED_AMOUNT_USD / ltc_price

    print(f"Prix LTC actuel : {ltc_price} USD")
    print(f"Montant attendu : {EXPECTED_AMOUNT_USD} USD")
    print(f"Minimum requis  : {min_ltc:.8f} LTC\n")

    while True:
        try:
            result = check_payment(LTC_ADDRESS, min_ltc)

            if result:
                print("Transaction détectée")
                print("TX Hash       :", result["tx_hash"])
                print("Montant reçu  :", result["amount_ltc"], "LTC")
                print("Confirmations :", result["confirmations"])

                if (
                    result["amount_ltc"] >= min_ltc
                    and result["confirmations"] >= MIN_CONFIRMATIONS
                ):
                    print("\nPAIEMENT CONFIRMÉ (USD OK)")
                    break
                else:
                    print("Montant ou confirmations insuffisants\n")
            else:
                print("Aucune transaction entrante détectée")

        except Exception as e:
            print("Erreur :", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
