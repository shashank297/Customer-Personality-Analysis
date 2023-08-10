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
            Education=request.form.get('education'),
            Income=float(request.form.get('income')),
            Kidhome=int(request.form.get('kidhome')),
            Teenhome=int(request.form.get('teenhome')),
            Recency=int(request.form.get('recency')),
            MntWines=int(request.form.get('mntwines')),
            MntFruits=int(request.form.get('mntfruits')),
            MntMeatProducts=int(request.form.get('mntmeatproducts')),
            MntFishProducts=int(request.form.get('mntfishproducts')),
            MntSweetProducts=int(request.form.get('mntsweetproducts')),
            MntGoldProds=int(request.form.get('mntgoldprods')),
            NumDealsPurchases=int(request.form.get('numdealspurchases')),
            NumWebPurchases=int(request.form.get('numwebpurchases')),
            NumCatalogPurchases=int(request.form.get('numcatalogpurchases')),
            NumStorePurchases=int(request.form.get('numstorepurchases')),
            NumWebVisitsMonth=int(request.form.get('numwebvisitsmonth')),
            AcceptedCmp3=int(request.form.get('acceptedcmp3')),
            AcceptedCmp4=int(request.form.get('acceptedcmp4')),
            AcceptedCmp5=int(request.form.get('acceptedcmp5')),
            AcceptedCmp1=int(request.form.get('acceptedcmp1')),
            AcceptedCmp2=int(request.form.get('acceptedcmp2')),
            Complain=int(request.form.get('complain')),
            Response=int(request.form.get('response')),
            Customer_for=int(request.form.get('customer_for')),
            Age=int(request.form.get('age')),
            Spent=int(request.form.get('spent')),
            Living_with=request.form.get('living_with'),
            Children=int(request.form.get('children')),
            Family_size=int(request.form.get('family_size')),
            Is_parent=request.form.get('is_parent')
        )

        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(final_new_data)

        results = round(pred[0], 2)

        return render_template('results.html', final_result=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
