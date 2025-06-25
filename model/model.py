import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def fillDD_store(self):
        lista_store = DAO.getStore()
        return lista_store

    def creaGrafo(self, store, num_giorni):
        # pulisco il grafo
        self._grafo.clear()

        # creo i nodi e li aggiungo
        lista_nodi = DAO.getNodes(store)
        for l in lista_nodi:
            self._grafo.add_node(l)
            self._idMap[l.id] = l

        # creo gli archi e li aggiungo
        lista_archi = DAO.getEdges(store, num_giorni)
        for a in lista_archi:
             self._grafo.add_edge(self._idMap[a[0]], self._idMap[a[1]], weight=a[2])

    def graphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def fillDD_ordini(self):
        return self._grafo.nodes



