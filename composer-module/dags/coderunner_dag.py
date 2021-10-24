from datetime import timedelta, datetime, date
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, \
    DataprocClusterDeleteOperator
from airflow.contrib.operators import gcs_to_bq
from airflow.trigger_rule import TriggerRule
from airflow import DAG
from get_group_activities import *
from config import Config

cfg = Config()

DEFAULT_DAG_ARGS = {
    'depends_on_past': False,
    'start_date': datetime(2021, 10, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    'project_id': "${project_id}"
}

cluster_name = "CodeCluster-{{ ds_nodash }}"

schedule_interval="${schedule_interval}"
if schedule_interval == 'None':
    schedule_interval = None

def copy_csv_to_bucket():

    hook = GoogleCloudStorageHook()

    source_bucket = "${composer_bucket}"
    source_object = cfg.airflow_data_path + f"{cfg.output_filename}_{date.today().strftime('%Y-%m-%d')}.csv"
    target_bucket = "${datastore_bucket}"
    target_object = f"{cfg.output_filename}_{date.today().strftime('%Y-%m-%d')}.csv"

    hook.copy(source_bucket, source_object, target_bucket, target_object)
    hook.delete(source_bucket, source_object)


def create_cluster():
    return DataprocClusterCreateOperator(
        task_id='create_dataproc_cluster',
        cluster_name=cluster_name,
        zone='${zone}',
        region='${region}',
        tags=['dataproc']
    )

def delete_cluster():
    return DataprocClusterDeleteOperator(
        task_id='delete_dataproc_cluster',
        cluster_name=cluster_name,
        zone='${zone}',
        region='${region}',
        trigger_rule=TriggerRule.ALL_DONE
    )


with DAG('CodeRunnerETL',
        default_args=DEFAULT_DAG_ARGS,
        catchup=False,
        max_active_runs=1,
        schedule_interval=schedule_interval) as dag:

        create_cluster() >> extract_transform() >> copy_csv_to_bucket() >> delete_cluster()