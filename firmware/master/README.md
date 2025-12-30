# SuperESP Master - Firmware dokumentace

Master ESP32-C3 s DHT22 senzorem pro monitoring teploty a vlhkosti.

---

## 🎯 Přehled

**SuperESP Master** je hlavní jednotka clusteru, která:
- 📊 Měří teplotu a vlhkost pomocí DHT22
- 📡 Připojuje se k WiFi a Home Assistant
- 🌐 Poskytuje webové rozhraní pro monitoring
- 💾 Připraveno pro SD kartu logging (volitelné - BLOK 2.5)
- 🔗 Komunikuje se Scanner ESP jednotkami přes UART (BLOK 4)

---

## 🔧 Hardware požadavky

### Základní sestava
- ✅ **ESP32-C3 Super Mini** (4MB flash)
- ✅ **DHT22** sensor (teplota & vlhkost)
- ✅ **10kΩ resistor** (pull-up pro DHT22)
- ✅ **USB-C kabel** (napájení + programování)
- ✅ **3x Dupont kabely** (F-F) pro DHT22

### Volitelné rozšíření
- 📦 **SD Card Reader** (SPI modul)
- 💾 **microSD karta** (1-32GB)
- 🔌 **Breadboard** pro snadné zapojení

---

## 📐 Pinout a zapojení

### GPIO použití na Master ESP

```
ESP32-C3 Super Mini - MASTER
┌─────────────────────────────┐
│         USB-C               │
│           ║                 │
│  GND ●────╨────────────● 3V3│
│  GND ●─────────────────● GND│
│    0 ●─────────────────● 1  │
│    2 ●─[DHT22 DATA]────● 10 │
│    3 ●─(SD MISO)*──────● 9  │
│    4 ●─(SD CLK)*───────● 8  │ ← LED (onboard)
│    5 ●─(SD MOSI)*──────● 7  │
│    6 ●─────────────────● 6  │
│   20 ●─(UART RX)*──────● 21 │ ← (UART TX)*
└─────────────────────────────┘

* Volitelné - pro budoucí rozšíření
```

### Zapojení DHT22

```
DHT22                 ESP32-C3 Master
┌──────────┐         ┌──────────┐
│   VCC    │─────────│ 3V3      │
│   GND    │─────────│ GND      │
│   DATA   │─────────│ GPIO2    │
└────┬─────┘         └──────────┘
     │
   [10kΩ]  ← Pull-up resistor mezi VCC a DATA
     │
   ──┴──
```

**Důležité:**
- ⚠️ Pull-up 10kΩ resistor je **NUTNÝ** pro stabilní komunikaci
- 💡 DHT22 má 3 nebo 4 piny (podle modulu), použijte jen VCC, GND, DATA
- 🔌 Napájení DHT22 je 3.3V (ESP32-C3 nemá 5V tolerantní GPIO)

### Zapojení SD karty (volitelné - BLOK 2.5)

**Pro desky BEZ vytržených GPIO 6/7:**
```
SD Card Module      ESP32-C3
┌──────────┐       ┌──────────┐
│   VCC    │───────│ 3V3      │
│   GND    │───────│ GND      │
│   CS     │───────│ GPIO10   │
│   MOSI   │───────│ GPIO5    │
│   CLK    │───────│ GPIO6    │
│   MISO   │───────│ GPIO7    │
└──────────┘       └──────────┘
```

**Pro desky s vytržený GPIO 6/7 (alternativní SPI):**
```
SD Card Module      ESP32-C3 (software SPI)
┌──────────┐       ┌──────────┐
│   VCC    │───────│ 3V3      │
│   GND    │───────│ GND      │
│   CS     │───────│ GPIO10   │
│   MOSI   │───────│ GPIO5    │
│   CLK    │───────│ GPIO4    │
│   MISO   │───────│ GPIO3    │
└──────────┘       └──────────┘
```

💡 **Poznámka:** SD karta integrace je připravena v `sd_card.yaml`, ale vyžaduje další vývoj v BLOK 2.5.

---

## 🚀 Instalace a první spuštění

### Krok 1: Příprava secrets

```bash
cd firmware/master/
cp secrets.yaml.example secrets.yaml
```

Otevřete `secrets.yaml` a vyplňte:
```yaml
wifi_ssid: "VaseWiFiSSID"
wifi_password: "VaseWiFiHeslo"
api_key: "32-znakovy-nahodny-klic"  # Vygenerujte náhodně
ota_password: "vaseOTAheslo"
ap_password: "fallback123"  # Pro fallback AP
```

**Generování API klíče:**
```bash
# Linux/Mac
openssl rand -base64 32

# Python (kdykoliv)
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Krok 2: Zapojení hardware

1. **DHT22:**
   - VCC → 3V3
   - GND → GND
   - DATA → GPIO2
   - 10kΩ resistor mezi VCC a DATA

2. **ESP32-C3:**
   - Připojte USB-C kabel

### Krok 3: Flash firmware

**První flash (přes USB):**
```bash
esphome run main.yaml
```

Vyberte sériový port (např. `/dev/ttyUSB0` nebo `COM3`)

**Další flashování (přes OTA):**
```bash
esphome run main.yaml
```

Vyberte "Wirelessly" a IP adresu ESP

### Krok 4: Ověření funkčnosti

1. **LED bliká** každých 60s při měření → ✅ Firmware běží
2. **Připojení k WiFi:**
   - Zkontrolujte router (zařízení "superesp-master")
   - Nebo se připojte k AP "SuperESP-Master" (pokud WiFi selhalo)

3. **Web interface:**
   - Otevřete `http://superesp-master.local` nebo IP adresu
   - Měli byste vidět teplotu a vlhkost

4. **Home Assistant:**
   - ESPHome integrace automaticky detekuje zařízení
   - Přidejte pomocí API klíče ze `secrets.yaml`

---

## 🌐 WiFi konfigurace a troubleshooting

### WiFi workaroundy (kritické pro ESP32-C3!)

Firmware obsahuje několik důležitých workaroundů pro stabilitu WiFi:

```yaml
esp32:
  framework:
    type: arduino  # ← NE esp-idf! Arduino má lepší WiFi support

wifi:
  fast_connect: false        # ← Důležité! Pomáhá s Auth Expired
  power_save_mode: none      # ← Vypne power saving (stabilnější)
  output_power: 8.5dB        # ← Snížený výkon (méně problémů)
  reboot_timeout: 0s         # ← Nikdy se nerestartuje kvůli WiFi
```

### Řešení problému "Auth Expired"

**Příznaky:**
- ESP se připojí, pak se odpojí s "Auth Expired"
- V logu vidíte `WIFI_REASON_AUTH_EXPIRE`

**Řešení:**

1. **Router nastavení (doporučeno):**
   - Vypněte **PMF** (Protected Management Frames)
   - Nastavte **WPA2-PSK** (NE WPA3!)
   - Kanál: Fixní 1-11 (ne Auto)
   - Šířka: 20MHz (ne 40MHz nebo Auto)

2. **Firmware už obsahuje workaroundy:**
   - ✅ `fast_connect: false`
   - ✅ `power_save_mode: none`
   - ✅ `output_power: 8.5dB`
   - ✅ `framework: arduino`

3. **Pokud stále nefunguje:**
   - Zkuste jiný WiFi router/AP
   - Použijte 2.4GHz hotspot z mobilu (test)
   - Zkontrolujte sílu signálu (RSSI > -70dBm)

### Fallback AP režim

Pokud se ESP nepřipojí k WiFi, automaticky spustí:
- **SSID:** `SuperESP-Master`
- **Heslo:** `fallback123` (z `secrets.yaml`)

Připojte se a otevřete `http://192.168.4.1`

---

## 📊 Monitorované hodnoty

### Sensory

| Sensor | Jednotka | Update interval | Poznámka |
|--------|----------|-----------------|----------|
| **Teplota** | °C | 60s | DHT22, přesnost ±0.5°C |
| **Vlhkost** | % | 60s | DHT22, přesnost ±2% |
| **WiFi Signal** | dBm | 60s | Síla WiFi signálu |
| **Uptime** | s | 60s | Čas běhu od restartu |

### Text sensory

| Sensor | Popis |
|--------|-------|
| **IP Address** | Aktuální IP adresa |
| **Connected SSID** | Název připojené WiFi sítě |
| **MAC Address** | MAC adresa ESP |
| **ESPHome Version** | Verze ESPHome firmwaru |

### Binary sensory

| Sensor | Popis |
|--------|-------|
| **Status** | Online/Offline stav |

---

## 🏠 Home Assistant integrace

### Automatická detekce

1. **ESPHome integrace** by měla automaticky najít "SuperESP Master"
2. Pokud ne, přidejte manuálně:
   - Configuration → Integrations → Add Integration
   - Vyberte "ESPHome"
   - Zadejte IP nebo `superesp-master.local`
   - Zadejte encryption key ze `secrets.yaml`

### Entity v Home Assistant

Po přidání budete mít:
```
sensor.superesp_master_teplota
sensor.superesp_master_vlhkost
sensor.superesp_master_wifi_signal
sensor.superesp_master_uptime
sensor.superesp_master_ip_address
sensor.superesp_master_connected_ssid
sensor.superesp_master_mac_address
sensor.superesp_master_esphome_version
binary_sensor.superesp_master_status
light.superesp_master_status_led
```

### Příklad použití v Lovelace

```yaml
type: entities
title: SuperESP Master
entities:
  - entity: sensor.superesp_master_teplota
    name: Teplota
  - entity: sensor.superesp_master_vlhkost
    name: Vlhkost
  - entity: sensor.superesp_master_wifi_signal
    name: WiFi Signál
  - entity: binary_sensor.superesp_master_status
    name: Status
```

---

## 🔧 Pokročilá konfigurace

### Změna update intervalu

V `main.yaml` upravte:
```yaml
sensor:
  - platform: dht
    # ...
    update_interval: 30s  # ← Změňte na 30s místo 60s
```

### Přidání notifikací

```yaml
# V main.yaml
on_...:
  then:
    - homeassistant.service:
        service: notify.mobile_app
        data:
          message: "Teplota vysoká: {{ states('sensor.superesp_master_teplota') }}°C"
```

### Přidání SD karty

1. Zapojte SD modul podle schématu výše
2. V `main.yaml` přidejte:
   ```yaml
   packages:
     sd_card: !include sd_card.yaml
   ```
3. TODO: Dokončit implementaci v BLOK 2.5

---

## 🐛 Troubleshooting

### DHT22 nečte hodnoty

**Příznaky:**
- Sensor ukazuje "Unknown" nebo "nan"
- V logu: `Failed to read from DHT sensor`

**Řešení:**
1. ✅ Zkontrolujte zapojení (VCC, GND, DATA)
2. ✅ **10kΩ resistor** mezi VCC a DATA (nejčastější problém!)
3. ✅ Kabely ne delší než 20cm
4. ✅ DHT22 není vadný (test jiným ESP/Arduino)
5. Zkuste jiné GPIO (např. GPIO1, GPIO10)

### LED nebliká

**Příznaky:**
- Onboard LED nesvítí/nebliká

**Řešení:**
1. LED je **inverted**, bliká při měření (60s interval)
2. Zkontrolujte v web UI: `light.status_led` zapnout manuálně
3. Některé desky mají LED na jiném GPIO (většinou GPIO8)

### WiFi se nepřipojí

Viz sekce [WiFi konfigurace a troubleshooting](#-wifi-konfigurace-a-troubleshooting) výše.

### OTA selhává

**Příznaky:**
- "Bad Answer" nebo timeout při OTA

**Řešení:**
1. Použijte stejnou síť jako ESP (ne přes VPN)
2. Zkuste přes USB kabel
3. Restartujte ESP (odpojte/zapojte napájení)
4. Zkontrolujte `ota_password` ve `secrets.yaml`

---

## 📚 Další kroky

Po zprovoznění Master ESP:

1. **BLOK 2.5:** Přidat SD kartu logging
2. **BLOK 3:** Scanner ESP firmware (WiFi skenování)
3. **BLOK 4:** UART komunikace Master ↔ Scanner
4. **BLOK 5:** Rozšířená Home Assistant integrace
5. **BLOK 6-8:** Web UI ve stylu JARVIS

---

## 📖 Reference

- [ESPHome dokumentace](https://esphome.io/)
- [ESP32-C3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [DHT22 Datasheet](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)
- [SuperESP HARDWARE.md](../../docs/HARDWARE.md)
- [SuperESP TROUBLESHOOTING.md](../../docs/TROUBLESHOOTING.md)

---

## 🤝 Podpora

- **Issues:** [GitHub Issues](https://github.com/skokycz/SuperESP/issues)
- **Main README:** [SuperESP README](../../README.md)
- **Roadmap:** [docs/ROADMAP.md](../../docs/ROADMAP.md)

---

**Master ESP firmware úspěšně nainstalován! ✅**

<p align="center">
  <i>"JARVIS, jak je teplota?" - Coming soon in BLOK 6-8 🦾</i>
</p>
