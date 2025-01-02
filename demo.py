# from src.logger import logging

# logging.debug("This is debug msg")
# logging.info("This is info msg")
# logging.warning("This is warning msg")
# logging.error("This is error msg")
# logging.critical("This is critical msg")

# # Exception testing

# from src.logger import logging
# from src.exception import MyException
# import sys

# try:
#     a=1+'z'
# except Exception as e:
#     logging.info(e)
#     raise MyException(e,sys) from e

from src.pipeline.training_pipeline import TrainPipeline

pipeline = TrainPipeline()
pipeline.run_pipeline()