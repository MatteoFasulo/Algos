from math import sin, cos, sqrt, atan2, radians


def calculate_distance(lon1, lat1, lon2, lat2, R=6373.0):
    #print(lon1, lat1, lon2, lat2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return int(distance)
