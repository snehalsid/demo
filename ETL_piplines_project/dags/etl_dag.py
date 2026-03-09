from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024,1,1)
}

with DAG(
    dag_id="s3_postgres_etl",
    schedule_interval="@daily",
    catchup=False,
    default_args=default_args
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python /opt/airflow/scripts/extract.py"
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python /opt/airflow/scripts/transform.py"
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /opt/airflow/scripts/load.py"
    )

    extract >> transform >> load



# 6️⃣ Final DAG Flow
# S3 Raw Bucket
#       ↓
# Extract.py
# (download + read)
#       ↓
# Transform.py
# (clean data)
#       ↓
# Load.py
# (chunk insert into PostgreSQL)
#       ↓
# Cleanup
# (delete local file + move to Done folder)