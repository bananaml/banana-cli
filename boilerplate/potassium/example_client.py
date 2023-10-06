# you need to install the Banana Python SDK for this:
# pip3 install banana-dev
from banana_dev import Client

# Create a reference to your model on Banana
my_model = Client(
    # Here pointed to your local instance of potassium.
    # Run it with `python3 app.py`
    # When testing your live model, you will want to 
    # change this to point to the model URL, which is 
    # found in the model page in the dashboard.
    url="http://localhost:8000", 

    # Found in the model page in the dashboard.
    api_key="YOUR_API_KEY"

    # If your python client is < 6.0.0, you will need 
    # to also include a "model_key" parameter, which may be left empty:
    # model_key=""
)

# Specify the model's input JSON. Below is an example 
# for a BERT model. Yours will be different, based on 
# your model's inputs in the `@app.handler` endpoint 
# in app.py
inputs = {
    "prompt": "Software developers start with a Hello, [MASK]! script",
}

# Call your model's inference endpoint on Banana
result, meta = my_model.call("/", inputs)

print(result)
