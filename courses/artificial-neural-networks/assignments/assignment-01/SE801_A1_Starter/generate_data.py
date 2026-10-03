"""Generate the fixed synthetic data only; contains no model or solution."""
import csv
import random
from pathlib import Path

SEED = 801
CLASS_NAMES = {0: 'normal', 1: 'offset', 2: 'unstable'}


def generate(output_dir=None):
    output_dir = Path(output_dir) if output_dir else Path(__file__).parent / 'data'
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    for split, counts in [('train', (600, 200, 100)),
                          ('validation', (180, 60, 30)),
                          ('test', (180, 60, 30))]:
        rows = []
        # Correlated Gaussian measurements; classes overlap intentionally.
        for label, count in enumerate(counts):
            mean = [(0.0, 0.0), (1.6, 0.8), (-0.6, 1.7)][label]
            scale = [1.0, 1.0, 1.4][label]
            for index in range(count):
                z1, z2 = rng.gauss(0, 1), rng.gauss(0, 1)
                x1 = mean[0] + scale * z1
                x2 = mean[1] + scale * (0.35 * z1 + (1 - 0.35**2)**0.5 * z2)
                rows.append([f'{split}_{label}_{index:04d}', x1, x2, label])
        rng.shuffle(rows)
        with (output_dir / f'{split}.csv').open('w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['sample_id', 'reading_1', 'reading_2', 'label'])
            writer.writerows(rows)


if __name__ == '__main__':
    generate()
