from geopy import geocoders


class TimezoneMixin(object):
    """ mixin class that manage the user's timezone
    """
    def __init__(self, *args, **kwargs):
        self.geo = geocoders.GoogleV3()
        return super(TimezoneMixin, self).__init__(*args, **kwargs)

    def get_place_coordinates(self, city):
        """ returns <place, (lat, long)>
        """
        return self.geo.geocode(city)

    def get_timezone(self, city):
        place, (lat, lng) = self.get_place_coordinates(city)
        return self.geo.timezone((lat, lng))