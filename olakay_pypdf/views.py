import os, datetime
from pyhtml2pdf import converter
import logging, traceback
from rest_framework.views import APIView
from django.template import loader

from rest_framework.response import Response


def error_response(message='An error occurred', group='BAD_REQUEST', status_code=400):
    response_data = {'status': False, 'group': group, 'detail': message, 'message': message}
    return Response(response_data, status=status_code)

def success_response(data=None, message='Success',  status_code=200):
    response_data = {'status': True, 'message': message,'detail': message,'data': data}
    return Response(response_data, status=status_code)


def bad_request_response(message='Bad Request', group='BAD_REQUEST', status_code=400):
    return error_response(message, group , status_code)


def internal_server_error_response(message='Internal Server Error', status_code=500):
    return error_response(message, None, status_code)



class PYPDF(APIView):
    def get(**kwargs):
        try:
            # Email.send_aws_error_notification('olanrewaju@prembly.com','Export Start','EXPORTING PROCESS STARTED')
            columns = {
                "ID": 'identifier',
                "REFERENCE": 'reference',
                "AMOUNT": 'amount',
                "TYPE": 'type',
                "SCORE": 'score',
                "SEVERITY": 'severity',
                "STATE": 'state',
                "USER_ID": 'user_id',
            }
            records = [
                {
                    "id": "e40dc11d-ace9-4d2a-bd68-7ae2c918533b",
                    "amount": 600915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN2303090918",
                    "user": {
                        "id": "9d78137f-d826-43da-9223-1e69405cdebb",
                        "reference": "024-799-440190801",
                        "first_name": "AbdulKabeer",
                        "last_name": "olanrewaju"
                    }
                },
                {
                    "id": "8d1426ab-5b74-4c75-a4ac-0a534bae30e6",
                    "amount": 600915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN2303090918",
                    "user": {
                        "id": "407e8316-1477-4690-9af4-5fe28ebe6b53",
                        "reference": "024-799-2440190801",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                },
                {
                    "id": "528ed4bd-03d2-411f-aff1-af3c7d5fce27",
                    "amount": 60000915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN2303090918",
                    "user": {
                        "id": "0a4f935a-a19d-45e9-8fe1-73b0d86e6efe",
                        "reference": "024-799-244019080",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                },
                {
                    "id": "09b984b3-5470-4ca4-83db-7509075c94c5",
                    "amount": 60000915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN230309876tgh",
                    "user": {
                        "id": "ec98c99f-ce2a-4fc0-9d0f-b44fa41936a5",
                        "reference": "024-79-244019080",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                },
                {
                    "id": "1bbe074f-bcbd-432a-9c99-e426c9d21ac4",
                    "amount": 60000915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN230309876tgh",
                    "user": {
                        "id": "ec98c99f-ce2a-4fc0-9d0f-b44fa41936a5",
                        "reference": "024-79-244019080",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                },
                {
                    "id": "7fe74c00-fae9-4110-82dd-bbd21e8b6349",
                    "amount": 60000915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN230309876tgh",
                    "user": {
                        "id": "ec98c99f-ce2a-4fc0-9d0f-b44fa41936a5",
                        "reference": "024-79-244019080",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                },
                {
                    "id": "69a7301c-31a8-43a6-9b1a-f5354b3afa80",
                    "amount": 60000915.41,
                    "type": None,
                    "score": 0,
                    "severity": "low",
                    "state": None,
                    "user_id": "",
                    "reference": "293NKKEJEIOIIN230309876tgh",
                    "user": {
                        "id": "ec98c99f-ce2a-4fc0-9d0f-b44fa41936a5",
                        "reference": "024-79-244019080",
                        "first_name": "Felicia",
                        "last_name": "Gomez"
                    }
                }
            ]
            request = kwargs['request']



            columns_format = request.data.get('columns',[])

            if not columns_format:columns_format =  list(columns.keys())

            for col in columns_format:
                if col not in columns.keys():
                    return bad_request_response(message=f"{col} is an invalid, available choices are {','.join(columns.keys())}")
                
            data_to_export = [ columns_format ]
            for val in records:
                data_to_export.append([ getattr(val,columns[col],'N/A') for col in columns_format])

            today = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            today_html = datetime.datetime.now().strftime("%Y-%m-%d")

            # Load the template
            template = loader.get_template('email/tm/export.html')

            # Render the template with the provided context
            html_file_name = f'Transactions-{today}.html'
            pdf_file_name = f'Transactions-{today}.pdf'
            context = {'headers': data_to_export[0], 'data_to_export': data_to_export[1:],"today":today_html}
            rendered_html = template.render(context)

            # Save the rendered HTML to the file
            with open(html_file_name, 'w') as f:
                f.write(rendered_html)

            try:
                path = os.path.abspath(html_file_name)
                converter.convert(f'file:///{path}', pdf_file_name)
            finally:
                # Delete the temporary HTML file
                try:
                    print(path)
                    if os.path.exists(path):
                        os.unlink(path)
                        print("File has been deleted")
                    else:
                        print("File does not exist")
                except Exception as e:
                    print(e)
            

            
            return success_response()

        except Exception as e:
            logging.error(e)
            traceback_string = traceback.format_exc()
            logging.error(traceback_string)

            return internal_server_error_response(message=f"{str(traceback_string)} ::: {str(e)}")


    