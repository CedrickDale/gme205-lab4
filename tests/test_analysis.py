from shapely.geometry import box

from src.spatial import Parcel, SpatialObject
from src.analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


def make_parcel(
    parcel_id,
    zone,
    is_active,
    area_sqm,
    geometry=None,
):
    if geometry is None:
        geometry = box(0, 0, 1, 1)

    return Parcel(
        parcel_id,
        geometry,
        {
            "zone": zone,
            "is_active": is_active,
            "area_sqm": area_sqm,
        },
    )


def test_total_active_area_excludes_inactive():
    parcels = [
        make_parcel(1, "Residential", True, 5000),
        make_parcel(2, "Commercial", False, 7000),
        make_parcel(3, "Industrial", True, 3000),
    ]

    result = total_active_area(parcels)

    assert result == 8000


def test_parcels_above_threshold_includes_exact_threshold():
    parcels = [
        make_parcel(1, "Residential", True, 5000),
        make_parcel(2, "Commercial", True, 4999),
        make_parcel(3, "Industrial", True, 7000),
    ]

    result = parcels_above_threshold(
        parcels,
        threshold=5000,
    )

    result_ids = [
        parcel.parcel_id
        for parcel in result
    ]

    assert result_ids == [1, 3]


def test_count_by_zone():
    parcels = [
        make_parcel(1, "Residential", True, 5000),
        make_parcel(2, "Residential", True, 6000),
        make_parcel(3, "Commercial", True, 7000),
    ]

    result = count_by_zone(parcels)

    assert result == {
        "Residential": 2,
        "Commercial": 1,
    }


def test_development_candidates_rejects_inactive():
    parcels = [
        make_parcel(
            1,
            "Residential",
            False,
            6000,
        )
    ]

    result = development_candidates(
        parcels,
        min_area=5000,
        allowed_zones={
            "Residential",
            "Commercial",
        },
    )

    assert result == []


def test_development_candidates_rejects_disallowed_zone():
    parcels = [
        make_parcel(
            1,
            "Industrial",
            True,
            6000,
        )
    ]

    result = development_candidates(
        parcels,
        min_area=5000,
        allowed_zones={
            "Residential",
            "Commercial",
        },
    )

    assert result == []


def test_development_candidates_rejects_too_small():
    parcels = [
        make_parcel(
            1,
            "Commercial",
            True,
            4000,
        )
    ]

    result = development_candidates(
        parcels,
        min_area=5000,
        allowed_zones={
            "Residential",
            "Commercial",
        },
    )

    assert result == []


def test_intersecting_parcels():
    study_area = SpatialObject(
        box(0, 0, 5, 5)
    )

    inside = make_parcel(
        1,
        "Residential",
        True,
        6000,
        box(1, 1, 2, 2),
    )

    outside = make_parcel(
        2,
        "Commercial",
        True,
        7000,
        box(10, 10, 11, 11),
    )

    result = intersecting_parcels(
        [inside, outside],
        study_area,
    )

    result_ids = [
        parcel.parcel_id
        for parcel in result
    ]

    assert result_ids == [1]


def test_classify_suitability_grid_handles_1_0_and_nodata():
    slope_grid = [
        [10, 20],
        [None, 15],
    ]

    flood_grid = [
        [0.3, 0.2],
        [0.4, 0.6],
    ]

    result = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope=15,
        max_flood=0.5,
    )

    assert result == [
        [1, 0],
        [None, 0],
    ]


def test_count_suitable_cells_ignores_zero_and_nodata():
    suitability_grid = [
        [1, 0],
        [None, 1],
    ]

    result = count_suitable_cells(
        suitability_grid
    )

    assert result == 2