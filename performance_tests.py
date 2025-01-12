import time
from concurrent.futures import ThreadPoolExecutor
from http_client import HttpClient

def measure_performance(urls, version, concurrent_clients=1):
    client = HttpClient(version)

    # Si c'est HTTP 1.1, activer le pipelining
    if version == "1.1":
        client.enable_pipelining()  # On va ajouter cette méthode dans http_client.py

    client.setup_client()

    # Log pour vérifier le nombre de clients concurrents
    print(f"Mesure de performance pour HTTP/{version} avec {concurrent_clients} clients concurrents...")

    start_time = time.time()

    # Utilisation de ThreadPoolExecutor avec le nombre de clients concurrents
    with ThreadPoolExecutor(max_workers=concurrent_clients) as executor:
        results = list(executor.map(client.fetch_page, urls))

    elapsed_time = time.time() - start_time
    client.close()

    return elapsed_time, results

def generate_report(times, versions, concurrent_levels, filename="performance_report.png"):
    import matplotlib.pyplot as plt

    # Afficher les résultats dans la console
    print("\n=== Résultats des performances ===")
    for version, time_taken in times.items():
        print(f"HTTP/{version} :")
        for i, time_value in enumerate(time_taken):
            print(f"  - {concurrent_levels[i]} client(s) concurrent(s) : {time_value:.2f} secondes")
        print()  # Ligne vide pour espacer les résultats

    # Générer le graphique
    for version, time_taken in times.items():
        plt.plot(concurrent_levels, time_taken, label=f"HTTP/{version}")  # Axe X = concurrent_levels

    plt.xlabel("Nombre de clients concurrents")
    plt.ylabel("Temps total (s)")
    plt.legend()
    plt.title("Comparaison des performances HTTP")
    plt.savefig(filename)
    plt.show()
