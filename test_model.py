import joblib
import sklearn

print("Scikit-learn version:", sklearn.__version__)

try:
    model = joblib.load("student_performance_model.pkl")

    print("Model loaded successfully!")

except Exception as e:
    print("Model loading failed!")
    print("Error:", e)