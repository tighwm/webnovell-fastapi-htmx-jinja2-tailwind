from pydantic import ValidationError

from rest.auth.schemas import RegistrationForm


def validate_form(data):
    try:
        RegistrationForm(**data)
    except ValidationError as e:
        errs = e.errors()
        for err in errs:
            field = err["loc"]
            msg = err["msg"]
            msg = msg.split(maxsplit=2)
            data[f"{field[0]}_err"] = msg[2]
        return False
    return True
