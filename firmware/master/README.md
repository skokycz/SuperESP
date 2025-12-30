# SuperESP Master Firmware (BLOK 2)

Firmware pro Master ESP32-C3 s DHT22 senzorem a OLED displejem SSD1306.

## 📋 Funkce

- 🌡️ **DHT22 sensor** - měření teploty a vlhkosti
- 📺 **OLED displej 0.96"** - zobrazení dat (SSD1306, 128x64, I2C)
- 📊 **Dvě stránky displeje** - automatické přepínání každých 5 sekund
- 📡 **WiFi monitoring** - stav připojení, IP adresa, síla signálu
- 🏠 **Home Assistant integrace** - export všech sensorů
- 🌐 **Web server** - monitoring přes prohlížeč
- 🔄 **OTA aktualizace** - bezdrátové nahrávání firmware

## 🔌 Hardware zapojení

### ESP32-C3 Super Mini pinout

```
         ESP32-C3 Super Mini
         ┌─────────────────┐
    3V3  │ 3V3         GND │  GND
         │ GPIO0      GPIO1│
   DHT22 │ GPIO2      GPIO10│
         │ GPIO3      GPIO20│
         │ GPIO4      GPIO21│
         │ GPIO5      GPIO8 │  (LED)
         │ GPIO6      GPIO9 │
         │ GPIO7           │
         └─────────────────┘
```

### OLED SSD1306 zapojení

```
OLED Pin    →    ESP32-C3 Pin    →    Popis
─────────────────────────────────────────────
VCC         →    3.3V             →    Napájení
GND         →    GND              →    Zem
SDA         →    GPIO1            →    I2C Data
SCL         →    GPIO0            →    I2C Clock
```

### DHT22 zapojení

```
DHT22 Pin   →    ESP32-C3 Pin    →    Popis
─────────────────────────────────────────────
VCC         →    3.3V             →    Napájení
DATA        →    GPIO2            →    Data signál
GND         →    GND              →    Zem
```

**Poznámka:** DHT22 může vyžadovat pull-up rezistor 4.7kΩ mezi DATA a VCC.

### Alternativní I2C piny

Pokud GPIO0 a GPIO1 nejsou dostupné (některé desky mají vytržené GPIO6/7), můžete použít:

```yaml
i2c:
  sda: GPIO4
  scl: GPIO5
  scan: true
```

## 📺 OLED displej - stránky

Displej automaticky přepína mezi dvěma stránkami každých 5 sekund.

### Stránka 1 - Hlavní informace

```
┌────────────────────────┐
│ SuperESP Master        │
│────────────────────────│
│ Teplota: 22.5°C        │
│ Vlhkost: 45.2%         │
│                        │
│ WiFi: Connected        │
│ IP: 192.168.1.100      │
└────────────────────────┘
```

**Zobrazuje:**
- Název zařízení
- Aktuální teplota (z DHT22)
- Aktuální vlhkost (z DHT22)
- Stav WiFi připojení
- IP adresa nebo AP mode info

### Stránka 2 - Systémové informace

```
┌────────────────────────┐
│ System Info            │
│────────────────────────│
│ Uptime: 2h 35m         │
│ Signal: -42 dBm        │
│                        │
│ ESPHome                │
│ BLOK 2 - Master        │
└────────────────────────┘
```

**Zobrazuje:**
- Uptime zařízení
- Síla WiFi signálu
- Verze firmware
- Identifikace bloku

## 🚀 Instalace

### 1. Příprava secrets

```bash
cd firmware/master
cp secrets.yaml.example secrets.yaml
```

Upravte `secrets.yaml` a vyplňte:
- WiFi SSID a heslo
- API klíč (vygenerujte: `openssl rand -base64 32`)
- OTA heslo

### 2. Kompilace a nahrání

```bash
# Z kořenového adresáře projektu
esphome run firmware/master/main.yaml
```

Nebo přes USB:

```bash
esphome run firmware/master/main.yaml --device /dev/ttyUSB0
```

### 3. Ověření

Po nahrání firmware:

1. **LED kontrola** - pokud máte LED na GPIO8, měla by svítit
2. **Web rozhraní** - otevřete http://superesp-master.local v prohlížeči
3. **Home Assistant** - zařízení by se mělo objevit automaticky
4. **OLED displej** - měl by zobrazovat data a přepínat stránky

## 🔍 Troubleshooting

### OLED displej nezobrazuje nic

1. **Zkontrolujte zapojení:**
   - VCC na 3.3V (NIKOLI 5V!)
   - GND na GND
   - SDA na GPIO1
   - SCL na GPIO0

2. **Zkontrolujte I2C adresu:**
   
   V logách ESPHome hledejte:
   ```
   [I][i2c:028]: Found i2c device at address 0x3C
   ```
   
   Pokud vidíte `0x3D` místo `0x3C`, upravte v `main.yaml`:
   ```yaml
   display:
     - platform: ssd1306_i2c
       address: 0x3D  # Změna z 0x3C
   ```

3. **Pokud I2C scan nic nenajde:**
   - Zkontrolujte fyzické připojení
   - Zkuste vyměnit SDA a SCL
   - Vyzkoušejte alternativní piny (GPIO4/GPIO5)

### DHT22 nevrací data

1. **Přidejte pull-up rezistor** 4.7kΩ mezi DATA pin a 3.3V
2. **Zkontrolujte napájení** - DHT22 může vyžadovat stabilní 3.3V
3. **Prodlužte update interval:**
   ```yaml
   sensor:
     - platform: dht
       update_interval: 120s  # Původně 60s
   ```

### WiFi se nepřipojí

1. **Zkontrolujte secrets.yaml** - správné SSID a heslo
2. **Zapněte Fallback AP:**
   
   ESP vytvoří vlastní AP s názvem "SuperESP-Master" a heslem "superesp123"
   
3. **Připojte se k AP** a konfigurujte WiFi přes captive portal

### ESPHome kompilace selhává

1. **Aktualizujte ESPHome:**
   ```bash
   pip install --upgrade esphome
   ```

2. **Zkontrolujte Python verzi** (vyžadováno 3.8+):
   ```bash
   python --version
   ```

3. **Vyčistěte cache:**
   ```bash
   esphome clean firmware/master/main.yaml
   esphome run firmware/master/main.yaml
   ```

## 📊 Home Assistant integrace

Po připojení k Home Assistant budou dostupné tyto entity:

### Sensory
- `sensor.superesp_master_temperature` - Teplota
- `sensor.superesp_master_humidity` - Vlhkost
- `sensor.superesp_master_uptime` - Uptime
- `sensor.superesp_master_wifi_signal` - WiFi signál

### Binary Sensors
- `binary_sensor.superesp_master_status` - Status připojení

### Text Sensors
- `text_sensor.superesp_master_ip_address` - IP adresa
- `text_sensor.superesp_master_connected_ssid` - Připojené SSID
- `text_sensor.superesp_master_mac_address` - MAC adresa
- `text_sensor.superesp_master_esphome_version` - Verze ESPHome

### Příklad automatizace

```yaml
automation:
  - alias: "SuperESP vysoká teplota alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.superesp_master_temperature
        above: 30
    action:
      - service: notify.mobile_app
        data:
          message: "Vysoká teplota! {{ states('sensor.superesp_master_temperature') }}°C"
```

## 🔧 Pokročilá konfigurace

### Změna update intervalů

V `main.yaml` upravte:

```yaml
sensor:
  - platform: dht
    update_interval: 30s  # Častější měření
```

### Deaktivace displeje v noci

Přidejte do `main.yaml`:

```yaml
time:
  - platform: homeassistant
    id: homeassistant_time

display:
  - platform: ssd1306_i2c
    # ... existující konfigurace
    lambda: |-
      auto time = id(homeassistant_time).now();
      if (time.hour >= 22 || time.hour < 7) {
        // Displej vypnutý v noci (22:00 - 7:00)
        return;
      }
      // ... zbytek kódu displeje
```

### Přidání SD karty (budoucí - BLOK 2 rozšíření)

SD karta bude přidána v další iteraci BLOK 2 pro logging dat.

## 📁 Struktura souborů

```
firmware/master/
├── main.yaml                 # Hlavní konfigurace
├── secrets.yaml.example      # Template pro secrets
├── secrets.yaml              # Vaše secrets (gitignored)
└── README.md                 # Tato dokumentace
```

## 🔗 Odkazy

- [ESPHome dokumentace](https://esphome.io/)
- [SSD1306 Display Component](https://esphome.io/components/display/ssd1306.html)
- [DHT Sensor Component](https://esphome.io/components/sensor/dht.html)
- [ESP32 Pinout Reference](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)

## ⚡ Next Steps (BLOK 2 pokračování)

- [ ] Přidat SD kartu logging
- [ ] Implementovat CSV formát pro data
- [ ] Přidat real-time grafy v web UI
- [ ] UART komunikace se Scanner ESP

---

**BLOK 2 Status:** 🚧 V Průběhu
**Datum vytvoření:** 2024-12
**Poslední update:** 2024-12
