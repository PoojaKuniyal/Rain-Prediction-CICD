import os
import comet_ml
import joblib
import xgboost as xgb
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, input_path,model_output_path): # processed_data, model_output
        self.input_path = input_path
        self.model_output_path = model_output_path

        self.experiment = comet_ml.Experiment(
            api_key='DRn7a7zTlkucrld7cDwMyDAH2',
            project_name='rain-prediction-cicd',
            workspace='poojakuniyal'
        )

        self.model = xgb.XGBClassifier()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        logger.info("Model training and cometML initialized..")

    def load_data(self):
        try:
            self.X_train = joblib.load(X_TRAIN_PATH)
            self.X_test = joblib.load(X_TEST_PATH)
            self.y_train = joblib.load(Y_TRAIN_PATH)
            self.y_test = joblib.load(Y_TEST_PATH)

            self.experiment.log_asset(X_TRAIN_PATH)
            self.experiment.log_asset(X_TEST_PATH)
            self.experiment.log_asset(Y_TRAIN_PATH)
            self.experiment.log_asset(Y_TEST_PATH)

            logger.info("Data loaded successfully...")

        except Exception as e:
            logger.error(f"Failed to load saved data {e}")
            raise CustomException("Failed to load data", e)
        
    
    def train_model(self):
        try:
            self.model.fit(self.X_train, self.y_train)
            joblib.dump(self.model, MODEL_OUTPUT_PATH)
            self.experiment.log_asset(MODEL_OUTPUT_PATH)

            logger.info("Training and saving of model done")
        except Exception as e:
            logger.error(f"Error while training model {e}")
            raise CustomException("Failed to train model ",e)
        
    def evaluate_model(self):
        try:
            training_score = self.model.score(self.X_train,self.y_train)
            logger.info(f"Trainin model score : {training_score}")

            y_pred = self.model.predict(self.X_test)

            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted")
            recall = recall_score(self.y_test, y_pred,average="weighted" )
            f1 = f1_score(self.y_test, y_pred,average="weighted")

            self.experiment.log_metric("Accuracy", accuracy)
            self.experiment.log_metric("Precision", precision)
            self.experiment.log_metric("Recall", recall)
            self.experiment.log_metric("F1-score", f1)


            logger.info(f"Accuracy : {accuracy}; Precision : {precision}, Recall : {recall}; F1 : {f1}")
            logger.info("Model evaluation done..")

        except Exception as e:
            logger.error(f"error while evaluting model")
            raise CustomException("Failed to evaluate model")
        
    
    def run(self):
        self.load_data()
        self.train_model()
        self.evaluate_model()
        logger.info("model training and evaluation done")

if __name__=="__main__":
    trainer = ModelTraining(OUTPUT_PATH, MODEL_PATH)
    trainer.run()
