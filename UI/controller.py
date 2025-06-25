import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._nodo_selezionato = None

    def fillDDStore(self):
        lista_store = self._model.fillDD_store()
        self._view._ddStore.options.clear()

        for a in lista_store:
            self._view._ddStore.options.append(ft.dropdown.Option(
                text=a,
            ))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        store = self._view._ddStore.value
        num_giorni = self._view._txtIntK.value

        if (store is None):
            self._view.txt_result.controls.append(ft.Text("Devi selezionare uno store."))
            self._view.update_page()
            return

        if (num_giorni == ""):
            self._view.txt_result.controls.append(ft.Text("Devi scrivere un numero di giorni."))
            self._view.update_page()
            return

        try:
            num_giorni = int(num_giorni)
        except:
            self._view.txt_result.controls.append(ft.Text("Deve essere un numero intero."))
            self._view.update_page()
            return

        # creo il grafo e i dettagli
        self._model.creaGrafo(store, num_giorni)
        n, e = self._model.graphDetails()

        # stampo nodi e archi
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {n} nodi e {e} archi"))
        self._view.update_page()

        self.fillDD_ordini()


    def fillDD_ordini(self):
        lista_ordini = self._model.fillDD_ordini()
        self._view._ddNode.options.clear()

        for a in lista_ordini:
            self._view._ddNode.options.append(ft.dropdown.Option(
                text=a.id,
                data=a,
                on_click=self.read_DD_ordini
            ))
        self._view.update_page()

    def read_DD_ordini(self, e):
        if e.control.data is None:
            self._nodo_selezionato = None
        else:
            self._nodo_selezionato = e.control.data


    def handleCerca(self, e):
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._nodo_selezionato}"))
        lista_nodi_connessi = self._model.getCammino(self._nodo_selezionato)
        for n in lista_nodi_connessi:
            self._view.txt_result.controls.append(ft.Text(f"{n.id}"))
        self._view.update_page()

    def handleRicorsione(self, e):
        pass
