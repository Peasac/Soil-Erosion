from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model
MODEL_PATH = 'soil_erosion_model.pkl'
model = joblib.load(MODEL_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Collect input data from the form
            land_use = request.form['land_use']
            vegetation_cover = float(request.form['vegetation_cover'])
            elevation = float(request.form['elevation'])
            annual_rainfall = float(request.form['annual_rainfall'])

            # Prepare data for prediction
            input_data = pd.DataFrame({
                'Land_Use': [land_use],
                'Vegetation_Cover': [vegetation_cover],
                'Topography_Elevation_m': [elevation],
                'ANNUAL': [annual_rainfall]
            })

            # Predict soil erosion
            prediction = model.predict(input_data)[0]

            # Classify into risk categories
            if prediction < 300:
                risk_category = "Low Risk"
            elif 300 <= prediction <= 800:
                risk_category = "Moderate Risk"
            elif 800 < prediction <= 1200:
                risk_category = "High Risk"
            else:
                risk_category = "Severe Risk"

            return render_template(
                "index.html",
                prediction=round(prediction, 2),
                risk_category=risk_category,
                form_data=request.form
            )

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
