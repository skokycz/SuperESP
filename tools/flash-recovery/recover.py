#!/usr/bin/env python3
"""
SuperESP Flash Recovery Tool
Obnoví ESP32-C3 po flashnutí ESP-IDF firmware
"""

import argparse
import subprocess
import sys
import time
import platform

def check_esptool():
    """Zkontroluje jestli je esptool nainstalován"""
    try:
        result = subprocess.run(['esptool.py', 'version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print(f"✓ esptool nalezen: {result.stdout.strip()}")
            return True
        else:
            print("✗ esptool není dostupný")
            return False
    except FileNotFoundError:
        print("✗ esptool není nainstalován")
        print("  Nainstalujte pomocí: pip install -r requirements.txt")
        return False

def detect_port():
    """Automatická detekce COM portu"""
    try:
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())
        
        if not ports:
            print("✗ Žádné COM porty nebyly nalezeny")
            return None
        
        # Hledání ESP32 zařízení
        esp_ports = []
        for port in ports:
            if 'USB' in port.description or 'Serial' in port.description or 'CH340' in port.description or 'CP210' in port.description:
                esp_ports.append(port.device)
        
        if esp_ports:
            detected_port = esp_ports[0]
            print(f"✓ Detekován port: {detected_port}")
            if len(esp_ports) > 1:
                print(f"  Další dostupné porty: {', '.join(esp_ports[1:])}")
            return detected_port
        
        # Pokud ESP32 nenalezen, vrátí první dostupný
        detected_port = ports[0].device
        print(f"⚠ ESP32 nebyl automaticky detekován, použit port: {detected_port}")
        print(f"  Dostupné porty: {', '.join([p.device for p in ports])}")
        return detected_port
        
    except ImportError:
        print("⚠ pyserial není nainstalován, nelze auto-detekovat port")
        # Default porty podle OS
        if platform.system() == 'Windows':
            return 'COM3'
        elif platform.system() == 'Darwin':  # macOS
            return '/dev/cu.usbserial-0001'
        else:  # Linux
            return '/dev/ttyUSB0'

def erase_flash(port, chip="esp32c3", baud=460800):
    """Kompletní vymazání flash paměti"""
    print(f"\n🔥 Mazání flash paměti na {port}...")
    print("   Toto může trvat několik sekund...")
    
    cmd = [
        'esptool.py',
        '--chip', chip,
        '--port', port,
        '--baud', str(baud),
        'erase_flash'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Flash paměť úspěšně vymazána!")
            return True
        else:
            print(f"✗ Chyba při mazání flash:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Chyba: {e}")
        return False

def verify_chip(port, chip="esp32c3", baud=460800):
    """Ověří připojení k ESP32 chipu"""
    print(f"\n🔍 Ověřování připojení k {chip}...")
    
    cmd = [
        'esptool.py',
        '--chip', chip,
        '--port', port,
        '--baud', str(baud),
        'chip_id'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Chip úspěšně detekován!")
            # Výpis základních informací
            for line in result.stdout.split('\n'):
                if 'Chip is' in line or 'MAC' in line or 'Crystal is' in line:
                    print(f"  {line.strip()}")
            return True
        else:
            print(f"✗ Nelze se připojit k chipu:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Chyba: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='SuperESP Flash Recovery - Obnova ESP32-C3 po ESP-IDF',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Příklady použití:
  %(prog)s                          # Auto-detekce portu a smazání flash
  %(prog)s --port COM3              # Windows s konkrétním portem
  %(prog)s --port /dev/ttyUSB0      # Linux s konkrétním portem
  %(prog)s --verify-only            # Pouze ověření připojení
  %(prog)s --chip esp32c3 --baud 115200  # Vlastní nastavení

Po smazání flash můžete flashnout ESPHome pomocí:
  esphome run firmware/test-blink/main.yaml
        """
    )
    
    parser.add_argument('--port', '-p', 
                       help='COM port (auto-detect pokud není zadán)')
    parser.add_argument('--chip', '-c', 
                       default='esp32c3', 
                       help='Typ chipu (výchozí: esp32c3)')
    parser.add_argument('--baud', '-b', 
                       type=int, 
                       default=460800, 
                       help='Baud rate (výchozí: 460800)')
    parser.add_argument('--verify-only', 
                       action='store_true',
                       help='Pouze ověří připojení bez mazání')
    parser.add_argument('--skip-verify',
                       action='store_true',
                       help='Přeskočí ověření a rovnou maže')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SuperESP Flash Recovery Tool")
    print("=" * 60)
    
    # Kontrola esptool
    if not check_esptool():
        sys.exit(1)
    
    # Detekce portu
    port = args.port if args.port else detect_port()
    if not port:
        print("\n✗ Nelze určit COM port")
        print("  Použijte: --port COM3 (nebo odpovídající port)")
        sys.exit(1)
    
    print(f"\nPoužité nastavení:")
    print(f"  Port: {port}")
    print(f"  Chip: {args.chip}")
    print(f"  Baud: {args.baud}")
    
    # Ověření připojení
    if not args.skip_verify:
        if not verify_chip(port, args.chip, args.baud):
            print("\n⚠ Tipy pro řešení problémů:")
            print("  1. Zkontrolujte USB kabel")
            print("  2. Stiskněte a podržte tlačítko BOOT při připojení")
            print("  3. Zkuste jiný USB port")
            print("  4. Zkuste nižší baud rate: --baud 115200")
            sys.exit(1)
    
    # Pokud jen ověření, ukončíme
    if args.verify_only:
        print("\n✓ Ověření dokončeno, flash nebyla mazána")
        sys.exit(0)
    
    # Mazání flash
    print("\n" + "!" * 60)
    print("VAROVÁNÍ: Tato operace SMAŽE veškerý obsah flash paměti!")
    print("!" * 60)
    
    try:
        response = input("\nPokračovat? (ano/ne): ").strip().lower()
        if response not in ['ano', 'a', 'yes', 'y']:
            print("Operace zrušena uživatelem")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nOperace zrušena uživatelem")
        sys.exit(0)
    
    if erase_flash(port, args.chip, args.baud):
        print("\n" + "=" * 60)
        print("✓ ÚSPĚCH! ESP32 je připraven pro nový firmware")
        print("=" * 60)
        print("\nDalší kroky:")
        print("1. Odpojte a znovu připojte ESP32")
        print("2. Flashněte ESPHome firmware:")
        print("   esphome run firmware/test-blink/main.yaml")
        print("\nPokud máte problémy, viz docs/TROUBLESHOOTING.md")
        sys.exit(0)
    else:
        print("\n✗ Smazání flash selhalo")
        sys.exit(1)

if __name__ == '__main__':
    main()
