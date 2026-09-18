from shapely.geometry import Polygon

from src.spatial import Parcel


def test_parcel_from_dict():
    record = {
        "parcel_id": 1,
        "zone": "Residential",
        "is_active": True,
        "area_sqm": 5000,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [121.0, 14.0],
                [121.1, 14.0],
                [121.1, 14.1],
                [121.0, 14.1],
                [121.0, 14.0],
            ]],
        },
    }

    parcel = Parcel.from_dict(record)

    assert parcel.parcel_id == 1
    assert parcel.zone == "Residential"
    assert parcel.is_active is True
    assert parcel.area_sqm == 5000
    assert isinstance(
        parcel.geometry,
        Polygon,
    )