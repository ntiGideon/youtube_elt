from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import extract_video_data, get_video_ids, get_playlist_id, save_to_json

from datawarehouse.dataware_house import staging_table, core_table
from dataquality.soda import yt_elt_data_quality

local_tz = pendulum.timezone("Africa/Accra")

## schemas
staging_schema = "staging"
core_schema = "core"

default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email": "gidiboateng200@gmail.com",
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2025, 1, 1, tzinfo=local_tz)
}

with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="DAG to produce JSON file with raw data",
    schedule="0 14 * * *",
    catchup=False
) as dag:
    # define tasks
    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extract_data)
    # define dependencies: this specifies in what order should the task runs
    playlist_id >> video_ids >> extract_data >> save_to_json_task



with DAG(
    dag_id="update_db",
    default_args=default_args,
    description="DAG to process JSON file and insert data into both staging and code schemas table ",
    schedule="0 15 * * *",
    catchup=False
) as dag:
    # define tasks
    update_staging = staging_table()
    update_core = core_table()
    # define dependencies: this specifies in what order should the task runs
    update_staging >> update_core


with DAG(
    dag_id="data_quality",
    default_args=default_args,
    description="DAG to check the data quality on both layers in the db",
    schedule="0 16 * * *",
    catchup=False
) as dag:
    # define tasks
    soda_validate_staging = yt_elt_data_quality(staging_schema)
    soda_validate_core = yt_elt_data_quality(core_schema)
    # define dependencies: this specifies in what order should the task runs
    soda_validate_staging >> soda_validate_core