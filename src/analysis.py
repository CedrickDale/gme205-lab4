def total_active_area(parcels):
    total = 0.0

    for parcel in parcels:
        if parcel.is_active:
            total += parcel.area_sqm

    return total


def parcels_above_threshold(parcels, threshold):
    selected_parcels = []

    for parcel in parcels:
        if parcel.area_sqm >= threshold:
            selected_parcels.append(parcel)

    return selected_parcels


def count_by_zone(parcels):
    zone_counts = {}

    for parcel in parcels:
        zone = parcel.zone

        if zone not in zone_counts:
            zone_counts[zone] = 0

        zone_counts[zone] += 1

    return zone_counts


def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False

    if parcel.zone not in allowed_zones:
        return False

    if parcel.area_sqm < min_area:
        return False

    return True


def development_candidates(parcels, min_area, allowed_zones):
    candidates = []

    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)

    return candidates


def intersecting_parcels(parcels, study_area):
    selected_parcels = []

    for parcel in parcels:
        if parcel.intersects(study_area):
            selected_parcels.append(parcel)

    return selected_parcels

def classify_suitability_grid(
    slope_grid,
    flood_grid,
    max_slope,
    max_flood,
):
    if len(slope_grid) != len(flood_grid):
        raise ValueError(
            "Slope and flood grids must have the same number of rows"
        )

    suitability_grid = []

    for row_index in range(len(slope_grid)):
        slope_row = slope_grid[row_index]
        flood_row = flood_grid[row_index]

        if len(slope_row) != len(flood_row):
            raise ValueError(
                "Slope and flood grids must have the same number of columns"
            )

        output_row = []

        for col_index in range(len(slope_row)):
            slope_value = slope_row[col_index]
            flood_value = flood_row[col_index]

            if slope_value is None or flood_value is None:
                output_row.append(None)

            elif slope_value <= max_slope and flood_value <= max_flood:
                output_row.append(1)

            else:
                output_row.append(0)

        suitability_grid.append(output_row)

    return suitability_grid


def count_suitable_cells(suitability_grid):
    suitable_count = 0

    for row in suitability_grid:
        for cell in row:
            if cell == 1:
                suitable_count += 1

    return suitable_count