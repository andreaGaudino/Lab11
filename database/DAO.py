from database.DB_connect import DBConnect
from model.dailySales import Sales
from model.products import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = "select distinct (gp.Product_color) from go_products gp  order by gp.Product_color asc "
        cursor.execute(query, ())

        for row in cursor:
            result.append(row[0])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProductsByColor(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary = True)
        query = "select * from go_products gp where gp.Product_color  = %s "
        cursor.execute(query, (color,))

        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllSales(year, color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds.Retailer_code , gds.Product_number , gds.Order_method_code , gds.`Date` , gds.Quantity , gds.Unit_price , gds.Unit_sale_price 
                from go_daily_sales gds , go_products gp 
                where year(gds.`Date`) = %s and gds.Product_number = gp.Product_number and gp.Product_color = %s  """
        cursor.execute(query, (year, color))

        for row in cursor:
            result.append(Sales(**row))
        cursor.close()
        conn.close()
        return result
