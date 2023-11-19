from app import app  # Replace with the actual import for your Flask app

def handler(event, context):
    return app(event, context)