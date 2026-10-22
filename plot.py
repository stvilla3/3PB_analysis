"""Plot the mean force-displacement curve over the final cycles of a test."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Configuration
CSV_PATH = Path("CPro M10 (L) 3PB 7.5d50N75v2000c4w.7a2.Loop 1.tracking.csv")
WINDOW = 100
GRID_POINTS = 1000
CURVE_COLOR = "#000000"
FIGURE_SIZE = (7.0, 4.5)
OUTPUT_PATH = None  # Set to a path such as "mean_curve.png" to save the figure.


REQUIRED_COLUMNS = ("Total Cycles", "Digital Position (mm)", "Force (N)")


def load_data(csv_path: Path) -> pd.DataFrame:
    """Load the CSV and verify the columns and numeric data required here."""
    data = pd.read_csv(csv_path)
    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        raise ValueError(f"Missing required CSV column(s): {', '.join(missing)}")

    data = data.loc[:, REQUIRED_COLUMNS].apply(pd.to_numeric, errors="coerce").dropna()
    if data.empty:
        raise ValueError("The CSV contains no valid numeric data in the required columns.")
    return data


def select_cycles(data: pd.DataFrame) -> pd.DataFrame:
    """Select rows belonging to the final configurable number of cycles."""
    maximum_cycle = data["Total Cycles"].max()
    lower_bound = maximum_cycle - WINDOW
    boundary_rows = np.flatnonzero(
        data["Total Cycles"].to_numpy() == lower_bound
    )
    if boundary_rows.size == 0:
        raise ValueError(
            f"Could not find cycle {lower_bound:g}, which is needed to locate "
            "the start of the final cycle window."
        )

    start_index = boundary_rows[-1] + 1
    selected = data.iloc[start_index:].copy()
    if selected.empty or selected["Total Cycles"].max() != maximum_cycle:
        raise ValueError("The final cycle window is empty or incomplete.")
    return selected


# def mean_curve(data: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
#     """Interpolate each cycle onto a shared position grid and average the forces."""
#     cycle_curves: list[tuple[np.ndarray, np.ndarray]] = []
#     for _, cycle in data.groupby("Total Cycles", sort=True):
#         position = cycle["Digital Position (mm)"].abs().to_numpy()
#         force = cycle["Force (N)"].abs().to_numpy()
#         order = np.argsort(position)
#         position, force = position[order], force[order]
#
#         # np.interp requires strictly increasing x values.
#         unique_position, inverse = np.unique(position, return_inverse=True)
#         mean_force = np.bincount(inverse, weights=force) / np.bincount(inverse)
#         if len(unique_position) < 2:
#             raise ValueError(f"Cycle {cycle['Total Cycles'].iloc[0]:g} is incomplete.")
#         cycle_curves.append((unique_position, mean_force))
#
#     grid_start = max(position[0] for position, _ in cycle_curves)
#     grid_stop = min(position[-1] for position, _ in cycle_curves)
#     if grid_start >= grid_stop:
#         raise ValueError("Selected cycles have no common Digital Position range.")
#
#     position_grid = np.linspace(grid_start, grid_stop, GRID_POINTS)
#     interpolated_force = np.vstack(
#         [np.interp(position_grid, position, force) for position, force in cycle_curves]
#     )
#     return position_grid, interpolated_force.mean(axis=0)


def plot_curve(position: np.ndarray, force: np.ndarray) -> None:
    """Create the publication-style force-displacement plot."""
    figure, axis = plt.subplots(figsize=FIGURE_SIZE)
    figure.patch.set_facecolor("white")
    axis.set_facecolor("white")
    axis.plot(position, force, color=CURVE_COLOR, linewidth=2.0)
    axis.set_xlabel("Absolute Digital Position (mm)")
    axis.set_ylabel("Absolute Force (N)")
    axis.set_xlim(-0.5, position.max()+0.5)
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
    data = load_data(CSV_PATH)
    selected = select_cycles(data)
    position = selected["Digital Position (mm)"].abs().to_numpy()
    force = selected["Force (N)"].abs().to_numpy()
    plot_curve(position, force)
    print(len(position))
    print(len(force))


if __name__ == "__main__":
    main()
