
def get_directory(self, filename):
    """ Directy of Profile picture
    """
    return 'profiles/{id}/{image}'.format(id=self.id, image=filename)


def get_directory_cover_photo(self, filename):
    """ Directory of Cover photo
    """
    return 'covers/{id}/{image}'.format(id=self.id, image=filename)