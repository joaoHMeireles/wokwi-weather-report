from flask import Flask, request
from app_service import transform_report_to_payload,  insert_device_payload

app = Flask(__name__)
domain = "/tago-io"
weather_domain = domain + '/weather/data'

@app.route(weather_domain, methods=['POST'])
def post_weather_conditions():
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        request_body =  request.json

        payload = transform_report_to_payload(request_body)
        result = insert_device_payload(payload)

        return result
    else:
        return 'Content-Type not supported!'

@app.route(weather_domain + '/last', methods=['GET'])
def get_last_register():
    return {"temperature": 12, "humdity": 65}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)