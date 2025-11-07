from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
from tensorflow import keras
import joblib

app = FastAPI(title="Hotel Cancellation Predictor")

# Setup template
templates = Jinja2Templates(directory="template")

# Load the model and preprocessor
try:
    model = keras.models.load_model('hotel_cancellation_model.keras')
    preprocessor = joblib.load('hotel_preprocessor.pkl')
    print("✓ Model and preprocessor loaded successfully")
except Exception as e:
    print(f"❌ Error loading model or preprocessor: {e}")
    model = None
    preprocessor = None

# Feature lists (same as in training)
features_num = [
    "lead_time", "arrival_date_week_number",
    "arrival_date_day_of_month", "stays_in_weekend_nights",
    "stays_in_week_nights", "adults", "children", "babies",
    "is_repeated_guest", "previous_cancellations",
    "previous_bookings_not_canceled", "required_car_parking_spaces",
    "total_of_special_requests", "adr",
]

features_cat = [
    "hotel", "arrival_date_month", "meal",
    "market_segment", "distribution_channel",
    "reserved_room_type", "deposit_type", "customer_type",
]

# Month mapping
month_mapping = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    # Numerical features
    lead_time: int = Form(...),
    arrival_date_week_number: int = Form(...),
    arrival_date_day_of_month: int = Form(...),
    stays_in_weekend_nights: int = Form(...),
    stays_in_week_nights: int = Form(...),
    adults: int = Form(...),
    children: int = Form(...),
    babies: int = Form(...),
    is_repeated_guest: int = Form(...),
    previous_cancellations: int = Form(...),
    previous_bookings_not_canceled: int = Form(...),
    required_car_parking_spaces: int = Form(...),
    total_of_special_requests: int = Form(...),
    adr: float = Form(...),
    # Categorical features
    hotel: str = Form(...),
    arrival_date_month: str = Form(...),
    meal: str = Form(...),
    market_segment: str = Form(...),
    distribution_channel: str = Form(...),
    reserved_room_type: str = Form(...),
    deposit_type: str = Form(...),
    customer_type: str = Form(...)
):
    if model is None or preprocessor is None:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "error": "Model or preprocessor not loaded properly"
        })
    
    try:
        # Create a DataFrame with the input data
        input_data = {
            'lead_time': [lead_time],
            'arrival_date_week_number': [arrival_date_week_number],
            'arrival_date_day_of_month': [arrival_date_day_of_month],
            'stays_in_weekend_nights': [stays_in_weekend_nights],
            'stays_in_week_nights': [stays_in_week_nights],
            'adults': [adults],
            'children': [children],
            'babies': [babies],
            'is_repeated_guest': [is_repeated_guest],
            'previous_cancellations': [previous_cancellations],
            'previous_bookings_not_canceled': [previous_bookings_not_canceled],
            'required_car_parking_spaces': [required_car_parking_spaces],
            'total_of_special_requests': [total_of_special_requests],
            'adr': [adr],
            'hotel': [hotel],
            'arrival_date_month': [month_mapping[arrival_date_month]],
            'meal': [meal],
            'market_segment': [market_segment],
            'distribution_channel': [distribution_channel],
            'reserved_room_type': [reserved_room_type],
            'deposit_type': [deposit_type],
            'customer_type': [customer_type]
        }
        
        df = pd.DataFrame(input_data)
        
        # Preprocess the input using the fitted preprocessor
        X_processed = preprocessor.transform(df)
        
        # Make prediction
        prediction_proba = model.predict(X_processed, verbose=0)
        probability = float(prediction_proba[0][0])
        
        # Determine result
        if probability > 0.5:
            prediction = "Likely to Cancel"
            confidence = probability
        else:
            prediction = "Not Likely to Cancel"
            confidence = 1 - probability
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "prediction": prediction,
            "confidence": round(confidence * 100, 2),
            "probability": round(probability * 100, 2)
        })
        
    except Exception as e:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "error": f"Prediction error: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
