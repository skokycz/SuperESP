# SuperESP Development Roadmap

12 bloků vývoje od základů po plně funkční WiFi toolkit ve stylu JARVIS.

---

## 📊 Přehled fází

```
Fáze 1: ZÁKLAD ━━━━━━━━━━━━━━━━━━━━━━━━━━ BLOK 1-4 (měsíc 1-2)
Fáze 2: INTEGRACE ━━━━━━━━━━━━━━━━━━━━━━━ BLOK 5-8 (měsíc 2-3)
Fáze 3: POKROČILÉ ━━━━━━━━━━━━━━━━━━━━━━━ BLOK 9-12 (měsíc 3-4)
```

---

## ✅ BLOK 1: Repository Setup + Flash Recovery

**Status:** ✅ **DOKONČENO**

**Cíl:** Vytvořit základní strukturu repozitáře a nástroje pro recovery ESP32-C3.

### Deliverables
- [x] Struktura repozitáře (tools, firmware, docs)
- [x] Flash recovery Python script (`recover.py`)
- [x] Test blink firmware (ESPHome)
- [x] Kompletní dokumentace (README, SETUP, HARDWARE, TROUBLESHOOTING)
- [x] MIT License
- [x] .gitignore

### Technologie
- Python 3.8+ (esptool, pyserial)
- ESPHome (test firmware)
- Git/GitHub

### Výstupy
- ✅ Repository na GitHubu
- ✅ Funkční flash recovery
- ✅ Test firmware který bliká LED

---

## 🔨 BLOK 2: Master ESP Firmware

**Status:** 🔨 **V PROCESU**

**Cíl:** Vytvořit firmware pro Master ESP s DHT22 a SD kartou.

### Deliverables
- [x] ESPHome konfigurace pro Master ESP
- [x] DHT22 integrace (teplota, vlhkost)
- [x] Webové rozhraní pro monitoring
- [x] OTA aktualizace
- [x] WiFi workaroundy pro Auth Expired problém
- [x] Kompletní dokumentace v češtině
- [ ] SD karta logging (SPI) - připraveno pro BLOK 2.5
- [ ] CSV formát pro data - připraveno pro BLOK 2.5

### Hardware požadavky
- ESP32-C3 Super Mini
- DHT22 sensor (GPIO2)
- SD Card Reader (SPI GPIO 4-7 nebo alternativní)
- microSD karta

### Funkce
- **Měření:** Teplota a vlhkost každých 60s
- **Logging:** Zápis dat na SD kartu (timestamp, temp, humidity)
- **Web UI:** Zobrazení aktuálních hodnot
- **Home Assistant:** Export sensorů

### Acceptance Criteria
- [x] DHT22 měří teplotu/vlhkost
- [x] Web interface zobrazuje hodnoty
- [x] HA integrace funguje
- [x] WiFi workaroundy implementovány
- [ ] Data se zapisují na SD kartu - připraveno pro BLOK 2.5

---

## 📡 BLOK 3: Scanner ESP Firmware

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Firmware pro Scanner ESP - skenování WiFi sítí.

### Deliverables
- [ ] WiFi scan komponenta (ESPHome custom)
- [ ] Detekce SSID, BSSID, RSSI, channel, encryption
- [ ] Buffering scan výsledků
- [ ] UART komunikace - reporting do Master
- [ ] LED indikace scan aktivity

### Funkce
- **Scan interval:** 10-30 sekund (konfigurovatelné)
- **2.4GHz only:** ESP32-C3 limit
- **Data format:** JSON přes UART
- **Deduplication:** Odstranění duplicit v bufferu

### Výstup dat (JSON)
```json
{
  "ssid": "MyNetwork",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "rssi": -45,
  "channel": 6,
  "encryption": "WPA2-PSK"
}
```

### Acceptance Criteria
- [ ] Scanner detekuje okolní WiFi sítě
- [ ] Data se odesílají přes UART
- [ ] LED bliká při skenování

---

## 🔗 BLOK 4: UART Komunikace

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Propojit všechny 3 ESP32 pomocí UART.

### Deliverables
- [ ] UART custom component pro ESPHome
- [ ] Protokol komunikace (framing, checksums)
- [ ] Master ← Scanner 1 ← Scanner 2 chain
- [ ] Data agregace na Master ESP
- [ ] Error handling a retry

### Topologie
```
Master (GPIO20/21) ↔ Scanner1 (GPIO20/21)
                     Scanner1 (GPIO2/3) ↔ Scanner2 (GPIO20/21)
```

### Protokol
- **Baud rate:** 115200
- **Format:** JSON s newline delimiter
- **Checksum:** CRC8 na konci
- **Retry:** 3x při chybě

### Acceptance Criteria
- [ ] Scanner 1 odesílá data do Master
- [ ] Scanner 2 odesílá data do Scanner 1
- [ ] Master agreguje data ze všech scannerů
- [ ] Chybějící pakety se logují

---

## 🏠 BLOK 5: Home Assistant Integrace

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Plná integrace s Home Assistant.

### Deliverables
- [ ] ESPHome API integrace
- [ ] Sensory: teplota, vlhkost, WiFi scan count
- [ ] Binary sensory: scan active, SD card OK
- [ ] Switche: manuální scan trigger, mode select
- [ ] HA Dashboard konfigurace

### Home Assistant entity
- `sensor.superesp_temperature`
- `sensor.superesp_humidity`
- `sensor.superesp_networks_found`
- `sensor.superesp_uptime`
- `binary_sensor.superesp_scanning`
- `switch.superesp_trigger_scan`

### Dashboard
- Card s teplotou/vlhkostí
- Graf historie měření
- Seznam detekovaných sítí
- Scan trigger tlačítko

### Acceptance Criteria
- [ ] Všechny entity viditelné v HA
- [ ] Dashboard funkční
- [ ] Automatizace možné

---

## 🎨 BLOK 6: Web UI Základ

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Základní webové rozhraní (React + Vite).

### Deliverables
- [ ] React + Vite projekt setup
- [ ] Základní layout (header, sidebar, main)
- [ ] API komunikace s ESP32 (REST/WebSocket)
- [ ] Stránka: Dashboard
- [ ] Stránka: WiFi Networks
- [ ] Stránka: Settings

### Technologie
- React 18+
- Vite (build tool)
- TailwindCSS (styling)
- Axios/Fetch (API)

### Pages
1. **Dashboard** - přehled (teplota, počet sítí)
2. **Networks** - tabulka detekovaných WiFi
3. **Settings** - konfigurace scan interval, atd.

### Acceptance Criteria
- [ ] Web UI běží lokálně
- [ ] Komunikuje s ESP32 API
- [ ] Zobrazuje real-time data

---

## 🦾 BLOK 7: JARVIS Design

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Implementovat Iron Man JARVIS styl do UI.

### Deliverables
- [ ] Futuristický design (dark theme, modrá/cyan)
- [ ] Animace: loading, transitions
- [ ] Particle efekty na pozadí
- [ ] Audio efekty (volitelné)
- [ ] Typografie: futuristický font (Orbitron?)

### Barevná paleta
- **Background:** #0a0e27 (tmavě modrá)
- **Primary:** #00d9ff (cyan)
- **Secondary:** #0080ff (modrá)
- **Accent:** #ff0080 (magenta)
- **Text:** #e0e0e0 (světle šedá)

### Komponenty
- Glowing borders
- Hexagon shapes
- Radar-style scan visualization
- Pulsing animations
- HUD-style overlays

### Acceptance Criteria
- [ ] UI vypadá jako z Iron Man filmu
- [ ] Animace smooth a cool
- [ ] Responzivní na mobilech

---

## 📊 BLOK 8: Real-time Vizualizace

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Real-time grafy a vizualizace dat.

### Deliverables
- [ ] Chart.js / Recharts integrace
- [ ] Graf: Teplota a vlhkost (čas)
- [ ] WiFi heatmap (síla signálu)
- [ ] Radar zobrazení WiFi sítí (channel vs RSSI)
- [ ] Live update přes WebSocket

### Grafy
1. **Line chart:** Teplota/vlhkost v čase (24h)
2. **Bar chart:** Počet sítí na channel
3. **Scatter plot:** RSSI vs Channel
4. **Heatmap:** Pokrytí WiFi v místnosti (budoucí)

### WebSocket API
```
ws://esp-ip:80/ws
→ {"temp": 22.5, "humidity": 45, "networks": [...]}
```

### Acceptance Criteria
- [ ] Grafy se aktualizují real-time
- [ ] Data historická zobrazena správně
- [ ] WebSocket stabilní

---

## 🤖 BLOK 9: HA Automatizace

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Pokročilé automatizace v Home Assistant.

### Deliverables
- [ ] Automatizace: alert při nové WiFi síti
- [ ] Automatizace: denní report skenů
- [ ] Notifikace do mobilu (HA app)
- [ ] Dashbord pro monitoring
- [ ] Blueprint pro vlastní automatizace

### Příklady automatizací
1. **Nová síť detekována:**
   - Trigger: Nová SSID
   - Action: Notifikace + log

2. **Vysoká teplota:**
   - Trigger: Teplota > 30°C
   - Action: Alert

3. **Denní summary:**
   - Trigger: 9:00 každý den
   - Action: Report počtu sítí, avg teplota

### Acceptance Criteria
- [ ] Automatizace funkční
- [ ] Notifikace chodí správně
- [ ] Blueprint dokumentován

---

## 🔐 BLOK 10: Handshake Capture

**Status:** 📋 **PLÁNOVÁNO** (Pokročilé)

**Cíl:** Zachytávání WPA/WPA2 handshake.

⚠️ **LEGÁLNÍ POUŽITÍ POUZE NA VLASTNÍCH SÍTÍCH!**

### Deliverables
- [ ] ESP32 monitor mode custom firmware
- [ ] Packet sniffing (promiscuous mode)
- [ ] Handshake detection (EAPOL)
- [ ] Uložení na SD kartu (.pcap)
- [ ] Web UI pro download captures

### Technické výzvy
- ESP32 omezený monitor mode support
- Packet parsing v real-time
- Storage na SD kartě (4-way handshake ~1KB)

### Legal disclaimer
```
⚠️ Tento nástroj je určen POUZE pro:
- Testování VLASTNÍCH WiFi sítí
- Bezpečnostní audity s POVOLENÍM
- Vzdělávací účely

Neoprávněné použití je NEZÁKONNÉ!
```

### Acceptance Criteria
- [ ] Handshake capture funguje
- [ ] .pcap soubory jsou validní
- [ ] Legal warning viditelný

---

## ☁️ BLOK 11: Cloud Sync

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Synchronizace dat do cloudu pro vzdálený přístup.

### Deliverables
- [ ] Backend API (Node.js/Python FastAPI)
- [ ] Database (PostgreSQL nebo MongoDB)
- [ ] ESP32 → Cloud push (HTTPS)
- [ ] Web UI ← Cloud pull
- [ ] User authentication
- [ ] Multi-device support

### Architektura
```
ESP32 → HTTPS POST → Backend API → Database
                          ↓
                     Web UI (remote access)
```

### Cloud options
1. **Self-hosted:** VPS (DigitalOcean, Hetzner)
2. **Serverless:** AWS Lambda + DynamoDB
3. **Firebase:** Realtime DB + Auth

### Features
- Historie všech scanů (long-term)
- Vzdálený přístup odkudkoliv
- Multi-user support
- API pro 3rd party integrace

### Acceptance Criteria
- [ ] Data se ukládají do cloudu
- [ ] Web UI přístupné vzdáleně
- [ ] Autentizace funguje

---

## 📦 BLOK 12: Finalizace & Dokumentace

**Status:** 📋 **PLÁNOVÁNO**

**Cíl:** Dokončení projektu, dokumentace, video.

### Deliverables
- [ ] Video tutorial (YouTube)
- [ ] Kompletní dokumentace (GitBook?)
- [ ] User manual (PDF)
- [ ] Troubleshooting guide (rozšířený)
- [ ] Contributing guide
- [ ] Changelog
- [ ] Release v1.0.0

### Video obsah
1. Úvod do projektu (3 min)
2. Hardware sestavení (5 min)
3. Software setup (5 min)
4. Demo všech funkcí (10 min)
5. Tips & tricks (3 min)

### Dokumentace
- Installation guide (step-by-step)
- API reference
- Configuration options
- FAQ
- Gallery (screenshots, hardware photos)

### Release checklist
- [ ] Veškerý kód otestován
- [ ] Dokumentace kompletní
- [ ] Video nahráno
- [ ] GitHub Release s binárkami
- [ ] Reddit/Hacker News post

### Acceptance Criteria
- [ ] Projekt lze zprovoznit podle dokumentace
- [ ] Video tutorial dostupné
- [ ] Release v1.0.0 na GitHubu

---

## 📅 Časový odhad

| Fáze | Bloky | Trvání | Celkem |
|------|-------|--------|--------|
| **Základ** | 1-4 | 2-3 týdny/blok | 2 měsíce |
| **Integrace** | 5-8 | 1-2 týdny/blok | 1.5 měsíce |
| **Pokročilé** | 9-12 | 1-2 týdny/blok | 1.5 měsíce |
| **CELKEM** | 1-12 | | **~4-5 měsíců** |

💡 Časový odhad závisí na:
- Dostupnosti času
- Technických problémech
- Hardware dostupnosti

---

## 🎯 Milestones

### MVP (Minimum Viable Product) - Konec Fáze 1
- ✅ BLOK 1: Flash recovery
- ✅ BLOK 2: Master firmware
- [ ] BLOK 3: Scanner firmware
- [ ] BLOK 4: UART komunikace
- **Výsledek:** Fungující cluster 3x ESP32 skenující WiFi

### Beta - Konec Fáze 2
- [ ] BLOK 5: Home Assistant
- [ ] BLOK 6-7: JARVIS UI
- [ ] BLOK 8: Real-time grafy
- **Výsledek:** Plně funkční lokální systém s cool UI

### Production - Konec Fáze 3
- [ ] BLOK 9: HA automatizace
- [ ] BLOK 10: Handshake capture (optional)
- [ ] BLOK 11: Cloud sync
- [ ] BLOK 12: Dokumentace
- **Výsledek:** Hotový produkt s dokumentací

---

## 🔄 Iterativní vývoj

Každý blok následuje tento workflow:

1. **Plánování** (1 den)
   - Specifikace požadavků
   - Technický design

2. **Implementace** (3-7 dní)
   - Coding
   - Testing
   - Bug fixing

3. **Dokumentace** (1 den)
   - README update
   - Code comments
   - User guide

4. **Review** (1 den)
   - Code review
   - Testing na hardware
   - Acceptance criteria check

**Total per block:** 6-10 dní

---

## 📈 Progress Tracking

Current progress:
```
[████████████████░░░░░░░░░░░░░░░░] 16% (BLOK 2/12)
```

Next up:
- [ ] BLOK 3: Scanner ESP Firmware

---

## 🤝 Přispívání

Pokud chcete přispět:
1. Vyberte si blok z roadmapy
2. Vytvořte issue s návrhem
3. Fork → Branch → PR
4. Follow roadmap design

---

**Roadmap je živý dokument a může se měnit podle potřeb!**

*Last updated: BLOK 2 dokončen ✅*
