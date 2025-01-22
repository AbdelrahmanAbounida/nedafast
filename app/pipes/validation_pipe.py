from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic_core._pydantic_core import ValidationError
from fastapi.exceptions import RequestValidationError
from app.middlewares.schemas import UnifiedResponse
from fastapi.responses import JSONResponse


class ValidationPipe:

    @staticmethod
    def handle_exception(exc: Exception):

        if isinstance(exc, StarletteHTTPException):
            status_code, error_message = exc.status_code, str(exc.detail)
        elif isinstance(exc, RequestValidationError):
            status_code, error_message = 422, str(exc)
        elif isinstance(exc, ValidationError):
            errs = exc.errors()
            errors = []
            for err in errs:
                match err['type']:
                    case 'json_invalid':
                        errors.append(err["msg"]) 
                    case "string_type":
                        print(err)
                        errors.append(f"{'.'.join(err['loc'][1:])} error: " + err["msg"]  ) if len(err['loc']) > 1 else errors.append(err["msg"])
            
            status_code, error_message = 500, " ".join(errors)
        else:
            error_message="Internal Server error"
            status_code=500

        unified_response = UnifiedResponse(code=status_code, message=error_message, error= status_code < 400)
        print(f"unified_response: {unified_response}")
        return JSONResponse(
            content=unified_response.model_dump(exclude_none=True),
            status_code=status_code
        )