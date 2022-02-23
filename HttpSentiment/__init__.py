import logging

import azure.functions as func

from ..src import custom_functions

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    custom_text = req.params.get('custom_text')
    if not custom_text:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            custom_text = req_body.get('custom_text')

    if custom_text:
        # Call sentiment function
        text_features = custom_functions.get_text_features(custom_text)
        return func.HttpResponse(f"{text_features}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
