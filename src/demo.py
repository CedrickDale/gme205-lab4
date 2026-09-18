# # from shapely.geometry import box

# # from spatial import Parcel, SpatialObject
# # from analysis import (
# #     total_active_area,
# #     parcels_above_threshold,
# #     count_by_zone,
# #     development_candidates,
# #     intersecting_parcels
# # )


# # # Small synthetic parcel sample
# # parcels = [
# #     Parcel(
# #         1,
# #         box(121.050, 14.648, 121.052, 14.650),
# #         {
# #             "zone": "Residential",
# #             "is_active": True,
# #             "area_sqm": 6000
# #         }
# #     ),

# #     Parcel(
# #         2,
# #         box(121.060, 14.658, 121.062, 14.660),
# #         {
# #             "zone": "Commercial",
# #             "is_active": True,
# #             "area_sqm": 4500
# #         }
# #     ),

# #     Parcel(
# #         3,
# #         box(121.070, 14.668, 121.072, 14.670),
# #         {
# #             "zone": "Industrial",
# #             "is_active": False,
# #             "area_sqm": 8000
# #         }
# #     )
# # ]


# # # Analysis parameters
# # AREA_THRESHOLD = 5000
# # MIN_AREA = 5000
# # ALLOWED_ZONES = {"Residential", "Commercial"}

# # study_area = SpatialObject(
# #     box(121.049, 14.647, 121.055, 14.653)
# # )


# # # Small checks
# # active_area = total_active_area(parcels)

# # above_threshold = parcels_above_threshold(
# #     parcels,
# #     AREA_THRESHOLD
# # )

# # zone_counts = count_by_zone(parcels)

# # candidates = development_candidates(
# #     parcels,
# #     MIN_AREA,
# #     ALLOWED_ZONES
# # )

# # inside_study_area = intersecting_parcels(
# #     parcels,
# #     study_area
# # )


# # # Display results
# # print("Total active area:", active_area)

# # print(
# #     "Parcels above threshold:",
# #     [parcel.parcel_id for parcel in above_threshold]
# # )

# # print(
# #     "Zone counts:",
# #     zone_counts
# # )

# # print(
# #     "Development candidates:",
# #     [parcel.parcel_id for parcel in candidates]
# # )

# # print(
# #     "Intersecting parcels:",
# #     [parcel.parcel_id for parcel in inside_study_area]
# # )

# from shapely.geometry import box

# from spatial import Parcel
# from analysis import is_development_candidate


# allowed_zones = {"Residential", "Commercial"}
# min_area = 5000


# parcel_pass = Parcel(
#     1,
#     box(0, 0, 1, 1),
#     {
#         "zone": "Residential",
#         "is_active": True,
#         "area_sqm": 6000
#     }
# )

# parcel_inactive = Parcel(
#     2,
#     box(0, 0, 1, 1),
#     {
#         "zone": "Residential",
#         "is_active": False,
#         "area_sqm": 6000
#     }
# )

# parcel_wrong_zone = Parcel(
#     3,
#     box(0, 0, 1, 1),
#     {
#         "zone": "Industrial",
#         "is_active": True,
#         "area_sqm": 6000
#     }
# )

# parcel_too_small = Parcel(
#     4,
#     box(0, 0, 1, 1),
#     {
#         "zone": "Commercial",
#         "is_active": True,
#         "area_sqm": 4000
#     }
# )


# print(
#     "Pass:",
#     is_development_candidate(
#         parcel_pass,
#         min_area,
#         allowed_zones
#     )
# )

# print(
#     "Inactive:",
#     is_development_candidate(
#         parcel_inactive,
#         min_area,
#         allowed_zones
#     )
# )

# print(
#     "Wrong zone:",
#     is_development_candidate(
#         parcel_wrong_zone,
#         min_area,
#         allowed_zones
#     )
# )

# print(
#     "Too small:",
#     is_development_candidate(
#         parcel_too_small,
#         min_area,
#         allowed_zones
#     )
# )
from shapely.geometry import box

from spatial import Parcel, SpatialObject
from analysis import (
    development_candidates,
    intersecting_parcels
)


parcels = [
    Parcel(
        1,
        box(121.051, 14.649, 121.053, 14.651),
        {
            "zone": "Residential",
            "is_active": True,
            "area_sqm": 6000
        }
    ),

    Parcel(
        2,
        box(121.070, 14.670, 121.072, 14.672),
        {
            "zone": "Commercial",
            "is_active": True,
            "area_sqm": 7000
        }
    ),

    Parcel(
        3,
        box(121.052, 14.650, 121.054, 14.652),
        {
            "zone": "Industrial",
            "is_active": True,
            "area_sqm": 8000
        }
    )
]


study_area = SpatialObject(
    box(121.050, 14.648, 121.060, 14.658)
)


candidates = development_candidates(
    parcels,
    min_area=5000,
    allowed_zones={"Residential", "Commercial"}
)

inside_study_area = intersecting_parcels(
    candidates,
    study_area
)


print(
    "Development candidates:",
    [parcel.parcel_id for parcel in candidates]
)

print(
    "Development candidates inside study area:",
    [parcel.parcel_id for parcel in inside_study_area]
)