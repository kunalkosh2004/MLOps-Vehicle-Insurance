import sys
import os
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from src.logger import logging
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from src.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from src.exception import MyException
from src.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file

class DataTransformation:
    def __init__(self,
                 data_ingestion_artifact = DataIngestionArtifact,
                 data_validation_artifact = DataValidationArtifact,
                 data_transformation_config = DataTransformationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            self._schema_config = read_yaml_file(file_path = SCHEMA_FILE_PATH)
        except Exception as e:
            raise MyExeption(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys)
    
    def get_data_transformer_object(self) -> Pipeline:
        """
        Creates and returns a data transformer object for the data, 
        including gender mapping, dummy variable creation, column renaming,
        feature scaling, and type adjustments.
        """
        logging.info("Entered get_data_transformer_object of DataTransformer class")
        try:
            # Initialize Transformer
            numeric_transformer = StandardScaler()
            mm_transformer = MinMaxScaler()
            logging.info("Transformer initiated: StandardScaler,MinMaxScaler")
            
            # Load schema config
            num_features = self._schema_config['num_features']
            mm_features = self._schema_config['mm_columns']
            logging.info("Cols loaded from schema.")
            
            # Creating Pipeline
            preprocessor = ColumnTransformer(
                transformers=[
                    ("StandardScaler",numeric_transformer,num_features),
                    ("MinMaxScaler",mm_transformer,mm_features)
                ],
                remainder='passthrough' #Leave other columns as they are
            )
            
            # Wrapping up the pipeline
            final_pipeline = Pipeline(steps=[("Preprocessor",preprocessor)])
            logging.info("Final Pipeline Ready!")
            logging.info("Exited get_data_transformer_object of DataTransformer class")
            return final_pipeline
        except Exception as e:
            raise MyException(e,sys)
        
    def _map_gender_columns(self,df):
        """Map Gender column to 0 for Female and 1 for Male."""
        logging.info("Mapping Gender column-> Male:1, Female:0")
        df['Gender'] = df['Gender'].map({'Male':1,'Female':0}).astype(int)
        return df
    
    def _create_dummy_columns(self,df):
        """Create dummy variables for categorical features."""
        logging.info("Create dummies for categorical columns")
        df = pd.get_dummies(df,drop_first=True)
        return df
    
    def _rename_columns(self,df):
        """Rename specific columns and ensure integer types for dummy columns."""
        logging.info("Renaming specific columns and casting into int")
        df = df.rename(columns={
            "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        
        for col in ['Vehicle_Age_lt_1_Year','Vehicle_Age_gt_2_Years','Vehicle_Damage_Yes']:
            if col in df.columns:
                df[col] = df[col].astype(int)
        return df
    
    def _drop_id_columns(self,df):
        """Drop the 'id' column if it exists."""
        logging.info("Deleting id column from dataset")
        col = self._schema_config['drop_columns']
        df.drop(columns=col, inplace=True)
        return df
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Initiates the data transformation component for the pipeline.
        """
        try:
            logging.info("Data Transformation Started")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            # load train and test data
            train_df = self.read_data(file_path = self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(file_path = self.data_ingestion_artifact.test_file_path)
            logging.info("Train-test data loaded")
            
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            logging.info("Input ans Target columns defines for both train and test df.")
            
            # Apply custom transformation in specified seq
            input_feature_train_df = self._map_gender_columns(input_feature_train_df)
            input_feature_train_df = self._drop_id_columns(input_feature_train_df)
            input_feature_train_df = self._create_dummy_columns(input_feature_train_df)
            input_feature_train_df = self._rename_columns(input_feature_train_df)
            
            input_feature_test_df = self._map_gender_columns(input_feature_test_df)
            input_feature_test_df = self._drop_id_columns(input_feature_test_df)
            input_feature_test_df = self._create_dummy_columns(input_feature_test_df)
            input_feature_test_df = self._rename_columns(input_feature_test_df)
            logging.info("Custom transformation applied on train and test df.")
            
            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object")
            
            logging.info("Initializing transformation for Training-data")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            
            logging.info("Initializing transformation for Testing-data")
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Transformation Done end to end to train-test df")
            
            logging.info("Applying SMOOTEENN for handling imbalanced dataset")
            smt = SMOTEENN(sampling_strategy = 'minority')
            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr,target_feature_train_df
            )
            
            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr,target_feature_test_df
            )
            logging.info("SMOTEENN applied to train-test df.")
            
            train_arr = np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr = np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("Feature-target concatenation done for train-test df.")
            
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            
            dir_path = os.path.join(self.data_transformation_config.data_transformation_transformed_dir)
            os.makedirs(dir_path,exist_ok=True)
            # print(dir_path)
            
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=test_arr)
            logging.info("Saving transformation object and transformed files.")

            logging.info("Data transformation completed successfully")
            return DataTransformationArtifact(
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )            
        except Exception as e:
            raise MyException(e,sys)
        