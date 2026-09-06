"""Object tables and nucleus-to-spheroid assignment."""

from __future__ import annotations

import numpy as np
import pandas as pd

from nuclear_imaging_core.measurements import region_feature_table


def _coordinate_columns(ndim: int) -> list[str]:
    if ndim == 2:
        return ["ceny", "cenx"]
    if ndim == 3:
        return ["cenz", "ceny", "cenx"]
    raise ValueError(f"Expected 2D or 3D labels, got ndim={ndim}")


def _object_table(image: np.ndarray, labels: np.ndarray) -> pd.DataFrame:
    table = region_feature_table(image, labels)
    rename = {"label": "label-id", "area": "size", "intensity_mean": "intensity-mean"}
    coordinate_names = _coordinate_columns(labels.ndim)
    rename.update({f"centroid-{index}": name for index, name in enumerate(coordinate_names)})
    return table.rename(columns=rename)


def assign_nuclei_to_spheroids(
    nuclei: pd.DataFrame,
    spheroid_labels: np.ndarray,
) -> pd.DataFrame:
    """Assign each nuclear centroid to a labelled spheroid."""
    labels = np.asarray(spheroid_labels)
    coordinate_names = _coordinate_columns(labels.ndim)
    result = nuclei.copy()
    memberships = []
    for row in result.itertuples(index=False):
        coordinates = tuple(
            int(round(float(getattr(row, name.replace("-", "_")))))
            for name in coordinate_names
        )
        inside = all(0 <= coordinate < size for coordinate, size in zip(coordinates, labels.shape))
        memberships.append(int(labels[coordinates]) if inside else 0)
    result["of-spheroid"] = memberships
    result["in-spheroid"] = (result["of-spheroid"] > 0).astype(int)
    return result


def measure_spheroid_system(
    nuclear_image: np.ndarray,
    nuclear_labels: np.ndarray,
    spheroid_labels: np.ndarray,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return nuclear and spheroid tables with pixel-based geometry."""
    image = np.asarray(nuclear_image)
    nuclei_labels = np.asarray(nuclear_labels)
    spheroids_labels = np.asarray(spheroid_labels)
    if image.shape != nuclei_labels.shape or image.shape != spheroids_labels.shape:
        raise ValueError("image, nuclear_labels and spheroid_labels must have the same shape")
    nuclei = assign_nuclei_to_spheroids(_object_table(image, nuclei_labels), spheroids_labels)
    spheroids = _object_table(image, spheroids_labels)
    counts = nuclei.loc[nuclei["in-spheroid"] == 1].groupby("of-spheroid").size()
    spheroids["nuclei-count"] = spheroids["label-id"].map(counts).fillna(0).astype(int)
    return nuclei, spheroids


__all__ = ["assign_nuclei_to_spheroids", "measure_spheroid_system"]
