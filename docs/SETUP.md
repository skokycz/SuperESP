# SuperESP Setup Guide

Kompletní návod na zprovoznění SuperESP od začátku až po první běžící firmware.

---

## 📋 Požadavky

### Software
- **Python 3.8+** - pro flash recovery a ESPHome
- **ESPHome** - pro kompilaci a flash firmware
- **Git** - pro klonování repository
- **USB-Serial drivers** - CH340 nebo CP210x (podle ESP32)

### Hardware
- **ESP32-C3 Super Mini** (minimálně 1ks)
- **USB kabel** (data, ne jen nabíjecí!)
- **Počítač** s Windows/Linux/macOS

### Volitelně (pro full setup)
- DHT22 teplotní sensor
- SD Card Reader modul (SPI)
- SPST-102 switch
- Propojovací kabely

---

## 🔧 Instalace

### 1. Klonování repository

```bash
git clone https://github.com/skokycz/SuperESP.git
cd SuperESP
```

### 2. Instalace Python závislostí

```bash
# Flash recovery nástroje
cd tools/flash-recovery
pip install -r requirements.txt
cd ../..

# ESPHome
pip install esphome
```

### 3. Ověření instalace

```bash
# Zkontrolujte esptool
esptool.py version

# Zkontrolujte ESPHome
esphome version
```

**Očekávaný výstup:**
```
esptool.py v4.7.0
...
Version: 2024.x.x
```

---

## 🔥 Flash Recovery (pokud ESP nefunguje)

Pokud jste ESP32 dříve flashli pomocí ESP-IDF nebo Arduino a nyní nejde flashnout ESPHome, proveďte recovery.

### Krok 1: Připojte ESP32
1. Připojte ESP32 k USB portu
2. **Stiskněte a podržte BOOT tlačítko** při zapojování (pokud není rozpoznán)

### Krok 2: Spusťte recovery

**Windows:**
```bash
cd tools/flash-recovery
python recover.py --port COM3
```

**Linux:**
```bash
cd tools/flash-recovery
python recover.py --port /dev/ttyUSB0
```

**macOS:**
```bash
cd tools/flash-recovery
python recover.py --port /dev/cu.usbserial-0001
```

**Auto-detekce (doporučeno):**
```bash
python recover.py
```

### Krok 3: Potvrzení

Nástroj se zeptá na potvrzení:
```
VAROVÁNÍ: Tato operace SMAŽE veškerý obsah flash paměti!
Pokračovat? (ano/ne):
```

Napište `ano` a stiskněte Enter.

### Krok 4: Ověření

Pokud vše proběhlo úspěšně:
```
✓ ÚSPĚCH! ESP32 je připraven pro nový firmware
```

**Problémy?** Viz [Troubleshooting](#-časté-problémy) níže.

---

## 🎯 Flash Test Firmware

Test firmware ověří, že ESP32 funguje správně.

### Krok 1: Konfigurace WiFi

```bash
cd firmware/test-blink

# Zkopírujte vzorový secrets soubor
cp secrets.yaml.example secrets.yaml

# Upravte WiFi údaje
nano secrets.yaml  # nebo jakýkoliv editor
```

**secrets.yaml:**
```yaml
wifi_ssid: "VaseWiFiSSID"
wifi_password: "VaseWiFiHeslo"
api_key: "vygenerujte-nahodny-32znakovy-klic"
ota_password: "vaseOTAheslo"
```

💡 **Tip:** API klíč vygenerujte pomocí:
```bash
python -c "import secrets; print(secrets.token_hex(16))"
```

### Krok 2: Flash firmware

**První flash (USB kabel):**
```bash
esphome run main.yaml
```

ESPHome:
1. Zkompiluje firmware
2. Detekuje USB port
3. Nahraje firmware do ESP32
4. Zobrazí logy

### Krok 3: Ověření funkčnosti

**Vizuální test:**
- LED na ESP32 by měla **blikat každou sekundu** ✅

**WiFi test:**
1. ESP32 se připojí k vaší WiFi
2. V lozích uvidíte IP adresu
3. Otevřete prohlížeč: `http://<IP_adresa>`
4. Uvidíte webové rozhraní s status LED

**Home Assistant test:**
1. Pokud máte HA, ESP32 se objeví v **Integrace**
2. Přidejte ho pomocí API klíče ze `secrets.yaml`
3. Ovládejte LED z HA!

---

## 🏠 Home Assistant integrace (volitelné)

### Automatická detekce

Pokud máte Home Assistant na stejné síti:
1. Jděte do **Nastavení → Zařízení a služby**
2. Klikněte na **+ PŘIDAT INTEGRACI**
3. Vyhledejte **ESPHome**
4. Mělo by se objevit **SuperESP Test**
5. Zadejte API klíč ze `secrets.yaml`

### Manuální přidání

1. Nastavení → Zařízení a služby → + PŘIDAT INTEGRACI
2. Vyberte **ESPHome**
3. Zadejte **IP adresu** ESP32
4. Zadejte **API klíč**

---

## 🔄 OTA Aktualizace (bez kabelu)

Po prvním flash můžete aktualizovat firmware přes WiFi:

```bash
cd firmware/test-blink
esphome run main.yaml
```

ESPHome nabídne:
```
How do you want to upload the firmware?
[1] Over The Air (OTA)
[2] Using USB cable
```

Zvolte **1** pro bezdrátovou aktualizaci! 🎉

---

## 📊 Monitoring a Logy

### Real-time logy

```bash
esphome logs main.yaml
```

nebo

```bash
esphome logs main.yaml --device <IP_adresa>
```

### Web interface

Otevřete v prohlížeči:
```
http://<IP_adresa_ESP32>
```

Uvidíte:
- Status LED (zapnout/vypnout)
- Uptime
- WiFi signal
- IP adresa
- ...

---

## ❗ Časté problémy

### ESP32 není detekován

**Příznaky:**
```
✗ esptool není dostupný
✗ Žádné COM porty nebyly nalezeny
```

**Řešení:**
1. **USB kabel** - Použijte datový kabel (ne jen nabíjecí)
2. **Drivers** - Nainstalujte CH340 nebo CP210x driver
3. **USB port** - Zkuste jiný port na počítači
4. **BOOT tlačítko** - Podržte při zapojování

**Driver links:**
- CH340: https://github.com/nodemcu/nodemcu-devkit/tree/master/Drivers
- CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

### Linux: Permission denied

```bash
# Přidejte uživatele do skupiny dialout
sudo usermod -a -G dialout $USER

# Odhlaste se a znovu přihlaste

# Nebo dočasně:
sudo chmod 666 /dev/ttyUSB0
```

### Flash selhává

**Chyba:**
```
A fatal error occurred: Failed to connect to ESP32
```

**Řešení:**
1. Stiskněte a podržte **BOOT** tlačítko
2. Stiskněte a pusťte **RESET** tlačítko (stále držte BOOT)
3. Pusťte **BOOT** tlačítko
4. Zkuste znovu flash

### ESPHome kompilace selhává

**Chyba:**
```
ERROR Error compiling...
```

**Řešení:**
1. Zkontrolujte `secrets.yaml` - musí existovat a mít správný formát
2. Zkuste smazat cache:
   ```bash
   rm -rf .esphome
   esphome run main.yaml
   ```

### WiFi se nepřipojí

**Příznaky:**
- ESP32 blikne LED, ale v lozích není IP
- Zobrazuje se AP "SuperESP Test Fallback"

**Řešení:**
1. Zkontrolujte **SSID a heslo** v `secrets.yaml`
2. ESP32-C3 podporuje jen **2.4GHz WiFi** (ne 5GHz!)
3. Zkuste se připojit k fallback AP:
   - SSID: `SuperESP Test Fallback`
   - Heslo: `superesp123`
   - Otevřete: `http://192.168.4.1`

---

## 🎓 Další kroky

Po úspěšném zprovoznění test firmware:

### BLOK 2: Master ESP
- Připojení DHT22 teplotního sensoru
- Přidání SD karty pro logging
- UART komunikace

### BLOK 3: Scanner ESP
- WiFi skenování okolních sítí
- Detekce SSID, síly signálu
- Reporting do Master ESP

### BLOK 4: UART komunikace
- Propojení všech 3 ESP32
- Sdílení dat mezi zařízeními

**Detailní roadmap:** [docs/ROADMAP.md](ROADMAP.md)

---

## 📚 Další zdroje

- **ESPHome dokumentace:** https://esphome.io
- **ESP32-C3 datasheet:** https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf
- **SuperESP TROUBLESHOOTING:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **SuperESP HARDWARE:** [HARDWARE.md](HARDWARE.md)

---

## 💬 Pomoc

Pokud máte problémy:
1. Prostudujte [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Zkontrolujte [GitHub Issues](https://github.com/skokycz/SuperESP/issues)
3. Vytvořte nový issue s popisem problému

---

**Úspěšnou instalaci!** 🎉
