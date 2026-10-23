import numpy as np
import pandas as pd
from pathlib import Path


CSV_PATH = Path("CPro M10 (L) 3PB 7.5d50N75v2000c4w.7a2.Loop 1.tracking.csv")
Window = 100
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
    lower_bound = maximum_cycle - Window
    boundary_rows = np.flatnonzero(
        data["Total Cycles"].to_numpy() == lower_bound
    )
    if boundary_rows.size == 0:
        raise ValueError(
            f"Could not find cycle {lower_bound:g}, which is needed to locate "
            "the start of the final cycle Window."
        )

    start_index = boundary_rows[-1] + 1
    selected = data.iloc[start_index:].copy()
    if selected.empty or selected["Total Cycles"].max() != maximum_cycle:
        raise ValueError("The final cycle Window is empty or incomplete.")
    return selected

def input() -> None:
    data = load_data(CSV_PATH)
    selected = select_cycles(data)
    position = selected["Digital Position (mm)"].abs().to_numpy()
    force = selected["Force (N)"].abs().to_numpy()
    return position, force

position, force = input()

print(position)
print(force)

print(f"{np.max(position):.2f}")
print(f"{np.max(force):.1f}")
max_force = np.max(force)