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

The resulting tables retain label identities, pixel coordinates, object sizes
and spheroid membership. Radial analysis accepts explicit pixel distances and
bin counts so the geometry can be tuned for each acquisition.
