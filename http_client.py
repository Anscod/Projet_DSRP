import time
import httpx

class HttpClient:
    def __init__(self, version):
        self.version = version
        self.session = None
        self.pipelining_enabled = False  # Ajout pour gérer le pipelining

    def setup_client(self):
        # Configure le client en fonction de la version de HTTP
        if self.version == "1.1":
            if self.pipelining_enabled:
                self.session = httpx.Client(http2=False)  # HTTP/1.1 avec pipelining
                print("Pipelining activé pour HTTP/1.1.")
            else:
                self.session = httpx.Client(http2=False)  # HTTP/1.1 sans pipelining
        else:
            self.session = httpx.Client(http2=(self.version == "2.0"))  # HTTP/2.0 ou HTTP/3.0

    def enable_pipelining(self):
        # Activer le pipelining pour HTTP/1.1
        if self.version == "1.1":
            self.pipelining_enabled = True

    def fetch_page(self, url):
        max_retries = 3  # Nombre de tentatives maximum
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Erreur HTTP {response.status_code} pour {url}")
                return None
        except httpx.RequestError as e:
            print(f"Erreur lors du téléchargement de {url} : {e}")
            time.sleep(1)  # Attente avant de réessayer
            return None

    def close(self):
        if self.session:
            self.session.close()
