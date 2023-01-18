import os
import urllib.request as request
from zipfile import ZipFile
from deepClassifier.entity import DataInjectionConfig
from deepClassifier import logger
from deepClassifier.utils import get_size
from tqdm import tqdm
from pathlib import Path
import shutil 


class DataIngestion:
    def __init__(self, config: DataInjectionConfig):
        self.config = config

    def download_file(self):
        logger.info("Trying to download file..")
        url=self.config.source_URL
        filename=self.config.local_data_file
        if not os.path.exists(self.config.local_data_file):
            logger.info("Download started")
            shutil.copy(url,filename)
            logger.info(f"{filename} downloaded from:  \n{url}")
        else:
            logger.info(
                f"File already exists of size: {get_size( Path(self.config.local_data_file))}"
            )

    def _get_updated_list_of_files(self, list_of_files):
        return [
            f
            for f in list_of_files
            # if f.endswith(".jpg") and ("COVID19" in f or "NORMAL" in f)
            if f.endswith(".jpg") and ("RRU_ON_THE_GROUND" in f or "RRU_ON_THE_TOP" in f)
        ]

    def _preprocess(self, zf: ZipFile, f: str, working_dir: str):
        target_filepath = os.path.join(working_dir, f)

        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)

        if os.path.getsize(target_filepath) == 0:
            logger.info(
                f"Removing file: {target_filepath} of size: {get_size(Path(target_filepath))}"
            )
            os.remove(target_filepath)

    def unzip_and_clean(self):
        logger.info(f"Unzipping and removing unwanted files")
        with ZipFile(file=self.config.local_data_file, mode="r") as zf:
            list_of_files = zf.namelist()
            updated_list_of_files = self._get_updated_list_of_files(
                list_of_files=list_of_files
            )
            for f in tqdm(updated_list_of_files):
                self._preprocess(zf, f, self.config.unzip_dir)
