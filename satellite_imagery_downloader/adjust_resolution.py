import math 
from .image_downloading import image_size  

def calculate_image_coords(lat, lon, w, h, z):
    R = (256 * 2**z) / 360
    delta_lon, delta_lat = w / R, h / R

    top_left =  lat + (delta_lat / 2), lon - (delta_lon / 2)
    bottom_right = lat - (delta_lat / 2), lon + (delta_lon / 2)

    return top_left, bottom_right

def center(lat1, lon1, lat2, lon2):
    return (lat1 + lat2) / 2, (lon1 + lon2) / 2

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def adjust_coords(lat1, lon1, lat2, lon2, zoom, desired_width=4000, desired_height=3000, print_info=True):
    init_center = center(lat1, lon1, lat2, lon2)
    tolerance = 0.1   
    adjustment_step = 0.001  
    cnt = 0
    max_iterations = 10**5

    while cnt < max_iterations:
        width, height = image_size(lat1, lon1, lat2, lon2, zoom)

        if abs(width - desired_width) < tolerance and abs(height - desired_height) < tolerance:
            break

        if height < desired_height:
            lat1 = min(lat1 + adjustment_step, 90)  
        else:
            lat1 = max(lat1 - adjustment_step, -90)

        if width < desired_width:
            lon2 = min(lon2 + adjustment_step, 180)  
        else:
            lon2 = max(lon2 - adjustment_step, -180)

        cnt += 1
        adjustment_step = max(0.00001, adjustment_step * 0.99)

        if width > 10 * desired_width or height > 10 * desired_height:
            print("Dimension explosion detected. Aborting adjustments.")
            break

    adjusted_center = center(lat1, lon1, lat2, lon2)
    delta = distance(init_center, adjusted_center)
    if print_info:
        print(f"Center distorted by {delta:.2f} km due to resolution adjustment.")

    return lat1, lon1, lat2, lon2

def adjust_for_resolution(center_lat, center_lon, zoom, width=4000, height=3000):
    (lat1, lon1), (lat2, lon2) = calculate_image_coords(center_lat, center_lon, width, height, zoom)
    lat1, lon1, lat2, lon2 = adjust_coords(lat1, lon1, lat2, lon2, zoom, width, height, print_info=True)
    lat1, lon1, lat2, lon2 = adjust_coords(lat1, lon1, lat2, lon2, zoom, width, height, print_info=False)
    top_left = lat1, lon1
    bottom_right = lat2, lon2
    return top_left, bottom_right