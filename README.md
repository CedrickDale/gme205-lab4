# GmE 205 Laboratory 4 — Spatial Algorithms and Structured Programming

The main objective of this laboratory activity is to translate familiar GIS analysis operations into explicit algorithms using structured programming concepts such as sequence, selection, repetition, and functions while preserving the object-oriented responsibilities established in Laboratory 3.

This laboratory uses the existing `SpatialObject` and `Parcel` object model as the representation layer, while the analysis logic is implemented separately through structured functions for vector and raster-style processing.

## Objectives

The objectives of this laboratory are to:

- Translate spatial-analysis questions into clear algorithms and pseudocode before implementation.
- Identify where sequence, selection, and repetition appear in vector and raster workflows.
- Load parcel records as `Parcel` objects using the existing object model from Laboratory 3.
- Implement reusable analysis functions with clear responsibilities and shallow conditional structures.
- Use inherited Shapely behavior for spatial predicates such as intersection.
- Apply structured programming to both feature-based vector analysis and cell-based raster-style analysis.
- Produce reproducible JSON and visualization outputs.
- Verify the analysis logic using focused tests and reasonableness checks.

## Tools and Technologies

The following tools were used:

- Python 3.x
- Visual Studio Code
- Git
- GitHub
- Shapely
- Matplotlib
- JSON

### How to set up the virtual environment

1. Open the project folder (`gme205-lab4`) in VS Code.
2. Open the terminal (`Terminal -> New Terminal`) and create the virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Confirm that the terminal prompt shows (.venv).
4. Select the interpreter inside .venv using Ctrl + Shift + P -> Python: Select Interpreter.
5. Install the required packages and update requirements.txt:

```bash
pip install shapely matplotlib
pip freeze > requirements.txt
```

### Part C - Vector-Analysis Algorithm and Pseudocode

BEGIN

    LOAD data/parcels_shapely_ready.json

    CONVERT each record INTO a Parcel object
    STORE all Parcel objects IN all_parcels

    IF all_parcels IS EMPTY THEN
        PRINT "No parcels found"
        STOP
    END IF

    SET total_active_area = 0
    SET area_threshold = chosen threshold
    SET minimum_development_area = 5000
    SET allowed_zones = {"Residential", "Commercial"}

    CREATE parcels_above_threshold = EMPTY LIST
    CREATE zone_counts = EMPTY DICTIONARY
    CREATE development_candidates = EMPTY LIST
    CREATE intersecting_parcels = EMPTY LIST
    CREATE study_area_candidates = EMPTY LIST

    FOR EACH parcel IN all_parcels

        IF parcel.is_active THEN
            ADD parcel.area_sqm TO total_active_area
        END IF

        IF parcel.area_sqm >= area_threshold THEN
            ADD parcel TO parcels_above_threshold
        END IF

        IF parcel.zone NOT IN zone_counts THEN
            SET zone_counts[parcel.zone] = 0
        END IF

        INCREMENT zone_counts[parcel.zone] BY 1

        IF parcel.is_active
            AND parcel.zone IS IN allowed_zones
            AND parcel.area_sqm >= minimum_development_area
        THEN
            ADD parcel TO development_candidates
        END IF

        IF parcel INTERSECTS study_area THEN
            ADD parcel TO intersecting_parcels
        END IF

    END FOR

    FOR EACH parcel IN development_candidates

        IF parcel INTERSECTS study_area THEN
            ADD parcel TO study_area_candidates
        END IF

    END FOR

    PRINT "Total active area:", total_active_area
    PRINT "Parcels above threshold:", parcels_above_threshold
    PRINT "Parcel count per zone:", zone_counts
    PRINT "Development candidates:", development_candidates
    PRINT "Intersecting parcels:", intersecting_parcels
    PRINT "Development candidates inside study area:", study_area_candidates

END