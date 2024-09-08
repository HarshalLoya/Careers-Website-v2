import pymysql
import os

timeout = 10


def load_jobs_from_db():
  try:
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_CONN_NAME'],
        host=os.environ['DB_CONN_HOSTNAME'],
        password=os.environ['DB_CONN_PASS'],
        read_timeout=timeout,
        port=11166,
        user=os.environ['DB_CONN_USER'],
        write_timeout=timeout,
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jobs")
    result = cursor.fetchall()
    connection.close()
  finally:
    pass
    
  return result


def load_job_with_id(id):
  try:
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ['DB_CONN_NAME'],
        host=os.environ['DB_CONN_HOSTNAME'],
        password=os.environ['DB_CONN_PASS'],
        read_timeout=timeout,
        port=11166,
        user=os.environ['DB_CONN_USER'],
        write_timeout=timeout,
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM jobs WHERE id = {id}")
    result = cursor.fetchall()
    connection.close()
  finally:
    pass
    
  if len(result) == 0:
    return None
  else:
    return result[0]
