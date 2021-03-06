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

    def retrieve(self, url, temp_name="tmp_name.jpg"):
        """
        retrieve item/image as tmp_name.jpg or location
        """
        try:
            r = requests.get(url, allow_redirects=True, timeout=60)
            open(temp_name, 'wb').write(r.content)
        except Exception as e:
            # TODO : write a handler for this please
            #     raise requests.exceptions.Timeout
            pass
