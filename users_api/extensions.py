def validate_length(item, column, length):
    if len(item) > length:
        raise LengthValidationError(column)
    return item


class LengthValidationError(BaseException):
    def __init__(self, column):
        self.column_name = column

# except extensions.LengthValidationError as exc:
# raise fastapi.exceptions.HTTPException(status_code=403,
#                                        detail={'exception': "LengthValidationError",
#                                                'column': exc.column_name})
