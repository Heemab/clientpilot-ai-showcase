from duckduckgo_search import DDGS


class SearchService:

    def search(self, query, max_results=10):

        results = []

        with DDGS() as ddgs:

            for item in ddgs.text(query, max_results=max_results):

                results.append(item)

        return results