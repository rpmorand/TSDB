"""
TSDB unit testing cases.
"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: BSD-3-Clause

import os
import unittest

import tsdb
from tsdb.database import DATABASE
from tsdb.utils.logging import Logger

DATASETS_TO_TEST = [
    "ucr_uea_Wine",
    "physionet_2012",
    "beijing_multisite_air_quality",
]


class TestTSDB(unittest.TestCase):
    logger_creator = Logger(name="testing log", logging_level="debug")
    logger = logger_creator.logger

    def test_0_available_datasets(self):
        available_datasets = tsdb.list()
        assert len(available_datasets) > 0
        assert len(DATABASE) == len(available_datasets)

    def test_1_downloading_only(self):
        tsdb.download_and_extract("ucr_uea_Wine", "./save_it_here")
        file_list = os.listdir()
        assert len(file_list) > 0
        tsdb.purge_path("save_it_here")

    def test_2_dataset_loading(self):
        for d_ in DATASETS_TO_TEST:
            data = tsdb.load(d_)
            assert isinstance(data, dict), f"Loaded dataset {d_} is not a dict."

    def test_3_dataset_purging(self):
        cached_datasets = tsdb.list_cache()
        assert isinstance(cached_datasets, list)
        tsdb.delete_cache("physionet_2012")  # delete single
        tsdb.delete_cache()  # delete all

    def test_4_logging(self):
        # different level logging
        self.logger.debug("debug")
        self.logger.info("info")
        self.logger.warning("warning")
        self.logger.error("error")

        # change logging level
        self.logger_creator.set_level("info")
        assert (
            self.logger.level == 20
        ), f"the level of logger is {self.logger.level}, not INFO"
        self.logger_creator.set_level("warning")
        assert (
            self.logger.level == 30
        ), f"the level of logger is {self.logger.level}, not WARNING"
        self.logger_creator.set_level("error")
        assert (
            self.logger.level == 40
        ), f"the level of logger is {self.logger.level}, not ERROR"
        self.logger_creator.set_level("debug")
        assert (
            self.logger.level == 10
        ), f"the level of logger is {self.logger.level}, not DEBUG"

        # save log into file
        self.logger_creator.set_saving_path("test_log", "testing.log")
        assert os.path.exists("test_log/testing.log")


if __name__ == "__main__":
    unittest.main()
