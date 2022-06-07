from flask import Flask, jsonify, render_template, request, Response
import pickle
import numpy
import sklearn
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard

from data_preprocessing import preprocessing
app=Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/predict',methods=['GET','POST'])
def index():
    from predictFromModel import prediction
    try:
        if request.json is not None:
            path = request.json['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(jsonify.loads(json_predictions) ))
        elif request.form is not None:
            path = request.form['filepath']

            pred_val = pred_validation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path,json_predictions = pred.predictionFromModel()
            return Response("Prediction File created at !!!"  +str(path) +'and few of the predictions are '+str(jsonify.loads(json_predictions) ))
        else:
            print('Nothing Matched')
    except ValueError:
        return Response("Error Occurred! %s" %ValueError)
    except KeyError:
        return Response("Error Occurred! %s" %KeyError)
    except Exception as e:
        return Response("Error Occurred! %s" %e)

    if request.method=='POST':
        try:

            age=int(request.form['age'])

            sex=request.form['sex']
            if sex=='female':
                sex=0
            else:
                sex=1

            bmi=float(request.form['bmi'])

            children=request.form['children']

            smoker=request.form['smoker']
            if smoker=='yes':
                smoker=1
            else:
                smoker=0

            region=request.form['region']
            if region=='northeast':
                region=0
            elif region=='northwest':
                region=1
            elif region=='southwest':
                region=2
            else:
                region=3

            filename=trainModel.returnmodel()
            model=pickle.load(open(filename,'rb'))
            prediction=model.predict([[age,sex,bmi,children,smoker,region]])
            print('prediction is', prediction)
            return render_template('results.html',prediction=prediction[0])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'



    else:
        return render_template('index.html')

def trainRouteClient():

    try:
        if request.json['folderPath'] is not None:
            path = request.json['folderPath']
            train_valObj = train_validation(path) #object initialization

            train_valObj.train_validation()#calling the training_validation function


            trainModelObj = trainModel() #object initialization
            trainModelObj.trainingModel() #training the model for the files in the table


    except ValueError:

        return Response("Error Occurred! %s" % ValueError)

    except KeyError:

        return Response("Error Occurred! %s" % KeyError)

    except Exception as e:

        return Response("Error Occurred! %s" % e)
    return Response("Training successfull!!")


if __name__=="__main__":
    app.run(debug=True,port=8000)