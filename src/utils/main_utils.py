import os
import sys

import numpy as np
import dill
import yaml
from pandas import DataFrame

from src.exception import MyException
from src.logger import logging

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise MyException(e,sys)
    
def write_yaml_file(file_path:str, content: object, replace:bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise MyException(e,sys)
    
def load_object(file_path:str) -> object:
    """
    Returns model/object from project directory.
    file_path: str location of file to load
    return: Model/Obj
    """
    try:
        with open(file_path, 'rb') as file_obj:
            obj = dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(e,sys)
    
def save_numpy_array_data(file_path:str, array:np.array) -> None:
    try:
        # dir_path = os.path.join(file_path)
        # os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise MyException(e,sys)
    
def load_numpy_array_data(file_path:str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise MyException(e,sys)
    
def save_object(file_path:str, obj:object) -> None:
    logging.info("Entered the save_object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(obj,file)
        
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise MyException(e,sys)
     