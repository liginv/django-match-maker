"""Models of the ``places`` app."""
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.utils.translation import ugettext_lazy as _


class PlaceManager(models.GeoManager):
    """Custom manager for the ``Place`` model."""
    def get_active(self):
        """Returns all places ordered by activity."""
        return self.get_query_set()

    def get_distance(self, lat, lng):
        """Returns all places and adds the computed distance."""
        pnt = Point(float(lng), float(lat))
        return self.get_query_set().distance(pnt)

    def get_nearby(self, radius, lat, lng):
        """Returns places nearby the given lat/lng within the given radius."""
        pnt = Point(float(lng), float(lat))
        places = self.get_query_set().filter(
            point__distance_lte=(pnt, D(km=radius))).distance(pnt)
        return places


class Place(models.Model):
    """
    Any place on earth.

    :name: The name of the place.
    :point: Lat/Lng of the place.
    :type: Optional type of the place.

    """
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )

    point = models.PointField(
        verbose_name=_('Point'),
        geography=True,
        null=True, blank=False,
    )

    type = models.ForeignKey(
        'places.PlaceType',
        verbose_name=_('Type'),
        null=True, blank=True,
    )

    objects = PlaceManager()

    def __unicode__(self):
        return self.name


class PlaceType(models.Model):
    """
    A masterdata table holding types of places.

    :name: The name of the type.

    """
    name = models.CharField(
        max_length=256,
        verbose_name=_('Name'),
    )

    def __unicode__(self):
        return self.name
