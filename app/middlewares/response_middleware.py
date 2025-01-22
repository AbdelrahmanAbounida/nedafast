from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware, _StreamingResponse
from starlette.concurrency import iterate_in_threadpool
from app.middlewares.schemas import UnifiedResponse
from starlette.responses import StreamingResponse
from fastapi import Request, Response
import json
from pydantic_core._pydantic_core import ValidationError
from app.pipes.validation_pipe import ValidationPipe


class UnifiedResponseMiddleware(BaseHTTPMiddleware):
    """
        Response interceptor 

        handle unified resposne schema  
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            
            if isinstance(response, JSONResponse):
                return self.handle_json_response(response)
            elif isinstance(response, StreamingResponse):
                print(f"respoinse:L {response}")
                return self.handle_streaming_response(response)
            elif isinstance(response, (HTMLResponse, PlainTextResponse)):
                return self.handle_text_response(response)
            elif isinstance(response, _StreamingResponse):
                return await self.handle_streaming_response_async(response)
            
            return response
        except Exception as e:
            print(f"error: {e}")
            return ValidationPipe.handle_exception(e)

    def handle_json_response(self, response:Response):
        content = json.loads(response.body.decode())
        unified_response = self.create_unified_response(response.status_code, content)
        return JSONResponse(
            content=unified_response.model_dump(exclude_none=True),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

    def handle_streaming_response(self, response:Response):
        unified_response = self.create_unified_response(response.status_code)
        headers = dict(response.headers, **{
            "X-Unified-Status": "success" if response.status_code < 400 else "error",
            "X-Unified-Message": unified_response.message
        })
        return StreamingResponse(
            response.body,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type
        )

    def handle_text_response(self, response:Response):
        content = response.body.decode()
        unified_response = self.create_unified_response(response.status_code, content)
        return JSONResponse(
            content=unified_response.model_dump(exclude_none=True),
            status_code=response.status_code,
            headers=dict(response.headers)
        )

    async def handle_streaming_response_async(self, response:StreamingResponse):
        response_body = [chunk async for chunk in response.body_iterator]

        
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response_body = (b''.join(response_body)).decode()
        unified_response = self.create_unified_response(response.status_code, json.loads(response_body))
        return JSONResponse(content=unified_response.model_dump())

    def create_unified_response(self, status_code, content=None):
        if status_code == 422 and "detail" in content: # pydantic validation error 
            raise ValidationError.from_exception_data(
            title="Validation Error",
            line_errors=content["detail"]
        )
        return UnifiedResponse(
            code=status_code,
            message="Success" if status_code < 400 else "Error",
            data=content ,
            error=True if status_code >= 400 else False
        )

    