# SuperESP

ESPHome konfigurace pro ESP32 moduly s optimalizovaným Wi-Fi připojením.

## 📋 Popis projektu

Tento projekt obsahuje kompletní ESPHome konfigurace pro dva ESP32 moduly:
- **ESP32-C3 Super Mini** - kompaktní modul s ESP32-C3 čipem
- **ESP32D** - standardní ESP32 vývojová deska

Konfigurace řeší běžné problémy s Wi-Fi připojením (např. "Auth Expired" chyby) pomocí optimalizovaných nastavení a zahrnují fallback AP hotspot pro snadnou diagnostiku.

## 🔧 Požadavky

### Software
- **ESPHome** (verze 2023.12.0 nebo novější)
  ```bash
  pip install esphome
  ```
- **Python** (verze 3.8 nebo novější)
- **esptool** (pro vymazání flash paměti)
  ```bash
  pip install esptool
  ```

### Hardware
- ESP32-C3 Super Mini nebo ESP32D modul
- USB kabel pro připojení k počítači
- Wi-Fi router s podporou WPA2-PSK (ne WPA3!)

## 🚀 Instalace a použití

### 1. Vytvoření secrets.yaml

Zkopírujte vzorový soubor a vyplňte své údaje:

```bash
cp secrets.yaml.example secrets.yaml
```

Upravte `secrets.yaml` a vyplňte:
- `wifi_ssid` - název vaší Wi-Fi sítě
- `wifi_password` - heslo k Wi-Fi (bez speciálních znaků!)
- `api_encryption_key` - vygenerujte pomocí: `esphome config esp32c3_supermini.yaml` (klíč se automaticky vytvoří)
- `ota_password` - vaše heslo pro OTA aktualizace
- `ap_password` - heslo pro fallback AP (výchozí: "fallback123")

**Poznámka:** Soubor `secrets.yaml` obsahuje citlivé údaje a neměl by být sdílen nebo commitován do gitu!

### 2. Kompilace firmware

Pro ESP32-C3 Super Mini:
```bash
esphome compile esp32c3_supermini.yaml
```

Pro ESP32D:
```bash
esphome compile esp32d.yaml
```

### 3. První nahrání firmware (přes USB)

#### Krok 1: Vymazání flash paměti (doporučeno při problémech)
```bash
# Pro ESP32-C3
esptool.py --chip esp32c3 --port /dev/ttyUSB0 erase_flash

# Pro ESP32D
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```

**Windows:** Použijte `COM3`, `COM4` atd. místo `/dev/ttyUSB0`  
**macOS:** Použijte `/dev/cu.usbserial-*` nebo `/dev/tty.usbserial-*`

#### Krok 2: Nahrání firmware
```bash
# Pro ESP32-C3 Super Mini
esphome run esp32c3_supermini.yaml

# Pro ESP32D
esphome run esp32d.yaml
```

Vyberte správný USB port, když se zobrazí výzva.

### 4. Další aktualizace (přes Wi-Fi/OTA)

Po úspěšném prvním nahrání můžete firmware aktualizovat bezdrátově:

```bash
esphome run esp32c3_supermini.yaml
# nebo
esphome run esp32d.yaml
```

ESPHome automaticky detekuje zařízení v síti a nabídne OTA aktualizaci.

## 🔍 Troubleshooting - Řešení problémů s Wi-Fi

### Problém: ESP se nemůže připojit k Wi-Fi ("Auth Expired")

#### 1. Zkontrolujte šifrování routeru
- **Použijte WPA2-PSK (AES)** - ESP32 má problémy s WPA3!
- Vypněte WPA3 a 802.11w (PMF - Protected Management Frames)
- V nastavení routeru vyberte: "WPA2-Personal" nebo "WPA2-PSK"

#### 2. Zkontrolujte Wi-Fi heslo
- Nepoužívejte speciální znaky (!, @, #, $, %, atd.)
- Zkuste jednoduché heslo jen s písmeny a čísly
- Zkontrolujte, že v `secrets.yaml` není překlep

#### 3. Zkontrolujte název Wi-Fi sítě (SSID)
- SSID nesmí obsahovat speciální znaky
- SSID je case-sensitive (rozlišuje velká/malá písmena)
- Zkuste jednoduchý SSID bez mezer

#### 4. Zkontrolujte Wi-Fi kanál
- ESP32 podporuje pouze **2.4 GHz** (ne 5 GHz!)
- Používejte kanály 1-11 (ne 12-14)
- Zkuste nastavit fixní kanál místo "Auto"

#### 5. Zkontrolujte sílu signálu
- ESP by měl být blízko routeru (alespoň při testování)
- Pro ESP32-C3 je výkon snížen na 8.5dB pro stabilitu

### Problém: Nespouští se fallback AP hotspot

Fallback AP se aktivuje automaticky po 60 sekundách, pokud se ESP nemůže připojit k Wi-Fi.

**Jak se připojit k fallback AP:**

1. Počkejte 60 sekund po startu ESP
2. Na telefonu/počítači vyhledejte Wi-Fi síť:
   - `ESP32-C3-Fallback` (pro C3 modul)
   - `ESP32D-Fallback` (pro D modul)
3. Připojte se pomocí hesla z `secrets.yaml` (výchozí: `fallback123`)
4. Měl by se otevřít captive portal pro konfiguraci
5. Zkontrolujte logy přes sériový port:
   ```bash
   esphome logs esp32c3_supermini.yaml
   # nebo
   esphome logs esp32d.yaml
   ```

### Problém: ESP se stále restartuje

- Zkontrolujte napájení - použijte kvalitní USB kabel a zdroj
- ESP32-C3 může mít problémy s nekvalitními USB kabely
- Zkuste jiný USB port nebo napájecí adaptér (minimálně 500mA)

## 📝 Poznámky k ESP32-C3

ESP32-C3 je RISC-V čip s některými specifiky:

1. **Nižší Wi-Fi výkon**: Výkon je snížen na 8.5dB (`output_power: 8.5dB`) pro lepší stabilitu
2. **USB Serial/JTAG**: C3 má vestavěný USB, není potřeba externí převodník
3. **Citlivější na napájení**: Vyžaduje stabilní napájení, použijte kvalitní USB kabel
4. **Boot režim**: Při nahrávání držte tlačítko BOOT, pokud se automatické nahrání nezdaří

## 📁 Struktura projektu

```
SuperESP/
├── README.md                    # Tento soubor
├── secrets.yaml.example         # Vzorový soubor s hesly (kopírovat na secrets.yaml)
├── secrets.yaml                 # Vaše skutečná hesla (NEGITOVAT!)
├── esp32c3_supermini.yaml       # Konfigurace pro ESP32-C3 Super Mini
└── esp32d.yaml                  # Konfigurace pro ESP32D
```

## 🔐 Bezpečnost

- Soubor `secrets.yaml` obsahuje citlivá data a je v `.gitignore`
- Nikdy nesdílejte `secrets.yaml` veřejně
- Pro produkční použití změňte všechna výchozí hesla
- Použijte silná hesla pro OTA a API

## 📚 Další informace

- [ESPHome dokumentace](https://esphome.io/)
- [ESP32 dokumentace](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- [ESP32-C3 dokumentace](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/)

## 🐛 Hlášení problémů

Pokud narazíte na problémy, vytvořte issue a přiložte:
- Logy ze sériového portu (`esphome logs ...`)
- Použitý modul (C3 nebo D)
- Typ routeru a použité šifrování
- Verzi ESPHome (`esphome version`)

## 📄 Licence

Tento projekt je open-source a volně k použití.