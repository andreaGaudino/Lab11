import datetime
from dataclasses import dataclass

@dataclass
class Sales:
    Retailer_code: int
    Product_number : int
    Order_method_code : int
    Date : datetime.datetime
    Quantity : int
    Unit_price : float
    Unit_sale_price : float