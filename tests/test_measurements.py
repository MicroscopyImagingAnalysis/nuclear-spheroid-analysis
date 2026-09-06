import numpy as np

from nuclear_spheroid_analysis import measure_spheroid_system


def test_measure_spheroid_system_preserves_membership_and_counts():
    image = np.ones((12, 12), dtype=np.float32)
    spheroids = np.zeros_like(image, dtype=np.uint16)
    spheroids[1:11, 1:11] = 1
    nuclei = np.zeros_like(spheroids)
    nuclei[2:4, 2:4] = 1
    nuclei[7:9, 7:9] = 2
    nuclear_table, spheroid_table = measure_spheroid_system(image, nuclei, spheroids)
    assert nuclear_table["of-spheroid"].tolist() == [1, 1]
    assert nuclear_table["in-spheroid"].tolist() == [1, 1]
    assert spheroid_table["nuclei-count"].tolist() == [2]
