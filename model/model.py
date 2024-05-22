import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.colors = None
        self.grafo = nx.Graph()
        self.idProduct = {}
        self.sales = []
        self.solBest = None
        self.nodoPartenza = None


    def addColors(self):
        self.colors = DAO.getAllColors()
        return self.colors
    def createGraph(self, color, year):
        self.grafo.clear()
        for p in DAO.getProductsByColor(color):
            self.idProduct[p.Product_number] = p

        self.grafo.add_nodes_from(list(self.idProduct.keys()))

        self.sales = DAO.getAllSales(year, color)
        for sale1 in self.sales:
            for sale2 in self.sales:
                if sale1.Product_number != sale2.Product_number and sale1.Date == sale2.Date and sale1.Retailer_code==sale2.Retailer_code:
                    if not self.grafo.has_edge(sale1.Product_number, sale2.Product_number):
                        self.grafo.add_edge(sale1.Product_number, sale2.Product_number, weight = 1, date = [sale1.Date])
                    else:
                        if sale1.Date not in self.grafo[sale1.Product_number][sale2.Product_number]["date"]:
                            self.grafo[sale1.Product_number][sale2.Product_number]["weight"] += 1
                            self.grafo[sale1.Product_number][sale2.Product_number]["date"].append(sale1.Date)

        return self.grafo
        # edges = self.grafo.edges(data = True)
        # sorted_edges = sorted(edges, key=lambda x: x[2]["weight"], reverse=True)
        # for i in sorted_edges[:3]:
        #     print(i[0], i[1],i[2]["weight"])
        #return self.grafo
        # print(self.getNumNodes())
        # print(self.getNumEdges())

    def ricercaPercorso(self, product):
        self.solBest = []
        self.nodoPartenza = product
        #print(self.grafo.edges)
        self.ricorsione(product, [], [])



    def ricorsione(self, product, parziale, listaNodi):
        archi_uscenti = self.grafo.edges(product, data=True)
        proseguo = False
        arcoPiuLungo = None
        for arco in archi_uscenti:
            if len(parziale) == 0:
                proseguo = True
                if arcoPiuLungo is None or arco[2]["weight"] > arcoPiuLungo[2]["weight"]:
                    arcoPiuLungo = arco
            elif arco[2]["weight"] >= parziale[-1][2]["weight"] and arco[1] not in listaNodi:
                proseguo = True
                if arcoPiuLungo is None or arco[2]["weight"] > arcoPiuLungo[2]["weight"]:
                    arcoPiuLungo = arco

        #condizione terminale
        if not proseguo:
            if len(parziale) > len(self.solBest) and self.nodoPartenza in listaNodi:
                self.solBest = parziale


        else:
            parziale.append(arcoPiuLungo)
            listaNodi.append(product)
            print(len(parziale),parziale)
            self.ricorsione(arcoPiuLungo[1], parziale, listaNodi)
            parziale.pop()
            listaNodi.pop()




    # def checkVincoli(self):
    #     pass

    def getNumNodes(self):
        return len(self.grafo.nodes)
    def getNumEdges(self):
        return len(self.grafo.edges)

