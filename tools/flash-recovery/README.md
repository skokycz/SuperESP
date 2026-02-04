# SuperESP Flash Recovery Tool

Nástroj pro obnovu ESP32-C3 po flashnutí ESP-IDF firmware, který brání instalaci ESPHome.

## Použití

### Instalace závislostí

```bash
pip install -r requirements.txt
```

### Základní použití

**Auto-detekce portu:**
```bash
python recover.py
```

**Specifikace portu:**

Windows:
```bash
python recover.py --port COM3
```

Linux:
```bash
python recover.py --port /dev/ttyUSB0
```

macOS:
```bash
python recover.py --port /dev/cu.usbserial-0001
```

### Pokročilé parametry

**Pouze ověření připojení (bez mazání):**
```bash
python recover.py --verify-only
```

**Vlastní baud rate (pokud má zařízení problémy):**
```bash
python recover.py --baud 115200
```

**Jiný typ chipu:**
```bash
python recover.py --chip esp32s3
```

**Přeskočení ověření:**
```bash
python recover.py --skip-verify
```

## Řešení problémů

### ESP32 není detekován

1. **Stiskněte tlačítko BOOT** při připojení USB
2. Zkuste **jiný USB kabel** (některé kabely jsou jen pro nabíjení)
3. Zkuste **jiný USB port** na počítači
4. Zkuste **nižší baud rate**: `--baud 115200`
5. Zkontrolujte **ovladače USB-Serial** (CH340, CP2102)

### Windows - ovladače

Pokud Windows nerozpoznává zařízení:
- CH340: https://github.com/nodemcu/nodemcu-devkit/tree/master/Drivers
- CP210x: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

### Linux - oprávnění

Pokud máte problém s přístupem k portu:
```bash
sudo usermod -a -G dialout $USER
# Odhlaste se a znovu přihlaste
```

Nebo dočasně:
```bash
sudo chmod 666 /dev/ttyUSB0
```

## Co dělat po smazání flash

1. **Odpojte a znovu připojte** ESP32
2. **Flashněte ESPHome firmware:**
   ```bash
   cd ../..
   esphome run firmware/test-blink/main.yaml
   ```
3. **Sledujte logy:**
   ```bash
   esphome logs firmware/test-blink/main.yaml
   ```

## Technické detaily

Nástroj provádí:
1. Detekci a ověření ESP32 chipu
2. Kompletní smazání flash paměti (`erase_flash`)
3. Potvrzení úspěšnosti operace

Po smazání je flash paměť prázdná a připravená pro nový firmware (ESPHome, Arduino, ESP-IDF).

## Bezpečnost

- Nástroj **vyžaduje potvrzení** před smazáním
- Použijte `--verify-only` pro **test bez mazání**
- Smazání je **nevratné** - zálohy nejsou možné

## Podpora

Pokud nástroj nefunguje, viz `/docs/TROUBLESHOOTING.md`
