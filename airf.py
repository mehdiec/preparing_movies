from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.ssh.operators.ssh import SSHOperator


default_args = {
    "owner": "you",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "cell_image_analysis_pipeline",
    default_args=default_args,
    description="An automated pipeline for cell image analysis",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 18),
    catchup=False,
)

# Python script for segmentation
segmentation = SSHOperator(
    task_id="segmentation_folder",
    ssh_conn_id="sancere",
    command="python /run/media/sancere/DATA1/segmentation-tools/scripts/inference_folder.py {{ dag_run.conf['project_folder'] if dag_run else '' }}",
    dag=dag,
)

create_run_batch = BashOperator(
    task_id="create_run_batch",
    bash_command="python create_run_batch_sap.py {{ dag_run.conf['project_folder'] if dag_run else '' }}",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_base = BashOperator(
    task_id="create_pipeline_files",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }}",
    dag=dag,
)
# Python script for preparing movies
peaking = BashOperator(
    task_id="peak_division",
    bash_command="python peak_division.py {{ dag_run.conf['project_folder'] if dag_run else '' }}",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_space_reg = BashOperator(
    task_id="create_sap_info_time_reg",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -sr",
    dag=dag,
)

# Python script for preparing movies
prepare_movies_map_arche = BashOperator(
    task_id="prepare_movies_map_arche",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -ra -archetype",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_map_rescale = BashOperator(
    task_id="prepare_movies_map_rescale",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -ra -rescale",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_rescaled_output_VM_AOT = BashOperator(
    task_id="prepare_movies_rescaled_output_VM_AOA",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -vm -aot",
    dag=dag,
)

# Python script for preparing movies
prepare_movies_map_AOA_first_animal = BashOperator(
    task_id="prepare_movies_map_AOA_first_animal",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -aoa --animal 0",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_map_AOA_second_animal = BashOperator(
    task_id="prepare_movies_map_AOA_second_animal",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -aoa --animal 1",
    dag=dag,
)
# Python script for preparing movies
prepare_movies_map_DBA = BashOperator(
    task_id="prepare_movies_map_DBA",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -dba",
    dag=dag,
)
prepare_movies_piv = BashOperator(
    task_id="prepare_movies_map_DBA",
    bash_command="python create_sap_info.py {{ dag_run.conf['project_folder'] if dag_run else '' }} -piv",
    dag=dag,
)

# MATLAB script: cell_tracking
run_sap_infos = BashOperator(
    task_id="run_sap_infos",
    bash_command='matlab -nodisplay -nosplash -r "addpath('
    + "'{{ dag_run.conf['project_folder'] if dag_run else '' }}'"
    + '); run_batch"',
    dag=dag,
)
# MATLAB script: cell_tracking
run_map_params = BashOperator(
    task_id="run_map_params",
    bash_command='matlab -nodisplay -nosplash -r "addpath('
    + "'{{ dag_run.conf['project_folder'] if dag_run else '' }}'"
    + '); MAP_parameters"',
    dag=dag,
)
run_map_params_animal1 = BashOperator(
    task_id="run_map_params_animal1",
    bash_command='matlab -nodisplay -nosplash -r "addpath('
    + "'{{ dag_run.conf['project_folder'] if dag_run else '' }}'"
    + '); MAP_parameters0"',
    dag=dag,
)
run_map_params_animal2 = BashOperator(
    task_id="run_map_params_animal2",
    bash_command='matlab -nodisplay -nosplash -r "addpath('
    + "'{{ dag_run.conf['project_folder'] if dag_run else '' }}'"
    + '); MAP_parameters1"',
    dag=dag,
)

# Here, you would add additional tasks like prepare_movies_2, cell_tracking_2, etc.

# Setting up the task dependencies
(
    prepare_movies_piv
    >> create_run_batch
    >> [segmentation, run_sap_infos]
    >> prepare_movies_base
    >> run_sap_infos
    # >> prepare_movies_space_reg  # HUGE STUPID ISSUE SOB
    # >> run_sap_infos
    # >> prepare_movies_map_arche
    # >> run_map_params
    # >> prepare_movies_map_rescale
    # >> run_map_params
    # >> prepare_movies_rescaled_output_VM_AOT
    # >> run_sap_infos
    # >> [prepare_movies_map_AOA_second_animal, prepare_movies_map_AOA_first_animal]
    # >> [run_map_params_animal1, run_map_params_animal2]
    # >> prepare_movies_map_DBA
    # >> run_map_params
)
