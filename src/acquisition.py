import requests

class Acquisition:
    """
    Acquisition
    """
    def __init__(self):
        """
        acquisition
        """
        pass

    def retrieve(self, url):
        """
        retrieve item/image as tmp_name.jpg
        """
        r = requests.get(url, allow_redirects=True)
        open('tmp_name.jpg', 'wb').write(r.content)
