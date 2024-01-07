from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
import requests
import logging
import psycopg2

def get_Redshift_connection():
    # 아래 변수 세팅 필요
    host = "*****"
    user = "*****"
    password = "*****"
    port = '****'
    dbname = "*****"
    conn = psycopg2.connect(f"dbname={dbname} user={user} host={host} password={password} port={port}")
    conn.set_session(autocommit=True)
    return conn.cursor()


def extract(url):
    logging.info("Extract started")
    f = requests.get(url)
    logging.info("Extract done")
    return (f.text)


def transform(text):
    logging.info("Transform started")
    lines = text.strip().split("\n")[1:]
    records = []
    for l in lines:
        (name, gender) = l.split(",")
        records.append([name, gender])
    logging.info("Transform ended")
    return records


def load(records):
    logging.info("load started")
    schema = "*****" # 세팅 필요
    cur = get_Redshift_connection()
    try:
        cur.execute("BEGIN;")
        cur.execute(f"DELETE FROM {schema}.name_gender;")

        for r in records:
            name = r[0]
            gender = r[1]
            print(name, "-", gender)
            sql = f"INSERT INTO {schema}.name_gender VALUES ('{name}', '{gender}')"
            cur.execute(sql)
        cur.execute("COMMIT;")   # cur.execute("END;")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        cur.execute("ROLLBACK;")
    logging.info("load done")

def etl(**context):
    link = context["params"]["url"]

    # 1차 개선 2번 : excution_data 얻어내기
    # context(딕셔너리) 안에는 Airflow가 관리하고 있는 시스템 변수들이 있음
    # task 자체에 대한 정보 (일부는 DAG의 정보가 되기도 함)를 읽고 싶다면 context['task_instance'] 혹은 context['ti']를 통해 가능
    # https://airflow.readthedocs.io/en/latest/_api/airflow/models/taskinstance/index.html#airflow.models.TaskInstance
    task_instance = context['task_instance']
    execution_date = context['execution_date']
    logging.info(execution_date)

    data = extract(link)
    lines = transform(data)
    load(lines)


dag = DAG(
    dag_id = 'name_gender_v2',
    start_date = datetime(2023,4,6),
    schedule = '0 2 * * *',
    catchup = False,
    # DAG의 수 설정
    max_active_runs = 1,
    # DAG 작업에 적용할 기본 인수 정의
    # retries : 실패시 시도해야하는 재시도 횟수
    # retry_delay : 재시도간의 시간 간격
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)


task = PythonOperator(
    task_id = 'perform_etl',
    python_callable = etl,
    # 1차 개선 1번 : params 변수를 통해 변수 넘기기
    # etl 함수에 link 변수에 할당하는 값
    params = {
        'url': "https://s3-geospatial.s3-us-west-2.amazonaws.com/name_gender.csv"
    },
    dag = dag)