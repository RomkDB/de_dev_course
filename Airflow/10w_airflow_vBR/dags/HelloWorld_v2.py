# 데코레이터를 사용한 코드
from airflow import DAG
from airflow.decorators import task
from datetime import datetime

# 데코레이터를 사용하여 태스크를 정의
@task
def print_hello():
    print("hello!")
    return "hello!"

@task
def print_goodbye():
    print("goodbye!")
    return "goodbye!"

# with문을 사용하여 DAG 객체를 생성
with DAG(
    dag_id = 'HelloWorld_v2',
    start_date = datetime(2022,5,5),
    catchup=False,
    tags=['example'],
    schedule = '0 2 * * *'
) as dag:

    # 태스크 실행 순서 정의(함수명이 태스크의 고유 식별자가 됨)
    print_hello() >> print_goodbye()