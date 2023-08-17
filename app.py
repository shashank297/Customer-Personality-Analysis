from flask import Flask, request, render_template, jsonify
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app = application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        data = CustomData(
            Income=float(request.form.get('income')),
            Customer_for=int(request.form.get('customer_for')),
            Age=int(request.form.get('age')),
            Spent=int(request.form.get('spent')),
            Children=int(request.form.get('children'))
        )

        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict_clusters(final_new_data)

        results = round(pred[0], 2)

        return render_template('results.html', final_result=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
