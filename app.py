from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import pymongo

#Create connection variable
conn='mongodb://localhost:27017'

# Initialize mongo connection
client=pymongo.MongoClient(conn)

#Connect to database us_energy_db
db=client.us_energy_db

#Initialize app
app=Flask(__name__)

cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Setup routes   
# @app.route("/")
# @cross_origin()
# def home():
#     energy_info = [doc for doc in db.State_EnergyData_2018.find({}, {'_id': False})]
#     # print(cs_info)
#     return jsonify(energy_info)

@app.route("/state/ranking")
@cross_origin()
def statedata():
    if (request.args):
        args=request.args
        print(args["name"])
        resultset=db.State_EnergyData_2018.find({"State Abbreviation":{"$eq":args["name"].upper()}}, {'_id': False})
        resultcount=db.State_EnergyData_2018.count_documents({"State Abbreviation":{"$eq":args["name"].upper()}})
        print(resultcount)
        if resultcount>0:
            state_data=[doc for doc in resultset]
            print(state_data)
            return jsonify(state_data)
        else:
            return jsonify({"Error":f"No matching record found for {args['name']}"}),404

    else:
        return jsonify({"error":"No query string"}), 404

@app.route("/state/production")
@cross_origin()
def productionsourcestatedata():
    if(request.args):
        args=request.args
        print(args["name"])
        value_search=args["name"].upper()
        resultcount=db.State_Energy_Production_Source_2018.count_documents({"State Abbreviation":value_search})
        print(resultcount)
        if resultcount>0:
            state_production_info= [doc for doc in db.State_Energy_Production_Source_2018.find({"State Abbreviation":value_search},{"_id":False})]
            return jsonify(state_production_info)
        else:
            return jsonify({"error":f"No record found for {args['name']}"}),404
    else:
        return jsonify({"Error":"No query string"}),404

@app.route("/renewables")
@cross_origin()
def renewable():
    energy_info = [doc for doc in db.US_Annual_Renewable.find({}, {'_id': False})]
    print(energy_info)
    # print(cs_info)
    return jsonify(energy_info)

if __name__=="__main__":
    app.run(debug=True)
