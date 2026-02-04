# SuperESP Hardware Specifikace

Kompletní hardware dokumentace pro SuperESP projekt.

---

## 🎯 ESP32-C3 Super Mini

### Základní specifikace
- **MCU:** ESP32-C3 (RISC-V single-core @ 160MHz)
- **WiFi:** 2.4GHz 802.11 b/g/n
- **Flash:** 4MB
- **RAM:** 400KB SRAM
- **GPIO:** 13 dostupných pinů
- **Rozměry:** ~22.5 x 18 mm
- **USB:** USB-C (nativní USB Serial/JTAG)
- **Napájení:** 5V (USB-C) nebo 3.3V (pin)

### Pinout ESP32-C3 Super Mini

```
                    ┌─────────────┐
                    │   USB-C     │
                    └──────┬──────┘
                           │
         GND  ●────────────┴────────────● 3V3
         GND  ●─────────────────────────● GND
          0   ●─────────────────────────● 1
          2   ●─────────────────────────● 10
          3   ●─────────────────────────● 9
          4   ●─────────────────────────● 8 (LED)
          5   ●─────────────────────────● 7 (SPI)
          6   ●─────────────────────────● 6 (SPI)
         20   ●─────────────────────────● 21
                    └──────────────┘
```

### GPIO funkce

| Pin | Funkce | Poznámky |
|-----|--------|----------|
| **GPIO0** | General I/O | Boot tlačítko (LOW při startu = download mode) |
| **GPIO1** | General I/O, UART TX | - |
| **GPIO2** | General I/O, ADC1_CH2 | - |
| **GPIO3** | General I/O, UART RX | - |
| **GPIO4** | General I/O, ADC1_CH4 | - |
| **GPIO5** | General I/O, ADC2_CH0 | SPI CS (pokud vytržen, použij jiný) |
| **GPIO6** | General I/O | **SPI CLK** ⚠️ Často vytržen |
| **GPIO7** | General I/O | **SPI MISO** ⚠️ Často vytržen |
| **GPIO8** | General I/O | **Onboard LED** (inverted) 💡 |
| **GPIO9** | General I/O | Boot button |
| **GPIO10** | General I/O | - |
| **GPIO20** | General I/O, UART RX | Alternative UART |
| **GPIO21** | General I/O, UART TX | Alternative UART |

⚠️ **Pozor:** GPIO 6 a 7 jsou často vytržené na levných boardech!

---

## 🔌 Zapojení - Plná verze (všechny GPIO)

Pokud máte ESP32-C3 se všemi piny:

### Master ESP (s DHT22 a SD kartou)

```
ESP32-C3 Master
├── GPIO2  → DHT22 Data
├── GPIO4  → SD Card CS
├── GPIO5  → SD Card MOSI
├── GPIO6  → SD Card CLK
├── GPIO7  → SD Card MISO
├── GPIO20 → UART RX (Scanner 1)
├── GPIO21 → UART TX (Scanner 1)
└── GPIO8  → Onboard LED (status)
```

### Scanner ESP 1 & 2 (skenování WiFi)

```
ESP32-C3 Scanner
├── GPIO20 → UART RX (Master nebo Scanner 2)
├── GPIO21 → UART TX (Master nebo Scanner 2)
└── GPIO8  → Onboard LED (status)
```

---

## 🔧 Zapojení - Bez GPIO 6,7 (alternativní SPI)

Pokud máte vytržené GPIO 6 a 7, použijte alternativní zapojení.

### Varianta A: Bez SD karty
Jednoduše nepoužívejte SD kartu modul. Všechna data pouze přes UART/WiFi.

### Varianta B: Software SPI (pomalejší)
Použijte jiné piny pro SPI:

```
ESP32-C3 Master (software SPI)
├── GPIO2  → DHT22 Data
├── GPIO3  → SD Card CS
├── GPIO4  → SD Card MOSI
├── GPIO5  → SD Card CLK   (software SPI)
├── GPIO10 → SD Card MISO  (software SPI)
├── GPIO20 → UART RX (Scanner 1)
├── GPIO21 → UART TX (Scanner 1)
└── GPIO8  → Onboard LED
```

**ESPHome konfigurace:**
```yaml
spi:
  clk_pin: GPIO5
  mosi_pin: GPIO4
  miso_pin: GPIO10
  # software SPI mode
```

---

## 🔋 Napájení - Bez 5V pinu

Pokud máte vytržený 5V pin, máte několik možností:

### Varianta A: USB-C napájení (doporučeno)
- Připojte každé ESP32 přes USB-C
- Nejjednodušší a nejspolehlivější
- USB hub s napájením

### Varianta B: 3.3V pin
- Přiveďte stabilizované 3.3V na 3V3 pin
- **POZOR:** Max ~500mA
- Použijte regulátor (např. AMS1117-3.3)

### Varianta C: Pájet přímo na board
- Pouze pro pokročilé!
- Najděte 5V pad na PCB
- Přiletujte kabel

---

## 📡 Kompletní cluster - 3x ESP32-C3

### Topologie

```
        ┌──────────────────────────────┐
        │    ESP32-C3 Master           │
        │  ┌──────────┐  ┌──────────┐  │
        │  │  DHT22   │  │ SD Card  │  │
        │  └────┬─────┘  └────┬─────┘  │
        │       │             │         │
        │    GPIO2         GPIO4-7      │
        └───────┬────────────┬──────────┘
                │            │
      ┌─────────┴────────────┴─────────┐
      │      UART (GPIO20/21)          │
      │                                 │
  ┌───┴────────┐              ┌────────┴───┐
  │  Scanner 1 │──────────────│  Scanner 2 │
  │  ESP32-C3  │  UART (20/21)│  ESP32-C3  │
  └────────────┘              └────────────┘
```

### Propojení UART

**Master ↔ Scanner 1:**
```
Master GPIO21 (TX) → Scanner1 GPIO20 (RX)
Master GPIO20 (RX) → Scanner1 GPIO21 (TX)
GND ──────────────── GND
```

**Scanner 1 ↔ Scanner 2:**
```
Scanner1 GPIO3 (TX) → Scanner2 GPIO20 (RX)
Scanner1 GPIO2 (RX) → Scanner2 GPIO21 (TX)
GND ────────────────── GND
```

💡 **Tip:** Použijte dupont kabely, breadboard nebo custom PCB.

---

## 🧩 Seznam součástek

### Minimální sestava (BLOK 1)
- [x] 1x ESP32-C3 Super Mini
- [x] 1x USB-C kabel (data)
- [x] 1x Počítač

### Základní sestava (BLOK 2-4)
- [ ] 3x ESP32-C3 Super Mini (~$2-3/ks)
- [ ] 3x USB-C kabel
- [ ] 1x DHT22 sensor (~$3)
- [ ] 1x SD Card Reader (SPI) (~$1)
- [ ] 1x microSD karta (1-32GB)
- [ ] 10x Dupont kabely (F-F)
- [ ] 1x Breadboard (optional)

### Plná sestava (BLOK 5-12)
- Výše uvedené +
- [ ] 1x SPST-102 switch (~$0.5)
- [ ] 1x 3.3V regulátor (pokud bez 5V)
- [ ] Krabička/case (3D print?)

### Volitelné
- [ ] Custom PCB pro cluster
- [ ] Antény pro WiFi (SMA connector)
- [ ] OLED display (128x64, I2C)
- [ ] RGB LED pro fancy status

---

## 🔍 Detailní schéma zapojení

### DHT22 připojení

```
DHT22               ESP32-C3
┌──────┐           ┌──────────┐
│  VCC │───────────│ 3V3      │
│  GND │───────────│ GND      │
│ DATA │───────────│ GPIO2    │
└──────┘           └──────────┘
      │
    [10kΩ]  (pull-up resistor mezi VCC a DATA)
      │
    ──┴──
```

### SD Card (SPI)

```
SD Card Module      ESP32-C3
┌──────────┐       ┌──────────┐
│   VCC    │───────│ 3V3      │
│   GND    │───────│ GND      │
│   CS     │───────│ GPIO4    │
│   MOSI   │───────│ GPIO5    │
│   CLK    │───────│ GPIO6    │
│   MISO   │───────│ GPIO7    │
└──────────┘       └──────────┘
```

**Pokud GPIO 6,7 vytržené:**
```
SD Card Module      ESP32-C3 (software SPI)
┌──────────┐       ┌──────────┐
│   VCC    │───────│ 3V3      │
│   GND    │───────│ GND      │
│   CS     │───────│ GPIO3    │
│   MOSI   │───────│ GPIO4    │
│   CLK    │───────│ GPIO5    │
│   MISO   │───────│ GPIO10   │
└──────────┘       └──────────┘
```

### UART propojení

```
Master ESP          Scanner ESP
┌──────────┐       ┌──────────┐
│ GPIO21   │───────│ GPIO20   │  (TX → RX)
│ GPIO20   │───────│ GPIO21   │  (RX → TX)
│ GND      │───────│ GND      │
└──────────┘       └──────────┘
```

---

## 📐 Fyzické uspořádání

### Desktop verze (breadboard)
```
┌────────────────────────────────────────┐
│  Breadboard                            │
│                                         │
│  [ESP32]  [ESP32]  [ESP32]             │
│    │        │        │                  │
│  [DHT22] [SD Card]                     │
│                                         │
└────────────────────────────────────────┘
```

### Kompaktní verze (custom PCB)
```
┌─────────────┐
│  ┌────┐     │
│  │ESP1│     │
│  └┬──┬┘     │
│   │  │      │
│  ┌▼──▼┐     │
│  │ESP2│ SD  │
│  └┬──┬┘ DHT │
│   │  │      │
│  ┌▼──▼┐     │
│  │ESP3│     │
│  └────┘     │
└─────────────┘
```

---

## ⚡ Spotřeba energie

| Režim | Jeden ESP32 | 3x ESP32 cluster |
|-------|-------------|------------------|
| **Idle** | ~80mA @ 3.3V | ~240mA |
| **WiFi Active** | ~120mA | ~360mA |
| **Scan Mode** | ~160mA | ~480mA |
| **Deep Sleep** | ~10μA | ~30μA |

**Napájení:**
- USB-C (5V, min 1A): ✅ Dostatečné
- Powerbank (2A): ✅ Ideální pro portable
- 3.3V regulátor: Min 500mA (1A doporučeno)

---

## 🛡️ Ochrana a bezpečnost

### Doporučené ochrany
1. **Dioda na napájení** - ochrana proti reverzní polaritě
2. **TVS dioda na GPIO** - ochrana proti přepětí
3. **10kΩ pull-up** na DHT22 data
4. **100nF kondenzátor** na VCC (každé ESP32)
5. **Plastová krabička** - ochrana před zkratem

### Anti-static
ESP32 je citlivé na ESD! Používejte:
- Anti-static náramek při pájení
- Avoid touching piny přímo
- Skladujte v anti-static obalu

---

## 📚 Odkazy a zdroje

### Datasheets
- [ESP32-C3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf)
- [ESP32-C3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-c3_technical_reference_manual_en.pdf)
- [DHT22 Datasheet](https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf)

### Nákup součástek
- **AliExpress:** ESP32-C3 Super Mini, DHT22, SD moduly
- **TME/GM Electronic (CZ):** Kvalitní součástky, rychlé doručení
- **Laskakit (CZ):** Český eshop s ESP32 a sensory

---

## 💡 Tipy a triky

### Problém: Vytržené GPIO 6,7
- Použijte software SPI (pomalejší, ale funguje)
- Nebo se vyhn SD kartě úplně

### Problém: Vytržený 5V pin
- USB-C napájení (nejlepší)
- 3.3V regulátor z externího zdroje

### Tip: Testování pinů
```yaml
# ESPHome test všech GPIO
switch:
  - platform: gpio
    name: "Test GPIO2"
    pin: GPIO2
```

### Tip: Deep sleep pro baterii
```yaml
deep_sleep:
  run_duration: 10s
  sleep_duration: 5min
```

---

**Hardware dokumentace hotovo!** 🔧

Další kroky: [SETUP.md](SETUP.md) | [ROADMAP.md](ROADMAP.md)
