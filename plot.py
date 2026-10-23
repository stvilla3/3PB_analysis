"""Plot the mean force-displacement curve over the final cycles of a test."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Configuration
CSV_PATH = Path("CPro M10 (L) 3PB 7.5d50N75v2000c4w.7a2.Loop 1.tracking.csv")
cycle = 1000
GRID_POINTS = 1000
CURVE_COLOR = "#000000"
FIGURE_SIZE = (7.0, 4.5)
OUTPUT_PATH = None  # Set to a path such as "mean_curve.png" to save the figure.


REQUIRED_COLUMNS = ("Total Cycles", "Digital Position (mm)", "Force (N)")


def load_data(csv_path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load the data from the CSV file."""
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)

        headers = [h.strip() for h in reader.fieldnames]
        cycle_column = headers[2]
        force_column = headers[8]
        position_column = headers[9]


        cycle = []
        force = []
        position = []

        for row in reader:
            if row[cycle_column] == str(cycle):
                if row[cycle_column] != '':
                    cycle.append(float(row[cycle_column]))
                if row[force_column] != '':
                    force.append(float(row[force_column]))
                if row[position_column] != '':
                    position.append(float(row[position_column]))

        cycle = np.array(cycle)
        force = np.array(force)
        position = np.array(position)

    return cycle, force, position

def plot_curve(position: np.ndarray, force: np.ndarray) -> None:
    """Create the publication-style force-displacement plot."""
    figure, axis = plt.subplots(figsize=FIGURE_SIZE)
    figure.patch.set_facecolor("white")
    axis.set_facecolor("white")
    axis.plot(position, force, color=CURVE_COLOR, linewidth=2.0)
    axis.set_xlabel("Absolute Digital Position (mm)")
    axis.set_ylabel("Absolute Force (N)")
    # axis.set_xlim(-0.5, position.max()+0.5)
    axis.set_ylim(bottom=0)
    axis.grid(True, color="#D9D9D9", linewidth=0.2, alpha=1.0)
    axis.set_axisbelow(True)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    figure.tight_layout()

    if OUTPUT_PATH is not None:
        figure.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.show()


def main() -> None:
    cycle, force, position = load_data(CSV_PATH)
    plot_curve(position, force)
    print(len(position))
    print(len(force))


if __name__ == "__main__":
    main()
