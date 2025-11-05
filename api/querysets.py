from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Sqrt, Power, Cast, Cos, Radians

def calculate_distance(queryset, lat, long):
    """
    - Calculate distance by getting query params: lat long.
    - Annotate to recent rides.
    """

    try:
        lat = float(lat)
        long = float(long)
    except Exception as e:
        
        return queryset
    
    # Check north/south(latitude) and east/west
    if not (90 >= lat >= -90 and 180 >= long >= -180):
        
        return queryset
    
    globe_km_degree = 111.32

    queryset = queryset.annotate(
        distance_km=ExpressionWrapper(Sqrt(
            Power((Cast(F('pickup_lat'), FloatField()) - lat) 
                * globe_km_degree, 2) +
            Power((Cast(F('pickup_long'), FloatField()) - long)
                * globe_km_degree * Cos(Radians(lat)), 2
            )
        ),output_field=FloatField(),)
    )
    
    return queryset