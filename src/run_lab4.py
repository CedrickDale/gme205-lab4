from shapely.geometry import box

from spatial import SpatialObject
from analysis import (
    development_candidates,
    intersecting_parcels
)


# F.1 Define the study area
study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)


# F.3 Combine attribute and spatial criteria
candidates = development_candidates(...)

inside_study_area = intersecting_parcels(
    candidates,
    study_area
)