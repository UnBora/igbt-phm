"""Load steady-state observations from the NASA IGBT aging experiment."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.io import loadmat


SIGNAL_COLUMNS = (
    "supply_voltage",
    "node1_voltage",
    "node2_voltage",
    "collector_emitter_current",
    "package_temperature",
)


def _device_id(path: Path) -> str | None:
    stem = re.sub(r"\s+\d+$", "", path.stem).strip()
    match = re.fullmatch(r"Device\s*(\d+)(?:b)?", stem, flags=re.IGNORECASE)
    return f"device_{match.group(1)}" if match else None


def _aging_data_directory(raw_root: Path) -> Path:
    if raw_root.name == "Aging Data" and raw_root.is_dir():
        return raw_root

    candidates = list(raw_root.rglob("Aging Data"))
    if len(candidates) != 1:
        raise FileNotFoundError(
            f"Expected one 'Aging Data' directory under {raw_root}, "
            f"found {len(candidates)}."
        )
    return candidates[0]


def load_aging_observations(raw_root: Path) -> pd.DataFrame:
    """Load per-record steady-state signals for Devices 2–5.

    Main and ``b`` MAT files are treated as segments of the same device run.
    Short ``check`` files and other experiment types are intentionally excluded.
    Signal values retain the units and conventions stored in the MAT files.
    """
    aging_dir = _aging_data_directory(Path(raw_root))
    mat_files = sorted(aging_dir.rglob("*.mat"))
    selected = [(path, _device_id(path)) for path in mat_files]
    selected = [(path, device) for path, device in selected if device is not None]
    if not selected:
        raise FileNotFoundError(f"No DeviceN or DeviceNb MAT files found under {aging_dir}.")

    rows: list[dict[str, float | str]] = []
    for path, device_id in selected:
        try:
            contents = loadmat(path, squeeze_me=True, struct_as_record=False)
            if "measurement" not in contents:
                raise ValueError("MAT file has no 'measurement' variable.")
            measurement = contents["measurement"]
            if not hasattr(measurement, "steadyState"):
                raise ValueError("Measurement has no 'steadyState' records.")

            records = np.atleast_1d(measurement.steadyState)
            for record in records:
                timestamp = float(np.asarray(record.timeEpoch).item())
                if not np.isfinite(timestamp) or timestamp <= 0:
                    continue

                signals = {
                    "supply_voltage": float(np.asarray(record.timeDomain.supplyVoltage).item()),
                    "node1_voltage": float(np.asarray(record.timeDomain.node1Voltage).item()),
                    "node2_voltage": float(np.asarray(record.timeDomain.node2Voltage).item()),
                    "collector_emitter_current": float(
                        np.asarray(record.timeDomain.collectorEmitterCurrent).item()
                    ),
                    "package_temperature": float(
                        np.asarray(record.timeDomain.packageTemperature).item()
                    ),
                }
                rows.append(
                    {
                        "device_id": device_id,
                        "timestamp_s": timestamp,
                        **signals,
                        "source_file": path.name,
                    }
                )
        except Exception as exc:
            raise RuntimeError(f"Could not load aging observations from {path}: {exc}") from exc

    observations = pd.DataFrame(rows)
    if observations.empty:
        raise ValueError(f"No timestamped steady-state records found under {aging_dir}.")

    observations = observations.replace([np.inf, -np.inf], np.nan)
    observations = observations.dropna(subset=["timestamp_s", *SIGNAL_COLUMNS])
    observations = observations.sort_values(["device_id", "timestamp_s"]).reset_index(drop=True)
    if observations.empty:
        raise ValueError("All steady-state records had missing or non-finite required signals.")
    return observations
