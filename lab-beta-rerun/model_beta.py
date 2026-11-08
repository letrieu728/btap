"""The copy model with S-shaped copying (respond(rho, beta) in place of rho): the prior-strength sweep at the
record's |beta| (names, 1.68) and a GPT-6.1-Sol-like |beta| (3.9), 50 runs each.

    python model_beta.py   -> cache/model_beta.pkl

For a Windows-safe, separately named rerun:
    python model_beta.py --workers 1 --runs 2 --output model_beta_rerun.pkl
"""
import multiprocessing
import pickle
import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'src'))
import model as md  # noqa: E402
from common import load_cache  # noqa: E402

class SerialPool:
    """Small Pool-compatible adapter for deterministic, Windows-safe reruns."""

    @staticmethod
    def map(function, items):
        return list(map(function, items))


def main():
    parser = argparse.ArgumentParser(description='Run the S-shaped-copying beta sweep.')
    parser.add_argument('--runs', type=int, default=md.RUNS,
                        help=f'repetitions per beta (default: {md.RUNS})')
    parser.add_argument('--workers', type=int, default=60,
                        help='worker processes; use 1 for Windows-safe serial execution')
    parser.add_argument('--output', default='model_beta.pkl',
                        help='filename written under cache/')
    args = parser.parse_args()
    if args.runs < 1:
        parser.error('--runs must be at least 1')
    if args.workers < 1:
        parser.error('--workers must be at least 1')

    par = load_cache('model.pkl')['par']
    output = ROOT.parent / 'cache' / args.output
    if args.workers == 1:
        pool = SerialPool()
        out = {b: md.sweep(par, pool, runs=args.runs, beta=b) for b in (1.68, 3.9)}
    else:
        with multiprocessing.Pool(args.workers) as pool:
            out = {b: md.sweep(par, pool, runs=args.runs, beta=b) for b in (1.68, 3.9)}
    with open(output, 'wb') as handle:
        pickle.dump(out, handle)
    print(f'done: {output}')


if __name__ == '__main__':
    main()
