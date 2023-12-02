import base64

from fastapi import UploadFile , File , HTTPException, status


def read_write_file(path , file: UploadFile = File(...), ):

    with open(path , 'wb') as f:
        while chunk := file.file.read():
            try:
                f.write(chunk)
            except Exception as e:
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)

def write_by_base64(path , file: UploadFile = File(...)):
    contents = file.file.read()

    # Encode the contents to base64
    encoded_string = base64.b64encode(contents).decode('utf-8')

    with open(path, "wb") as f:
        try:
            f.write(base64.b64decode(encoded_string))
        except Exception as e:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST)