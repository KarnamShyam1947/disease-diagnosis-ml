from utils.predict import get_predicted_value, symptom_dict
from flask_restx import Api, reqparse, Resource, Namespace
from flask import Flask, request
from flask_cors import CORS
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
CORS(app)
api = Api(
    app=app,
    title="Disease diagnosis",
    description="Get the solution for your disease",
    version="1.0",
    validate=True,
    doc="/"
)

predict_args = reqparse.RequestParser()
predict_args.add_argument(name="symptoms", type=str, location="json")

predict_namespace = Namespace(name="predict controller", path="/predict")

@predict_namespace.route("/symptoms")
class Symptoms(Resource):
    def get(self):
        all_symptoms = {key: None for key in symptom_dict}
        return all_symptoms

@predict_namespace.route("/symptoms-list")
class Predict2(Resource):
    @predict_namespace.expect(predict_args)
    def post(self):
        symptoms = predict_args.parse_args()['symptoms']
        queries = [symptom.strip() for symptom in symptoms.split(',')]

        return get_predicted_value(queries)

@predict_namespace.route("/")
class Predict(Resource):
    def post(self):
        symptoms = request.json['symptoms']
        queries = list()
        for s in symptoms:
            queries.append(s['tag'])

        return get_predicted_value(queries)

api.add_namespace(predict_namespace)

if __name__ == "__main__":
    app.run(debug=True)
    

