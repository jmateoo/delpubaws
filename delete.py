from flask import Flask, request, jsonify, make_response
import requests, json, os, boto3


app = Flask(__name__)


sqs = boto3.client('sqs', region_name='us-east-1')  
queue_url = 'https://sqs.us-east-1.amazonaws.com/019856031236/traslateoperator' 

@app.route('/v1/trasladar_ciudadano', methods=['DELETE'])
def delete_record():
    try:
        data = request.get_json()

        delete_url = "https://govcarpeta-76300fb42a5a.herokuapp.com/api-docs/#/default/delete_apis_unregisterCitizen"
        response = requests.delete(delete_url, json=data)
        print(response.status_code)
        if response.status_code == 200:
            print(response.content)
            message = {"id": data["id"],"operatorId": data["operatorId"], "operatorName": data["operatorName"]}
            response_content = response.content.decode('utf-8')
            data_json = json.dumps(data)
            # data_bytes = str(data).encode('utf-8')
            # future = publisher.publish(topic_path, data=data_bytes)
            sqs.send_message(QueueUrl=queue_url, MessageBody=data_json)
            return jsonify({'status_code': response.status_code, 'content': response_content, 'message': 'Ciudadano trasladado con exito', 'data':data}), 200
        else:
            return jsonify({'Error': "Error deleting record"}), response.status_code

    except Exception as e:
        app.logger.error("Error Request: %s", str(e))
        return jsonify ({"Error": "Error Request"})


@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({"message": "Failed: Application Error.."}), 500)

@app.errorhandler(501)
def not_implemented(error):
    return make_response(jsonify({"message": "Failed: Wrong Parameters.."}), 501)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)



