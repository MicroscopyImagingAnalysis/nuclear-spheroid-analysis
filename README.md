# nuclear-spheroid-analysis

Two- and three-dimensional workflows for measuring nuclei in multicellular
spheroids. The package connects object measurements with nucleus-to-spheroid
assignment and inward/outward radial summaries.

## Install

```bash
python -m pip install .
```

## Example

```python
from nuclear_spheroid_analysis import measure_spheroid_system

nuclei, spheroids = measure_spheroid_system(
    nuclear_image,
    nuclear_labels,
    spheroid_labels,
)
```

Add inward and outward radial bins using explicit pixel distances:

```python
from nuclear_spheroid_analysis import analyze_radial_2d

radial, nuclei, spheroids = analyze_radial_2d(
    nuclei,
    spheroids,
    nuclear_labels,
    spheroid_labels,
    {
        "nbins-sph": 20,
        "maxdist-sph-shell": 400,
        "maxdist-sph-outward": 400,
    },
    {},
)
```

Persist each identity-preserving output for downstream analysis:

```python
nuclei.to_csv("nuclear_features.csv", index=False)
spheroids.to_csv("spheroid_features.csv", index=False)
radial.to_csv("spheroid_radial_features.csv", index=False)
```

The resulting tables retain label identities, pixel coordinates, object sizes
and spheroid membership. Radial analysis accepts explicit pixel distances and
bin counts so the geometry can be tuned for each acquisition.
