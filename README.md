# 🦾 SuperESP

> *"JARVIS, přepni na hackerský mód."* - Iron Man inspirovaný WiFi toolkit pro ESP32-C3

**SuperESP** je pokročilý WiFi hacking a bezpečnostní testovací nástroj postavený na clusteru 3x ESP32-C3 Super Mini. Kombinuje sílu ESP32, ESPHome a Home Assistant do elegantního systému připomínajícího technologie z Iron Man.

![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![ESPHome](https://img.shields.io/badge/ESPHome-2024.x-orange)
![Platform](https://img.shields.io/badge/platform-ESP32--C3-red)

---

## ✨ Hlavní funkce

### 🎯 Aktuální (BLOK 1)
- ✅ **Flash Recovery Tool** - Obnova ESP32-C3 po ESP-IDF
- ✅ **Test Blink Firmware** - Ověření funkčnosti ESP32
- ✅ **Kompletní dokumentace** - Setup, hardware, troubleshooting

### 🚀 Plánované funkce
- 📡 **WiFi Scanner** - Profesionální skenování 2.4GHz sítí
- 🔐 **Handshake Capture** - Zachytávání WPA/WPA2 handshake
- 📊 **Real-time Dashboard** - Web UI ve stylu JARVIS
- 🏠 **Home Assistant integrace** - Plná automatizace
- 💾 **SD karta logging** - Persistent storage dat
- 🌐 **Cloud sync** - Vzdálený přístup k datům
- 🎨 **Iron Man UI** - Futuristické rozhraní s animacemi

---

## 🔧 Hardware

### Základní sestava
- **3x ESP32-C3 Super Mini** (RISC-V, WiFi 2.4GHz, 4MB flash)
- **1x DHT22** (teplota & vlhkost)
- **1x SD Card Reader** (SPI logging)
- **1x SPST-102** (master/scanner mód switch)

### Topologie
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Master    │──────│  Scanner 1  │──────│  Scanner 2  │
│   (WiFi)    │ UART │   (WiFi)    │ UART │   (WiFi)    │
│  + DHT22    │      │             │      │             │
│  + SD Card  │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
```

**Více informací:** [docs/HARDWARE.md](docs/HARDWARE.md)

---

## 🚀 Quick Start

### 1. Instalace závislostí

```bash
# Python nástroje
pip install -r tools/flash-recovery/requirements.txt

# ESPHome (pro firmware)
pip install esphome
```

### 2. Flash Recovery (pokud ESP nebliklo po ESP-IDF)

```bash
cd tools/flash-recovery
python recover.py --port COM3  # Windows
python recover.py --port /dev/ttyUSB0  # Linux
```

### 3. Flash test firmware

```bash
# Zkopírujte secrets
cp firmware/test-blink/secrets.yaml.example firmware/test-blink/secrets.yaml
# Upravte WiFi údaje v secrets.yaml

# Flashněte firmware
esphome run firmware/test-blink/main.yaml
```

### 4. Ověření

LED na ESP32 by měla **blikat každou sekundu**. ✅

**Kompletní návod:** [docs/SETUP.md](docs/SETUP.md)

---

## 📁 Struktura projektu

```
SuperESP/
├── tools/
│   └── flash-recovery/      # Flash recovery nástroje
├── firmware/
│   ├── test-blink/          # Test firmware (BLOK 1)
│   ├── master/              # Master ESP firmware (BLOK 2)
│   ├── scanner/             # Scanner ESP firmware (BLOK 3)
│   └── shared/              # Sdílené komponenty (BLOK 4)
├── web-ui/                  # JARVIS-style UI (BLOK 6-8)
├── homeassistant/           # HA konfigurace (BLOK 5,9)
├── cloud/                   # Cloud backend (BLOK 11)
└── docs/                    # Dokumentace
```

---

## 📖 Dokumentace

| Dokument | Popis |
|----------|-------|
| [SETUP.md](docs/SETUP.md) | Kompletní instalační návod |
| [HARDWARE.md](docs/HARDWARE.md) | Hardware specifikace a zapojení |
| [ROADMAP.md](docs/ROADMAP.md) | 12 bloků vývoje projektu |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Řešení častých problémů |

---

## 🗺️ Roadmap

### Fáze 1: Základ (BLOK 1-4)
- [x] **BLOK 1:** Repository setup + Flash recovery ✅
- [ ] **BLOK 2:** Master ESP firmware (DHT22, SD karta)
- [ ] **BLOK 3:** Scanner ESP firmware (WiFi scan)
- [ ] **BLOK 4:** UART komunikace mezi ESP

### Fáze 2: Integrace (BLOK 5-8)
- [ ] **BLOK 5:** Home Assistant integrace
- [ ] **BLOK 6:** Web UI základy
- [ ] **BLOK 7:** JARVIS design implementace
- [ ] **BLOK 8:** Real-time data vizualizace

### Fáze 3: Pokročilé (BLOK 9-12)
- [ ] **BLOK 9:** HA automatizace a notifikace
- [ ] **BLOK 10:** Handshake capture
- [ ] **BLOK 11:** Cloud sync a vzdálený přístup
- [ ] **BLOK 12:** Finalizace a dokumentace

**Detaily:** [docs/ROADMAP.md](docs/ROADMAP.md)

---

## 🎯 Use Cases

### 1. Bezpečnostní audit WiFi
- Skenování všech okolních sítí
- Detekce slabých zabezpečení
- Monitoring WiFi pokrytí

### 2. IoT Environment Monitoring
- Měření teploty/vlhkosti
- Logging dat na SD kartu
- Vizualizace v Home Assistant

### 3. Vzdělávací nástroj
- Naučte se ESP32 programování
- Pochopte WiFi protokoly
- Experimentujte s embedded systémy

---

## ⚠️ Právní upozornění

**SuperESP je určen výhradně pro:**
- Testování VLASTNÍCH WiFi sítí
- Vzdělávací účely
- Bezpečnostní audity s POVOLENÍM

**NEZÁKONNÉ použití:**
- ❌ Neoprávněný přístup k cizím sítím
- ❌ Zachytávání dat bez souhlasu
- ❌ Narušování komunikace

**Autor neručí za zneužití tohoto nástroje. Používejte zodpovědně!**

---

## 🤝 Přispívání

Projekt je v aktivním vývoji. Contributions jsou vítány!

1. Fork repository
2. Vytvořte feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit změny (`git commit -m 'Add some AmazingFeature'`)
4. Push do branch (`git push origin feature/AmazingFeature`)
5. Otevřete Pull Request

---

## 📄 License

Tento projekt je licencován pod MIT licencí - viz [LICENSE](LICENSE) soubor.

---

## 🙏 Poděkování

- **ESPHome** - za skvělý framework
- **Home Assistant** - za otevřenou platformu
- **ESP32 komunita** - za nekonečnou inspiraci
- **Marvel Studios** - za JARVIS inspiraci 🦾

---

## 📞 Kontakt & Podpora

- **Issues:** [GitHub Issues](https://github.com/skokycz/SuperESP/issues)
- **Dokumentace:** [docs/](docs/)
- **Troubleshooting:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

<p align="center">
  <b>Vytvořeno s ❤️ pro ESP32 a WiFi security community</b><br>
  <i>"Sometimes you gotta run before you can walk." - Tony Stark</i>
</p>