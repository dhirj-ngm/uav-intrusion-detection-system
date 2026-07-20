import joblib
import pandas as pd


class UAVPredictor:

    def __init__(self, model_path):

        artifact = joblib.load(model_path)

        self.model = artifact["model"]
        self.feature_columns = artifact["feature_columns"]
        self.feature_dtypes = artifact["feature_dtypes"]
        self.class_names = artifact["class_names"]

    def preprocess(self, data):

        df = pd.DataFrame([data])

        # Check missing columns
        missing = set(self.feature_columns) - set(df.columns)

        if missing:
            raise ValueError(f"Missing Features: {missing}")

        # Reorder
        df = df[self.feature_columns]

        # Convert datatype
        for col, dtype in self.feature_dtypes.items():
            df[col] = df[col].astype(dtype)

        return df

    def predict(self, data):

        sample = self.preprocess(data)

        pred = self.model.predict(sample)[0]

        confidence = self.model.predict_proba(sample)[0].max()

        return {
            "prediction": self.class_names[pred],
            "confidence": round(float(confidence) * 100, 2)
        }