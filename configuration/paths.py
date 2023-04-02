# imports
import os
import glob

#cons
DOT_DOT = ".."

FILES_DIR = "files"
EXP_DRIVERS_FILE_FROM_INSIDE = os.path.join(DOT_DOT ,FILES_DIR, "Drivers_with_kviut.csv")
NEW_DRIVERS_FILE_FROM_INSIDE = os.path.join(DOT_DOT ,FILES_DIR, "new_drivers.csv")
RATES_FILE_FROM_INSIDE = os.path.join(DOT_DOT, FILES_DIR, r"taarif.csv")

EXP_DRIVERS_FILE_FROM_OUTSIDE = os.path.join(FILES_DIR, "Drivers_with_kviut.csv")
NEW_DRIVERS_FILE_FROM_OUTSIDE = os.path.join(FILES_DIR, "new_drivers.csv")
RATES_FILE_FROM_OUTSIDE = os.path.join(FILES_DIR, r"taarif.csv")

CSV = "*"
TRIPS_DATA_DIR = "trips_data"
TRUCK_PATH_INSIDE = os.path.join(DOT_DOT, TRIPS_DATA_DIR, CSV)
TRUCK_PATH_OUTSIDE = os.path.join(TRIPS_DATA_DIR, CSV)
