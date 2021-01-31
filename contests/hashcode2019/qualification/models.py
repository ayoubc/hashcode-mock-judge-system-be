class Photo:
    def __init__(self, orientation, tags, index):
        self.tags = set(tags)
        self.orientation = orientation
        self.num_tags = len(tags)
        self.index = index


class Slide:
    def __init__(self, photos):
        self.tags = set()
        for photo in photos:
            self.tags |= set(photo.tags)

    def get_tags(self):
        return self.tags
