from config.paths_config import *
from src.data_processing import DataProcessing
from src.model_training import ModelTraining

if __name__ =="__main__":
    processor = DataProcessing(INPUT_PATH,OUTPUT_PATH)
    processor.run()

    trainer = ModelTraining(OUTPUT_PATH, MODEL_PATH)
    trainer.run()