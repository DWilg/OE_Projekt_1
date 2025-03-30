import argparse
from gui.app import run_gui
from tests.test_comparison import compare_configurations

# python main.py - domyślnie uruchamia GUI
# python main.py --mode testy - uruchamia testy porównawcze


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wybierz tryb uruchomienia aplikacji.")
    parser.add_argument("--mode", choices=["gui", "testy"], default="gui", help="Wybierz tryb: 'gui' lub 'testy'")
    args = parser.parse_args()

    if args.mode == "gui":
        run_gui()
    elif args.mode == "testy":
        results = compare_configurations()
        print("Testy zakończone. Wyniki zapisane.")
