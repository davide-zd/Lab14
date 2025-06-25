from database.DB_connect import DBConnect
from model.ordine import Ordine


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getStore():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.store_id id
                    from stores s 
                    order by id"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(store):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.order_id id
                    from stores s, orders o 
                    where s.store_id = %s
                        and s.store_id = o.store_id"""
        cursor.execute(query, (store,))

        for row in cursor:
            result.append(Ordine(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(store, num_giorni):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select o1.order_id id1, o2.order_id id2, count(distinct oi1.item_id) + count(distinct oi2.item_id) peso
                    from stores s1, stores s2, orders o1, orders o2, order_items oi1, order_items oi2
                    where s1.store_id = o1.store_id 
                        and s2.store_id = o2.store_id
                        and oi1.order_id = o1.order_id 
                        and oi2.order_id = o2.order_id
                        and s1.store_id = %s
                        and s1.store_id = s2.store_id
                        and o1.order_id != o2.order_id
                        and datediff(o2.order_date, o1.order_date) > 0
                        and datediff(o2.order_date, o1.order_date) < %s
                    group by id1, id2
                    order by id1, id2"""
        cursor.execute(query, (store, num_giorni))

        for row in cursor:
            result.append((row["id1"], row["id2"], row["peso"]))
        cursor.close()
        conn.close()
        return result

#     """select o1.order_id id1, o2.order_id id2, o1.order_date, o2.order_date, datediff(o2.order_date, o1.order_date) giorni, oi1.item_id i1, oi2.item_id i2, count(distinct oi1.item_id), count(distinct oi2.item_id), count(distinct oi1.item_id) + count(distinct oi2.item_id) peso
# from stores s1, stores s2, orders o1, orders o2, order_items oi1, order_items oi2
# where s1.store_id = o1.store_id
# 	and s2.store_id = o2.store_id
# 	and oi1.order_id = o1.order_id
# 	and oi2.order_id = o2.order_id
# 	and s1.store_id = 1
# 	and s1.store_id = s2.store_id
# 	and o1.order_id != o2.order_id
# 	and datediff(o2.order_date, o1.order_date) > 0
# 	and datediff(o2.order_date, o1.order_date) < 5
# 	and o1.order_id = 14
# 	and o2.order_id = 16
# group by id1, id2
# order by id1, id2"""
