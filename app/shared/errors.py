from fastapi.responses import JSONResponse

type_mapping = {
    tuple: 'array' ,
    list: 'array' ,
    dict: 'object' ,
    bool: 'boolean' ,
    str: 'string' ,
    float: 'number' ,
    int: 'number' ,
}


class Error(Exception):
    def __init__(
            self , code: int , title: str , msg: str ,
            status = 400 , headers = None , extra = None
    ):
        self.code = code
        self.title = title
        self.msg = msg
        self.status = status
        self.headers = headers

        # Its kinda check if extra is in dictionary mode
        if not isinstance(extra , dict):
            raise TypeError("Invalid Extra Arguments")

        self.extra = extra

    @property
    def schema( self ):
        extra = {
            'title': 'Extra' ,
            'type': 'object' ,
            'properties': {}
        }

        for j , p in self.extra.items():
            t = type_mapping.get(type(p) , 'any')

            extra['properties'][j] = {'type': t}

        return {
            'title': 'Error' ,
            'type': 'object' ,
            'required': ['code' , 'status' , 'message' , 'title' , 'extra'] ,
            'properties': {
                'code': {'type': 'integer'} ,
                'message': {'type': 'string'} ,
                'status': {'type': 'integer'} ,
                'title': {'type': 'string'} ,
                'extra': extra ,
            } ,
            'example': {
                'code': self.code ,
                'message': self.msg ,
                'status': self.status ,
                'title': self.title ,
                'extra': self.extra ,
            }
        }

    def json( self ):
        return JSONResponse(
            status_code = self.status,
            content = {
                'code': self.code,
                'title': self.title,
                'message': self.msg,
                'status': self.status,
                'extra': self.extra
            },
            headers = self.headers
        )

    def __call__(self, *args, **kwargs):
        msg = kwargs.pop('msg', self.msg)
        headers = kwargs.pop('headers', {})

        obj = Error(
            headers = headers,
            code = self.code,
            title = self.title,
            msg = msg.format(*args , **kwargs),
            status = self.status,
            extra = kwargs,
        )

        return obj



bad_verification = Error(4002, 'Bad Verification', 'Invalid Verification', 400)

no_change = Error(4003, 'No Change', 'Nothing to Change', 400)


bad_id = Error(4004, 'Bad ID', 'invalid {} ID {}', 404, extra={'id': 21})
bad_auth = Error(4005, 'invalid authentication credentials', 403)
forbidden = Error(4006, 'Forbidden', 'Not Enough Permissions', 403)
rate_limited = Error(4007, 'Rate Limited', 'Too Many Requests', 429)
bad_args = Error(4009, 'Bad Args', 'invalid args', 400)
bad_file = Error(
    40013, 'Bad File',
    'invalid or unknown file',
    400
)
not_unique = Error(
    4014, 'Not Unique',
    '{} is not a unique {}',
    400, extra={'value': 'xxx'}
)


database_error = Error(50001, 'Database Error', 'Database Error', 500)

all_errors = {
    bad_verification, bad_id, no_change, bad_auth,
    forbidden, rate_limited, bad_args, bad_file,
    not_unique, database_error
}
