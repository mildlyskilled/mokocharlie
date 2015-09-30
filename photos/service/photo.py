
class PhotoService:
    def __init__(self):
        pass

    provider = None

    def upload(self, image):
        if self.provider is not None:
            self.provider.upload(image)
        else:
            return None
