from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# DAG 객체 생성 : 작업의 구성과 스케줄링 정의
dag = DAG(
    dag_id = 'HelloWorld', # DAG의 고유 식별자
    start_date = datetime(2022,5,5), # 시작 날짜
    catchup=False, # backfill 수행여부
    tags=['example'], # DAG의 태그 정의
    schedule = '0 2 * * *') # 스케줄 설정(매일 2시에 실행)

def print_hello():
    print("hello!")
    return "hello!"

def print_goodbye():
    print("goodbye!")
    return "goodbye!"

# PythonOperator 태스크 생성
print_hello = PythonOperator(
    task_id = 'print_hello', # 태스크의 고유 식별자
    python_callable = print_hello, # 실행할 파이썬 함수
    dag = dag) # 태스크가 속한 DAG

print_goodbye = PythonOperator(
    task_id = 'print_goodbye',
    python_callable = print_goodbye,
    dag = dag)

# 태스크 실행 순서 정의(순서를 정하지 않으면 개별적으로 실행됨)
print_hello >> print_goodbye