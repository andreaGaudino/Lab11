import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.colors = None
        self.grafo = nx.Graph()
        self.idProduct = {}
        self.sales = []


    def addColors(self):
        self.colors = DAO.getAllColors()
        return self.colors
    def createGraph(self, color, year):
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



    def getNumNodes(self):
        return len(self.grafo.nodes)
    def getNumEdges(self):
        return len(self.grafo.edges)

