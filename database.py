import pymysql
import os

timeout = 10


def get_db_connection():
  return pymysql.connect(
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


def load_jobs_from_db():
  connection = None
  try:
    connection = get_db_connection()
    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM jobs")
      result = cursor.fetchall()
    return result
  finally:
    if connection:
      connection.close()


def load_job_with_id(job_id):
  connection = None
  try:
    connection = get_db_connection()
    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id, ))
      result = cursor.fetchall()
    return result[0] if result else None
  finally:
    if connection:
      connection.close()


def add_application_to_db(job_id, data):
  connection = None
  try:
    connection = get_db_connection()
    with connection.cursor() as cursor:
      cursor.execute(
          """
                INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
          (job_id, data['full_name'], data['email'], data['linkedin_url'],
           data['education'], data['work_experience'], data['resume_url']))
    connection.commit()
  finally:
    if connection:
      connection.close()