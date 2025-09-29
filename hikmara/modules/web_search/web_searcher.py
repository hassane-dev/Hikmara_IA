# hikmara/modules/web_search/web_searcher.py
from googlesearch import search

class WebSearcher:
    """
    Un module simple pour effectuer des recherches web.
    """

    def __init__(self):
        """
        Initialise le chercheur web.
        """
        pass

    def perform_search(self, query: str, num_results: int = 5) -> tuple[bool, list | str]:
        """
        Effectue une recherche Google et retourne les meilleurs résultats.
        :param query: La requête de recherche.
        :param num_results: Le nombre de résultats à retourner.
        :return: Un tuple (succès, liste de résultats ou message d'erreur).
                 Chaque résultat est un dictionnaire {'title': ..., 'url': ...}.
        """
        try:
            # La bibliothèque googlesearch est un générateur, on le convertit en liste
            # L'option `lang='fr'` favorise les résultats en français.
            search_results = search(query, num_results=num_results, lang='fr', stop=num_results)

            # La bibliothèque ne retourne que les URLs, nous n'avons pas les titres.
            # Nous allons retourner une liste de dictionnaires avec l'URL.
            results_list = [{"url": url} for url in search_results]

            if not results_list:
                return False, "Aucun résultat n'a été trouvé pour votre recherche."

            return True, results_list

        except Exception as e:
            return False, f"Une erreur est survenue lors de la recherche: {e}"