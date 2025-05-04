import argparse

from sim_file import run_sim

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="FPS testing mode")
    args = parser.parse_args()

    run_sim(testing=args.test)

