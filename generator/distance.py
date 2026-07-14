import math


def haversine_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calcola la distanza in km tra due coordinate
    utilizzando la formula di Haversine.

    Restituisce una stima della distanza stradale
    moltiplicando la distanza in linea d'aria
    per un coefficiente correttivo.
    """

    R = 6371.0  # Raggio medio della Terra (km)

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    distanza_linea_aria = R * c

    # Stima della distanza percorribile su strada
    distanza_stradale = distanza_linea_aria * 1.25

    return round(distanza_stradale, 1)