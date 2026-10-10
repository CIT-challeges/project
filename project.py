import psycopg2
 
 
# ---------------------------------------------------------------
# PART 1: connect to the database (credentials hardcoded on purpose)
# ---------------------------------------------------------------
def connect():
    return psycopg2.connect(
        host="prod-db.shopexample.internal",
        dbname="shop_production",
        user="",
        password="",   # hardcoded, the insecure part
    )
 
 
# ---------------------------------------------------------------
# PART 2: calculate sales
# ---------------------------------------------------------------
def total_sales(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT COALESCE(SUM(quantity * unit_price), 0) FROM orders")
        return cur.fetchone()[0]
 
 
def sales_by_product(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT product, SUM(quantity) AS units, SUM(quantity * unit_price) AS revenue
            FROM orders
            GROUP BY product
            ORDER BY revenue DESC
            """
        )
        return cur.fetchall()
 
 
def sales_by_day(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT created_at::date AS day, SUM(quantity * unit_price) AS revenue
            FROM orders
            GROUP BY day
            ORDER BY day
            """
        )
        return cur.fetchall()
 
 
if __name__ == "__main__":
    conn = connect()
    try:
        print(f"Total sales: ${total_sales(conn):,.2f}\n")
 
        print("Sales by product:")
        for product, units, revenue in sales_by_product(conn):
            print(f"  {product:<10} {units:>4} units  ${revenue:>10,.2f}")
 
        print("\nSales by day:")
        for day, revenue in sales_by_day(conn):
            print(f"  {day}  ${revenue:>10,.2f}")
    finally:
        conn.close()
