import os

INPUT_PATH ='artifacts/raw/data.csv'
OUTPUT_PATH = 'artifacts/processed'

X_TRAIN_PATH = os.path.join(OUTPUT_PATH,"X_train.pkl")
X_TEST_PATH = os.path.join(OUTPUT_PATH,"X_test.pkl")
Y_TRAIN_PATH = os.path.join(OUTPUT_PATH,"y_train.pkl")
Y_TEST_PATH = os.path.join(OUTPUT_PATH,"y_test.pkl")

MODEL_PATH = "artifacts/models"
os.makedirs(MODEL_PATH, exist_ok=True)
MODEL_OUTPUT_PATH = os.path.join(MODEL_PATH,"model.pkl")