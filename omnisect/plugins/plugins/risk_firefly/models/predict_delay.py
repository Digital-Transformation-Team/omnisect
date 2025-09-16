import os

import joblib
import pandas as pd


def predict_delay(temp: float, hum: float) -> int:
    """
    1 - zadderzhka
    0 - bez zadderzhki
    return: int
    """
    model = joblib.load(
        os.path.join(
            os.path.join(os.path.dirname(__file__)),
            "gradient_boosting_model.pkl",
        )
    )
    scaler = joblib.load(
        os.path.join(os.path.join(os.path.dirname(__file__)), "scaler.pkl")
    )
    df = pd.DataFrame({"Temperature": [temp], "Humidity": [hum]})
    df_scaled = scaler.transform(df)
    pred = model.predict(df_scaled)[0]
    return int(pred)
