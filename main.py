from performance_tests import measure_performance, generate_report

if __name__ == "__main__":
    # Liste des URLs à tester
    urls = [
        "https://www.cloudflare.com/",
        "https://www.cloudflare.com/",
        "https://www.cloudflare.com/"
    ]

    # Versions HTTP à tester
    versions = ["1.1", "2.0", "3.0"]

    # Liste des niveaux de clients concurrents à tester
    concurrent_levels = [1, 2, 3, 5, 10, 20]  # Ajout de nouveaux niveaux

    # Dictionnaire pour stocker les résultats de performance
    performance_results = {}

    # Effectuer les tests de performance pour chaque version HTTP et chaque niveau de concurrence
    for version in versions:
        performance_results[version] = []
        for clients in concurrent_levels:
            # Ajout d'un message pour indiquer l'utilisation de pipelining pour HTTP/1.1
            if version == "1.1":
                print(f"Test en cours pour HTTP/{version} avec pipelining, {clients} clients concurrents...")
            else:
                print(f"Test en cours pour HTTP/{version}, {clients} clients concurrents...")

            elapsed_time, _ = measure_performance(urls, version, concurrent_clients=clients)
            performance_results[version].append(elapsed_time)

    # Générer un rapport graphique
    generate_report(performance_results, versions, concurrent_levels)
