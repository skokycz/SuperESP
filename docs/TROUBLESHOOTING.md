# SuperESP Troubleshooting Guide

Řešení nejčastějších problémů při práci s SuperESP.

---

## 🔍 Obsah

1. [Flash Recovery problémy](#-flash-recovery-problémy)
2. [ESPHome problémy](#-esphome-problémy)
3. [WiFi problémy](#-wifi-problémy)
4. [Hardware problémy](#-hardware-problémy)
5. [Home Assistant problémy](#-home-assistant-problémy)
6. [Obecné problémy](#-obecné-problémy)

---

## 🔥 Flash Recovery problémy

### ESP32 není detekován

**Příznaky:**
```
✗ Žádné COM porty nebyly nalezeny
✗ Nelze se připojit k chipu
```

**Řešení:**

1. **Zkontrolujte USB kabel**
   - Použijte **DATA kabel** (ne jen nabíjecí!)
   - Zkuste jiný kabel
   - Test: Připojte telefon - funguje přenos dat?

2. **Instalujte ovladače**
   
   **Windows:**
   - **CH340:** https://github.com/nodemcu/nodemcu-devkit/tree/master/Drivers
   - **CP210x:** https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
   
   Po instalaci:
   - Odpojte a znovu připojte ESP32
   - Zkontrolujte Device Manager → Porty (COM & LPT)
   
   **Linux:**
   ```bash
   # Většina distribucí má driver vestavěný
   # Zkontrolujte dmesg:
   dmesg | grep ttyUSB
   
   # Mělo by zobrazit:
   # usb 1-1: ch341-uart converter now attached to ttyUSB0
   ```
   
   **macOS:**
   ```bash
   # CH340 driver:
   # https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver
   
   # Po instalaci:
   ls /dev/cu.*
   # Mělo by zobrazit: /dev/cu.usbserial-XXXX
   ```

3. **BOOT mode**
   - **Stiskněte a podržte BOOT** tlačítko
   - **Připojte USB** (stále držte BOOT)
   - **Pusťte BOOT** po 2 sekundách
   - Zkuste znovu flash

4. **Zkuste jiný USB port**
   - USB 2.0 porty někdy fungují lépe než 3.0
   - Zkuste port přímo na PC (ne přes hub)

5. **Nižší baud rate**
   ```bash
   python recover.py --baud 115200
   ```

### Flash selhává v průběhu

**Příznaky:**
```
Erasing flash (this may take a while)...
Traceback (most recent call last):
  File "esptool.py", line XXX
serial.serialutil.SerialException: device disconnected
```

**Řešení:**

1. **Špatný USB kabel nebo port**
   - Použijte kvalitní, krátký (<1m) kabel
   - Zkuste jiný port

2. **Nedostatečné napájení**
   - Použijte USB port přímo na PC
   - Ne USB hub bez napájení
   - Odpojte ostatní USB zařízení

3. **Interference**
   - Odpojte jiné ESP32 z USB
   - Zkuste bez WiFi adaptérů v blízkosti

### Permission denied (Linux)

**Příznaky:**
```
serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyUSB0: [Errno 13] Permission denied
```

**Řešení:**

**Dočasné:**
```bash
sudo chmod 666 /dev/ttyUSB0
```

**Trvalé:**
```bash
# Přidat uživatele do skupiny dialout
sudo usermod -a -G dialout $USER

# Odhlaste se a znovu přihlaste (nebo restart)
# Ověřte:
groups
# Mělo by obsahovat: dialout
```

---

## 🔌 ESPHome problémy

### ESPHome není nainstalován

**Příznaky:**
```
bash: esphome: command not found
```

**Řešení:**
```bash
pip install esphome

# Pokud pip není v PATH:
python -m pip install esphome

# Ověření:
esphome version
```

### Kompilace selhává

**Příznaky:**
```
ERROR Error compiling project
```

**Řešení:**

1. **secrets.yaml chybí**
   ```bash
   cd firmware/test-blink
   cp secrets.yaml.example secrets.yaml
   nano secrets.yaml  # upravte WiFi údaje
   ```

2. **Špatný formát YAML**
   - Zkontrolujte odsazení (2 mezery, NE taby!)
   - Použijte YAML validator: https://www.yamllint.com/
   
3. **Smazat cache**
   ```bash
   rm -rf .esphome
   esphome run main.yaml
   ```

4. **Chybějící dependencies**
   ```bash
   pip install --upgrade esphome
   ```

### OTA selhává

**Příznaky:**
```
ERROR Error uploading via OTA
```

**Řešení:**

1. **Špatné OTA heslo**
   - Zkontrolujte `secrets.yaml`
   - Heslo musí být stejné jako při prvním flash

2. **ESP32 offline**
   ```bash
   # Ping test:
   ping <IP_ESP32>
   
   # Pokud nereaguje:
   # - Zkontrolujte WiFi připojení
   # - Restartujte ESP32
   ```

3. **Firewall blokuje**
   - Windows: Povolte port 3232 (OTA)
   - Linux: 
     ```bash
     sudo ufw allow 3232
     ```

4. **Použijte USB fallback**
   ```bash
   esphome run main.yaml
   # Vyberte [2] Using USB cable
   ```

---

## 📡 WiFi problémy

### ESP32 se nepřipojí k WiFi

**Příznaky:**
- LED bliká, ale v logs žádná IP adresa
- Objeví se fallback AP: "SuperESP Test Fallback"

**Řešení:**

1. **Zkontrolujte SSID a heslo**
   ```yaml
   # secrets.yaml
   wifi_ssid: "PresneNazevSite"  # case-sensitive!
   wifi_password: "SpravneHeslo"
   ```

2. **2.4GHz pouze!**
   - ESP32-C3 **nepodporuje 5GHz**
   - Zkontrolujte, že router vysílá 2.4GHz
   - Rozdělte 2.4/5GHz do samostatných SSID (doporučeno)

3. **Vzdálenost a signál**
   - Přesuňte ESP32 blíž k routeru
   - Zkontrolujte sílu signálu:
     ```
     # V ESPHome logs:
     [wifi:xxx]: WiFi signal: -XX dB
     ```
   - **Dobrý signál:** -50 až -70 dBm
   - **Slabý signál:** -70 až -90 dBm

4. **MAC filter / security**
   - Zkontrolujte MAC filter na routeru
   - Dočasně vypněte firewall/security na routeru

5. **Připojte se k fallback AP**
   ```
   SSID: SuperESP Test Fallback
   Password: superesp123
   URL: http://192.168.4.1
   ```
   - Zkontrolujte logy
   - Upravte WiFi konfiguraci

### WiFi připojí, ale žádný internet

**Není problém!** ESP32 nepotřebuje internet, jen lokální síť.

Pokud ale internet chcete:
1. Zkontrolujte DHCP na routeru
2. Statická IP? Nastavte gateway a DNS v ESPHome:
   ```yaml
   wifi:
     manual_ip:
       static_ip: 192.168.1.100
       gateway: 192.168.1.1
       subnet: 255.255.255.0
   ```

---

## 🔧 Hardware problémy

### LED nebliká

**Příznaky:**
- ESP32 připojeno, WiFi OK, ale LED nesvítí/nebliká

**Řešení:**

1. **Zkontrolujte GPIO8**
   - LED je na GPIO8 (inverted)
   - Zkontrolujte config:
     ```yaml
     light:
       - platform: binary
         pin:
           number: GPIO8
           inverted: true  # DŮLEŽITÉ!
     ```

2. **LED poškozená?**
   - Test pomocí web UI: zapnout/vypnout LED
   - Pokud nereaguje → možná vadná LED na boardu

3. **Test jiného GPIO**
   ```yaml
   # Zkuste externí LED:
   light:
     - platform: binary
       pin: GPIO2  # bez inverted
   ```

### DHT22 nečte data (BLOK 2)

**Příznaky:**
```
[dht:xxx]: Error reading temperature/humidity
```

**Řešení:**

1. **Zapojení**
   ```
   DHT22      ESP32-C3
   VCC    →   3V3
   GND    →   GND
   DATA   →   GPIO2
   
   + 10kΩ pull-up mezi VCC a DATA
   ```

2. **Pull-up resistor chybí**
   - Některé DHT22 moduly mají vestavěný
   - Pokud ne, přidejte 10kΩ mezi VCC a DATA

3. **Špatný DHT22?**
   - Zkuste jiný sensor
   - Test na Arduinu/jiném zařízení

### SD karta nefunguje (BLOK 2)

**Příznaky:**
```
[spi:xxx]: SPI initialization failed
```

**Řešení:**

1. **Zapojení SPI**
   ```
   SD Module    ESP32-C3
   VCC      →   3V3 (nebo 5V pokud modul podporuje)
   GND      →   GND
   CS       →   GPIO4
   MOSI     →   GPIO5
   CLK      →   GPIO6
   MISO     →   GPIO7
   ```

2. **GPIO 6,7 vytržené?**
   - Použijte software SPI (viz [HARDWARE.md](HARDWARE.md))

3. **SD karta formát**
   - Použijte **FAT32** (ne exFAT/NTFS)
   - Max 32GB (doporučeno 1-16GB)
   - Naformátujte:
     ```bash
     # Windows: Format → FAT32
     # Linux:
     sudo mkfs.vfat -F 32 /dev/sdX1
     ```

4. **Napájení**
   - SD moduly vyžadují stabilní 3.3V
   - Použijte kvalitní USB kabel/napájení

---

## 🏠 Home Assistant problémy

### ESP32 se neobjeví v HA

**Řešení:**

1. **Zkontrolujte síť**
   - HA a ESP32 musí být na **stejné síti**
   - Zkontrolujte firewall

2. **Manuální přidání**
   - Nastavení → Zařízení a služby
   - \+ Přidat integraci
   - ESPHome
   - Zadejte IP adresu ESP32
   - Zadejte API klíč ze `secrets.yaml`

3. **API klíč**
   ```yaml
   # secrets.yaml
   api_key: "vygenerujte-novy-klic-32-znaku"
   ```
   
   Vygenerujte nový:
   ```bash
   python -c "import secrets; print(secrets.token_hex(16))"
   ```

### Entity nefungují v HA

**Řešení:**

1. **Restart ESP32**
   - Odpojte a znovu připojte USB
   - Nebo v HA: Zařízení → Restartovat

2. **Reload integrace**
   - Nastavení → Zařízení a služby
   - ESPHome → SuperESP → Znovu načíst

3. **Zkontrolujte logy**
   ```bash
   esphome logs firmware/test-blink/main.yaml
   ```

---

## 🐛 Obecné problémy

### Python pip problémy

**"pip není rozpoznán..."**

**Windows:**
```bash
python -m pip install esptool
# nebo:
py -m pip install esptool
```

**Linux/Mac:**
```bash
python3 -m pip install esptool
```

### Git problémy

**"git není rozpoznán..."**

Instalujte Git:
- **Windows:** https://git-scm.com/download/win
- **Linux:** `sudo apt install git` (Debian/Ubuntu)
- **macOS:** `brew install git`

### Obecná performance

**ESP32 pomalé, laguje**

1. **Přetížená WiFi**
   - Snižte scan interval
   - Použijte kvalitnější router

2. **Log level příliš verbose**
   ```yaml
   logger:
     level: INFO  # místo DEBUG
   ```

3. **Restart ESP32**
   - Memory leak? Restart pomůže

---

## 📞 Získání pomoci

Pokud výše uvedené nepomohlo:

### 1. Zkontrolujte GitHub Issues
https://github.com/skokycz/SuperESP/issues

### 2. Vytvořte nový Issue

**Zahrňte:**
- **Popis problému** (co děláte, co se stane)
- **Hardware:** ESP32 typ, verze
- **Software:** ESPHome verze, OS
- **Logy:**
  ```bash
  esphome logs main.yaml > logs.txt
  ```
- **Config:** Relevantní části YAML (BEZ hesel!)

### 3. Community

- **ESPHome Discord:** https://discord.gg/KhAMKrd
- **Home Assistant Community:** https://community.home-assistant.io/
- **ESP32 subreddit:** r/esp32

---

## 🔍 Debugging Tips

### Zobrazit detailní logy

```bash
esphome logs main.yaml --verbose
```

### Web serial (Chrome/Edge)

1. Otevřete https://web.esphome.io/
2. Connect → Vyberte COM port
3. Uvidíte real-time logy v prohlížeči!

### Serial monitor (manual)

**Windows:**
```bash
# PuTTY nebo:
mode COM3 BAUD=115200 PARITY=N DATA=8
```

**Linux/Mac:**
```bash
screen /dev/ttyUSB0 115200
# nebo:
minicom -D /dev/ttyUSB0 -b 115200
```

### Ping test

```bash
ping <IP_ESP32>

# Continuous ping (Linux):
ping -i 1 <IP_ESP32>

# Traceroute:
traceroute <IP_ESP32>
```

### WiFi scan (ověření 2.4GHz)

**Windows:**
```bash
netsh wlan show networks mode=bssid
```

**Linux:**
```bash
sudo iwlist wlan0 scan | grep -E "ESSID|Frequency"
```

**macOS:**
```bash
/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s
```

Zkontrolujte, že vaše síť vysílá na **2.4GHz (channel 1-13)**.

---

## ✅ Checklist před hlášením problému

Než vytvoříte issue, zkontrolujte:

- [ ] Přečetl jsem SETUP.md
- [ ] Zkontroloval jsem TROUBLESHOOTING.md (tento dokument)
- [ ] Ověřil jsem hardware zapojení (HARDWARE.md)
- [ ] Použil jsem správné USB data kabel
- [ ] Nainstaloval jsem USB-Serial driver
- [ ] secrets.yaml existuje a má správné údaje
- [ ] WiFi je 2.4GHz (ne 5GHz)
- [ ] Zkusil jsem flash recovery
- [ ] Zkusil jsem smazat .esphome cache
- [ ] Mám aktuální verzi ESPHome
- [ ] Zkontroloval jsem existující GitHub Issues

---

**Hodně štěstí! Většina problémů se vyřeší jedním z výše uvedených řešení.** 🍀

*Last updated: BLOK 1*
