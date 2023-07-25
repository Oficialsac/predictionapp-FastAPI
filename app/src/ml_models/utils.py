import joblib
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir,'joblib_linear.pkl')

def read_ml_model():
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        return model
    