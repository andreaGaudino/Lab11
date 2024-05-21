import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []
        self._color = None
        self._year = None
        self.grafo = None

    def fillDD(self):
        #riempimento dd year
        self._view.btn_graph.disabled = False
        self._listYear = [2015, 2016, 2017, 2018]
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), self._listYear))
        self._view._ddyear.options = yearsDD

        #Riempimento dd color
        self._listColor = self._model.addColors()
        coloriDD = list(map(lambda x: ft.dropdown.Option(x), self._listColor))
        self._view._ddcolor.options = coloriDD
        self._view.update_page()


    def handle_graph(self, e):
        if self._view._ddyear.value is None or self._view._ddcolor.value is None:
            self._view.txtOut.clear()
            self._view.txtOut.controls.append(ft.Text(f"Anno o colore non selezionati"))
            return
        else:
            self._view._ddnode.disabled = False
            self._view.btn_search.disabled = False
            self._year = int(self._view._ddyear.value)
            self._color = self._view._ddcolor.value
            grafo = self._model.createGraph(self._color, self._year)
            self._view.txtOut.clean()
            self._view.txtOut.controls.append(ft.Text(f"Grafo creato correttamente"))
            self._view.txtOut.controls.append(ft.Text(f"Il grafo ha {len(grafo.nodes)} nodi e {len(grafo.edges)} archi"))

            edges = grafo.edges(data=True)
            sorted_edges = sorted(edges, key=lambda x: x[2]["weight"], reverse=True)

            lista_nodi_migliori = []

            for i in sorted_edges[:3]:
                self._view.txtOut.controls.append(ft.Text(f"Arco da {i[0]} a {i[1]}, peso={i[2]["weight"]}"))
                lista_nodi_migliori.append(i[0])
                lista_nodi_migliori.append(i[1])


            lista_ripetuti = []

            for j in lista_nodi_migliori:
                if lista_nodi_migliori.count(j)>1 and j not in lista_ripetuti:
                    lista_ripetuti.append(j)
            self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono: {lista_ripetuti}"))
            self.fillDDProduct()
            self._view.update_page()

    def fillDDProduct(self):
        listaProduct = self._model.idProduct.values()
        for p in listaProduct:
            self._view._ddnode.options.append(ft.dropdown.Option(text=p.Product, key = p.Product_number))
        self._view.update_page()




    def handle_search(self, e):
        product = self._view._ddnode.value
        self._model.ricercaPercorso(int(product))
