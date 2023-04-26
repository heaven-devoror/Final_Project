from pathlib import Path
import pandas as pd
from zipfile import ZipFile
import io
from urllib.request import urlopen
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials

def fetch(dataset_url: str) -> pd.DataFrame:
    filedata = urlopen(dataset_url).read()
    filename = ZipFile(io.BytesIO(filedata))
    df = pd.read_csv(filename.open("global_power_plant_database.csv"), encoding = 'latin1')
    return df


@task()
def write_local(df: pd.DataFrame, dataset_file: str) -> Path:
    """"Write this dataframe to a csv file"""
    loc = Path.home() / 'Final_Project' / 'dataset' / 'global_dataset'
    try:
        loc.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        print("Folder is already there")
    else:
        print("Folder was created")
    file_name = f"{dataset_file}.csv"
    path = Path(loc / file_name)
    df.to_csv(path)
    return path

@task()
def write_gcs(path: Path, dataset_file: str) -> None:
    """Upload local csv file to GCS"""
    dest_path = Path(f"global/{dataset_file}.csv")
    gcs_block = GcsBucket.load("global-energy-bucket")
    gcs_block.upload_from_path(from_path=path, to_path=dest_path)
    return



@task()
def write_bq(df: pd.DataFrame) -> None:
    gcp_credentials_block = GcpCredentials.load("final-cred")
    df.to_gbq(
        destination_table="global_data_bq_storage.global_energy",
        project_id="dtc-de-course-374912",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow
def etl_web_to_gcs() -> None:
    """Main ETL Function"""
    dataset_file = "global_power_plant_database"
    dataset_url = "https://wri-dataportal-prod.s3.amazonaws.com/manual/global_power_plant_database_v_1_3.zip"

    df = fetch(dataset_url)
    path = write_local(df,dataset_file)
    write_gcs(path, dataset_file)
    write_bq(df)





if __name__ == '__main__':
    etl_web_to_gcs()