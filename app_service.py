import tago

my_device = tago.Device('19af9c33-7e4e-4de3-bea1-e28273293ee0')

def transform_report_to_payload(report: dict):
    temperature_register = create_register("temperature", "C°", report["temperature"])
    humidity_register = create_register("humidity", "%", report["humidity"])

    return [temperature_register, humidity_register]

def create_register(variable: str, unit: str, value: int):
    return { "variable": variable, "unit": unit, "value": value}

def insert_device_payload(payload):
    return  my_device.insert(payload)