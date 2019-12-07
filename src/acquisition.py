import requests

class Acquisition:
    """
    Acquisition
    """
    def __init__(self):
        # init
        pass

    def retrieve(self, url):
        r = requests.get(url, allow_redirects=True)
        open('tmp_name.jpg', 'wb').write(r.content)

        
if __name__=="__main__":
    x = Acquisition()
    x.retrieve("http://84.241.3.55/cgi-bin/snapshot.cgi?chn=0&u=admin&p=&q=0&1575597402")
    
