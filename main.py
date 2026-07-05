print("Merhaba Nous, ben geldim!")
import requests

def check_contract(contract_address):
    # GoPlus Security API'sine bağlanıyoruz
    url = f"https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses={contract_address}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Basit bir güvenlik kontrolü yapalım
        result = data.get("result", {})
        is_honeypot = result.get(contract_address.lower(), {}).get("is_honeypot", "0")
        
        if is_honeypot == "1":
            print(f"UYARI: {contract_address} adresi bir HONEYPOT (tuzak) olabilir!")
        else:
            print(f"Güvenlik Analizi: {contract_address} adresi temiz görünüyor.")
            
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

# Test için örnek bir kontrat adresi (PEPE token adresi)
test_address = "0x6982508145454Ce325dDbE47a25d4ec3d2311933"
check_contract(test_address)
