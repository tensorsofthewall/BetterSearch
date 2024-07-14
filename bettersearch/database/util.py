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