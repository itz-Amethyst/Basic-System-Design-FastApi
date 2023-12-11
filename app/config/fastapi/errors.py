from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.shared.errors import all_errors


def Set_Errors_In_Doc_Schema(app: FastAPI):
    for route in app.routes:
        if not isinstance(route , APIRoute):
            continue

        errors = []

        for d in route.dependencies:
            errors.extend(getattr(d , 'errors' , []))

        oid = route.path.replace('/' , '_').strip('_')
        oid += '_' + '_'.join(route.methods)
        route.operation_id = oid

        errors.extend((route.openapi_extra or {}).pop('errors' , []))

        for e in errors:
            example = e.schema.get('example' , {})
            route.responses[e.code] = {
                'description': f'{e.title} - {e.status}' ,
                'content': {
                    'application/json': {
                        'schema': {
                            '$ref': f'#/errors/{e.code}' ,
                            'example': example
                        }
                    }
                }
            }

def Custom_OpenApi(app:FastAPI):
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema['errors'] = {}

    for e in all_errors:
        schema['errors'][e.code] = e.schema


    # Add individual error schemas under 'components/schemas/errors'
    for e in all_errors:
        schema['components']['schemas'][f'Error_Detail/{e.code} - {e.title}'] = e.schema

    app.openapi_schema = schema
    # return app.openapi_schema