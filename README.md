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


### Challenge 1 — Change the Policy Without Rewriting the Algorithm

The `development_candidates()` function was executed using two different parameter sets without changing the function implementation.

Policy 1:
- Minimum area: 5,000 m²
- Allowed zones: Residential and Commercial
- Candidate count: 45

Policy 2:
- Minimum area: 8,000 m²
- Allowed zones: Residential and Commercial
- Candidate count: 26

The results changed from 45 candidates to 26 candidates when the minimum area requirement was increased from 5,000 m² to 8,000 m². The `development_candidates()` function itself remained unchanged, demonstrating that the policy can be modified through input parameters rather than rewriting the algorithm.

### Challenge 2 — Compose, Do Not Duplicate

The development candidates inside the study area were obtained by composing existing analysis results instead of creating a new function that repeats all of the conditions.

First, the development candidates were identified using the existing `development_candidates()` function:

```python
candidates = development_candidates(
    parcels,
    min_area=5000.0,
    allowed_zones={"Residential", "Commercial"}
)
```

### Challenge 3 — Explain One “Bad vs Good” Refactor

An example of a less readable approach is to place all development-candidate conditions inside nested `if` statements:

```python
for parcel in parcels:
    if parcel.is_active:
        if parcel.zone == "Residential" or parcel.zone == "Commercial":
            if parcel.area_sqm >= min_area:
                candidates.append(parcel)
```

This approach works, but the conditions become more deeply nested as more criteria are added.

The final implementation uses a separate helper function:
```python

def is_development_candidate(parcel, min_area, allowed_zones):
    if not parcel.is_active:
        return False

    if parcel.zone not in allowed_zones:
        return False

    if parcel.area_sqm < min_area:
        return False

    return True
```
The collection function then handles only the repetition across parcels:
```python
def development_candidates(parcels, min_area, allowed_zones):
    candidates = []

    for parcel in parcels:
        if is_development_candidate(parcel, min_area, allowed_zones):
            candidates.append(parcel)

    return candidates
```

The responsibility for deciding whether one parcel satisfies the development policy was moved into is_development_candidate(). The development_candidates() function is then responsible only for looping through the parcel collection and collecting the parcels that pass the rule.

This makes the code easier to read, test, and extend because additional criteria can be added to the helper without creating deeper nested conditions in the collection loop.

### Challenge 4 — Transfer the Algorithmic Pattern

The vector analysis processes one `Parcel` object at a time:

```text
FOR EACH parcel
```

The raster analysis processes a two-dimensional grid:

```text
FOR EACH row
    FOR EACH column
```

The representation-specific parts are different. The vector workflow uses `Parcel` objects, parcel attributes, and spatial behavior such as intersection. The raster workflow uses row and column positions and evaluates cell values from the slope and flood grids.

However, the same structured-programming ideas are used in both workflows:

- **Sequence** — data is loaded, processed, and reported in a defined order.
- **Selection** — conditions determine whether a parcel or raster cell satisfies the analysis rule.
- **Repetition** — the vector workflow repeats over parcels, while the raster workflow repeats over rows and cells.
- **Functions** — separate functions are used to organize the analysis into smaller responsibilities.

The data representation changes, but the underlying algorithmic pattern remains the same.

## Part K — README Reflection

#### Algorithm

For the vector-analysis question on total active parcel area, writing the pseudocode first made the implementation more straightforward. The problem was separated into three simple steps: initialize the total, repeat through every parcel, and add the parcel area only when the parcel is active. This made the final function easier to write because the required inputs, condition, accumulator, and return value were already clear before writing Python code.

> **Algorithm insight:** Writing the logic first separates the problem-solving steps from the programming syntax, making the final implementation easier to trace and verify.

#### Control Flow

Sequence appears in the overall workflow where the program loads the data, constructs `Parcel` objects, defines the analysis parameters, performs the analysis, and produces the outputs. Selection appears in conditions such as checking whether a parcel is active, whether its area meets a threshold, whether its zone is allowed, whether it intersects the study area, and whether a raster cell satisfies the slope and flood criteria. Repetition appears when the program loops through parcel collections and when it processes raster rows and columns.

> **Control-flow insight:** Sequence defines the order of the workflow, selection decides which elements satisfy a rule, and repetition applies those decisions across the dataset.

#### Responsibility

The `intersects()` behavior belongs to `SpatialObject` because spatial intersection is a reusable geometric behavior that is not specific to one type of object. The development-candidate rule belongs to `analysis.py` because being active, belonging to an allowed zone, and meeting a minimum area threshold are analysis-specific criteria rather than permanent characteristics of every parcel.

> **Responsibility rule:** Spatial objects provide their own state and reusable spatial behavior, while analysis functions coordinate objects and apply project-specific rules.

#### Conditional Structure

The development-candidate logic avoids deeply nested `if` statements by using the `is_development_candidate()` helper function with guard clauses. Each failed condition immediately returns `False`, while parcels that satisfy all conditions return `True`. The `development_candidates()` function then only handles repetition across the parcel collection.

> **Conditional design:** Separating one-parcel decision logic from collection-level repetition keeps the code shallow, readable, and easier to extend.

#### Area Meaning

The exercise uses the provided `area_sqm` attribute instead of interpreting `geometry.area` as square meters because the parcel geometries use longitude and latitude coordinates. Shapely calculates area using the coordinate space supplied to it, so `geometry.area` would not automatically represent an area in square meters. The provided `area_sqm` value already contains the metric area required by the analysis.

> **Area meaning:** Geometry calculations depend on the coordinate system, so the model must use an attribute whose units correctly match the analysis question.

#### Vector vs Raster

Vector repetition processes one `Parcel` object at a time, so one loop is normally used to move through the parcel collection. Raster processing uses a two-dimensional grid, so it naturally requires an outer loop for rows and an inner loop for columns. Although the representation is different, both workflows still use repetition to process individual spatial elements and selection to determine whether each element satisfies the required rule.

> **Vector-raster insight:** The shape of the data changes how repetition is written, but the same sequence, selection, and repetition concepts remain underneath both workflows.

#### Scale

The separation between spatial objects, analysis functions, parameters, and runner responsibilities would remain useful even if the dataset grew to one million parcels or a `10,000 × 10,000` raster. The design would still make the system easier to understand and maintain. However, explicit Python loops over extremely large datasets would become inefficient. Larger workflows would likely require spatial indexing, chunked processing, optimized array operations, or specialized GIS libraries while preserving the same overall separation of responsibilities.

> **Scale insight:** Clean algorithm and object design remains useful at larger scales, but the implementation strategy must become more efficient as the amount of spatial data increases.