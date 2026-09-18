import json
import os

import matplotlib.pyplot as plt
from shapely.geometry import box

from spatial import Parcel, SpatialObject

from analysis import (
    total_active_area,
    parcels_above_threshold,
    count_by_zone,
    development_candidates,
    intersecting_parcels,
    classify_suitability_grid,
    count_suitable_cells,
)


def main():

    # --------------------------------------------------
    # 1. Load parcel data
    # --------------------------------------------------

    with open(
        "data/parcels_shapely_ready.json",
        "r",
        encoding="utf-8"
    ) as file:
        parcel_records = json.load(file)


    # --------------------------------------------------
    # 2. Construct Parcel objects
    # --------------------------------------------------

    parcels = []

    for record in parcel_records:
        parcel = Parcel.from_dict(record)
        parcels.append(parcel)


    # --------------------------------------------------
    # 3. Validate parcel collection
    # --------------------------------------------------

    if len(parcels) == 0:
        print("No valid parcels were loaded.")
        return


    # --------------------------------------------------
    # 4. Define analysis parameters
    # --------------------------------------------------

    AREA_THRESHOLD = 10000.0

    MIN_AREA = 5000.0

    ALLOWED_ZONES = {
        "Residential",
        "Commercial"
    }

    study_area = SpatialObject(
        box(
            121.050,
            14.648,
            121.060,
            14.658
        )
    )


    # --------------------------------------------------
    # 5. Vector analysis
    # --------------------------------------------------

    active_area = total_active_area(parcels)

    above_threshold = parcels_above_threshold(
        parcels,
        AREA_THRESHOLD
    )

    zone_counts = count_by_zone(parcels)

    candidates = development_candidates(
        parcels,
        min_area=MIN_AREA,
        allowed_zones=ALLOWED_ZONES
    )

    candidates_policy_2 = development_candidates(
        parcels,
        min_area=8000.0,
        allowed_zones={"Residential", "Commercial"}
    )

    inside_study_area = intersecting_parcels(
        candidates,
        study_area
    )


    # --------------------------------------------------
    # 6. Load and analyze raster data
    # --------------------------------------------------

    with open(
        "data/suitability_grid.json",
        "r",
        encoding="utf-8"
    ) as file:
        raster_data = json.load(file)


    slope_grid = raster_data["slope_deg"]
    flood_grid = raster_data["flood_m"]

    max_slope = raster_data["criteria"]["max_slope_deg"]
    max_flood = raster_data["criteria"]["max_flood_m"]


    suitability_grid = classify_suitability_grid(
        slope_grid,
        flood_grid,
        max_slope,
        max_flood
    )

    suitable_cell_count = count_suitable_cells(
        suitability_grid
    )


    # --------------------------------------------------
    # 7. Assemble JSON-ready report
    # --------------------------------------------------

    report = {
        "vector": {
            "parcel_count": len(parcels),

            "total_active_area_sqm": active_area,

            "zone_counts": zone_counts,

            "above_threshold_ids": [
                parcel.parcel_id
                for parcel in above_threshold
            ],

            "candidate_ids": [
                parcel.parcel_id
                for parcel in candidates
            ],

            "study_area_candidate_ids": [
                parcel.parcel_id
                for parcel in inside_study_area
            ]
        },

        "raster": {
            "rows": len(suitability_grid),

            "cols": len(suitability_grid[0]),

            "suitable_cell_count": suitable_cell_count,

            "suitability_grid": suitability_grid
        }
    }


    # --------------------------------------------------
    # 8. Write report and figures
    # --------------------------------------------------

    os.makedirs(
        "output",
        exist_ok=True
    )


    # Write JSON report

    with open(
        "output/lab4_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            report,
            file,
            indent=4
        )


    # --------------------------------------------------
    # Vector preview
    # --------------------------------------------------

    fig, ax = plt.subplots()


    for parcel in parcels:

        geometry = parcel.geometry

        if geometry.geom_type == "Polygon":

            x, y = geometry.exterior.xy

            if parcel in candidates:
                ax.plot(
                    x,
                    y,
                    linewidth=2.5
                )

            else:
                ax.plot(
                    x,
                    y,
                    linewidth=0.8
                )


    study_x, study_y = study_area.geometry.exterior.xy

    ax.plot(
        study_x,
        study_y,
        linestyle="--",
        linewidth=2
    )


    ax.set_title(
        "Lab 4 Vector Analysis Preview"
    )

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.set_aspect(
        "equal",
        adjustable="box"
    )

    plt.tight_layout()

    plt.savefig(
        "output/lab4_vector_preview.png",
        dpi=300
    )

    plt.close()


    # --------------------------------------------------
    # Raster preview
    # --------------------------------------------------

    display_grid = []

    for row in suitability_grid:

        display_row = []

        for cell in row:

            if cell is None:
                display_row.append(
                    float("nan")
                )

            else:
                display_row.append(cell)

        display_grid.append(
            display_row
        )


    fig, ax = plt.subplots()

    image = ax.imshow(
        display_grid
    )

    ax.set_title(
        "Lab 4 Raster Suitability Preview"
    )

    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    plt.colorbar(
        image,
        ax=ax,
        label="Suitability"
    )

    plt.tight_layout()

    plt.savefig(
        "output/lab4_raster_preview.png",
        dpi=300
    )

    plt.close()


    # --------------------------------------------------
    # Finished
    # --------------------------------------------------

    print("Lab 4 workflow completed.")

    print(
    "Policy 1 candidate count:",
    len(candidates)
    )

    print(
    "Policy 2 candidate count:",
    len(candidates_policy_2)
    )
    
    print(
        "Report saved to:",
        "output/lab4_report.json"
    )

    print(
        "Vector preview saved to:",
        "output/lab4_vector_preview.png"
    )

    print(
        "Raster preview saved to:",
        "output/lab4_raster_preview.png"
    )


if __name__ == "__main__":
    main()