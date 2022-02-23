import logging

import azure.functions as func

from . import custom_functions

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

    print(custom_text)

    if custom_text:
        
        clean_text = custom_functions.clean_text(custom_text)
        return func.HttpResponse(f"{clean_text}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a custom_text in the query string or in the request body for a personalized response.",
             status_code=200
        )
