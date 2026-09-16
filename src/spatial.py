from shapely.geometry import Point as ShapelyPoint
from shapely.geometry import shape
import math


class SpatialObject:
    """Base abstraction for domain objects that have geometry."""

    def __init__(self, geometry):
        self.geometry = geometry

    def bbox(self):
        return self.geometry.bounds

    def intersects(self, other):
        return self.geometry.intersects(other.geometry)


class Point(SpatialObject):
    def __init__(self, id, lon, lat, name=None, tag=None):

        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")

        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        geometry = ShapelyPoint(lon, lat)
        super().__init__(geometry)

        self.id = id
        self.name = name
        self.tag = tag

    @property
    def lon(self):
        return self.geometry.x

    @property
    def lat(self):
        return self.geometry.y

    def to_tuple(self):
        return (self.lon, self.lat)

    def distance_to(self, other):
        return Point.haversine_m(
            self.lon,
            self.lat,
            other.lon,
            other.lat
        )

    @staticmethod
    def haversine_m(lon1, lat1, lon2, lat2):

        R = 6_371_000.0

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(dlambda / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return R * c

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            d["id"],
            float(d["lon"]),
            float(d["lat"]),
            name=d.get("name"),
            tag=d.get("tag")
        )

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tag": self.tag,
            "geometry": [
                self.lon,
                self.lat
            ],
            "bbox": list(self.bbox())
        }


class Parcel(SpatialObject):
    def __init__(self, parcel_id, geometry, attributes: dict):
        super().__init__(geometry)

        self.parcel_id = parcel_id
        self.attributes = attributes

    @property
    def area_sqm(self):
        return float(self.attributes["area_sqm"])

    @property
    def zone(self):
        return self.attributes["zone"]

    @property
    def is_active(self):
        return bool(self.attributes["is_active"])

    @classmethod
    def from_dict(cls, record):
        geometry = shape(record["geometry"])

        attributes = {
            "zone": record["zone"],
            "is_active": record["is_active"],
            "area_sqm": record["area_sqm"]
        }

        return cls(
            record["parcel_id"],
            geometry,
            attributes
        )

    def as_dict(self):
        return {
            "parcel_id": self.parcel_id,
            "bbox": list(self.bbox()),
            "attributes": self.attributes
        }