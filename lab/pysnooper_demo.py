import pysnooper

from target import process_orders, build_demo_database


@pysnooper.snoop("lab/pysnooper_output.log")
def traced_process_orders():
    conn = build_demo_database()
    try:
        return process_orders(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    print(traced_process_orders())
