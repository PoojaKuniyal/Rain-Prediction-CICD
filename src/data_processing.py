import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os 
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger =get_logger(__name__)

class DataProcessing:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None

        os.makedirs(self.output_path, exist_ok=True)
        logger.info("Data processing initialized...")

    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data loaded successfully...")
        except Exception as e:
            logger.error(f"Error while loading data {e}")
            raise CustomException("Failed to load data", e)
    
    def preprocess_data(self):
        try:
            percent_missing = self.df.isnull().sum() * 100 / len(self.df)
            cols_to_drop = percent_missing[percent_missing >10].index
            self.df.drop(columns=cols_to_drop, inplace=True) 
            # Drop rows where target variables are missing
            self.df = self.df.dropna(subset=['RainTomorrow'])

            self.df['Date'] = pd.to_datetime(self.df['Date'])
            self.df['Year'] = self.df['Date'].dt.year
            self.df['Month'] = self.df['Date'].dt.month
            self.df['Day'] = self.df['Date'].dt.day
            self.df.drop("Date", axis=1, inplace=True)

            categorical = []
            numerical = []

            for col in self.df.columns:
                if self.df[col].dtype=='object':
                    categorical.append(col)
                else:
                    numerical.append(col)

            for col in self.df.columns:
                if col in numerical:
                    self.df[col]= self.df[col].fillna(self.df[col].median())
                else:
                    self.df[col] = self.df[col].fillna(self.df[col].mode()[0])

            for col in categorical:
                label_encoder = LabelEncoder()
                self.df[col] = label_encoder.fit_transform(self.df[col])
                label_mapping = dict(zip(label_encoder.classes_,range(len(label_encoder.classes_))))
                logger.info(f"Label mapping for {col}")
                logger.info(label_mapping)

            logger.info("Data processing done..")
        except Exception as e:
            logger.error(f"Error while preprocessing data {e}")
            raise CustomException("Failed to proprocess data..",e)
    
    
    def split_data(self):
        try:
            X = self.df.drop('RainTomorrow', axis=1)
            y = self.df.RainTomorrow

            logger.info(X.columns)

            X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2, stratify=y, random_state=90)

            joblib.dump(X_train, X_TRAIN_PATH)
            joblib.dump(X_test, X_TEST_PATH)
            joblib.dump(y_train, Y_TRAIN_PATH)
            joblib.dump(y_test, Y_TEST_PATH)

            logger.info("Splitted and saved successfully..")
        except Exception as e:
            logger.error(f"Error while splitting and saving pickle files")
            raise CustomException("Faailed to split and save data")

    def run(self):
        self.load_data()
        self.preprocess_data()
        self.split_data()
        logger.info("Data processing completeed..")

if __name__ =="__main__":
    processor = DataProcessing(INPUT_PATH,OUTPUT_PATH)
    processor.run()
