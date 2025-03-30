import argparse

# python main.py - domyślnie uruchamia GUI
# python main.py --mode testy - uruchamia testy porównawcze
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["gui", "testy"], default="gui")
    args = parser.parse_args()

    if args.mode == "gui":
        from gui.app import run_gui  
        run_gui()
    elif args.mode == "testy":
        from tests.test_comparison import compare_configurations 
        compare_configurations()