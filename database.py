import pymysql
import os

def load_jobs_from_db():
  timeout = 10
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

  try:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM jobs")
    result = cursor.fetchall()
  finally:
    connection.close()

  return result
