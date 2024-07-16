import os
import platform
from collections import defaultdict
from .constants import parsable_exts
from pathlib import Path

def convert_gps_info_to_lat_lon_alt(gpsInfo):
    def convert_to_degrees(value):
        degrees, minutes, seconds = value
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    lat_direction = gpsInfo[1]
    lat_value = gpsInfo[2]
    lon_direction = gpsInfo[3]
    lon_value = gpsInfo[4]
    altitude = gpsInfo[5]
    
    latitude = convert_to_degrees(lat_value)
    if lat_direction == 'S':
        latitude = -latitude
    
    longitude = convert_to_degrees(lon_value)
    if lon_direction == 'W':
        longitude = -longitude
    
    return f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}m"


def get_all_exts(exts):
    all_exts = []
    for key in exts.keys():
        if any(isinstance(sub, list) for sub in exts[key]):
            for sublist in exts[key]:
                all_exts.extend(sublist)
        else:
            all_exts.extend(exts[key])
    return all_exts


def find_files_recursively(folders):
        files = []
        for dir in folders:
            dir_path = Path(dir)
            if dir_path.exists() and dir_path.is_dir():
                files.extend([p for p in dir_path.rglob('*') if p.suffix in get_all_exts(parsable_exts)])
        
        return files


def create_init_config():
    config = defaultdict(str)
    config['index_folders'] = os.path.expanduser("~")
    if platform.system() == "Windows":
        config['index_folder_exceptions'] = os.path.join(os.path.expanduser("~"), "AppData")
    return config