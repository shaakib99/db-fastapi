from database.service import DatabaseService
from demo.router import router as DemoRouter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asgi import OpenTelemetryMiddleware
from opentelemetry import trace
from fastapi import FastAPI, Response, Request
from dotenv import load_dotenv
import uvicorn
import os
import json

def lifespan(app):
    load_dotenv()

    # check database connection
    db_service = DatabaseService(None)
    db_service.connect()
    db_service.create_metadata()
    yield
    db_service.disconnect()

app = FastAPI(lifespan=lifespan)

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(OpenTelemetryMiddleware)

# routes
routes = [DemoRouter]
for route in routes:
    app.include_router(route)


@app.middleware("http")
async def log_middleware(request:Request, call_next):
    req_tracer = trace.get_tracer(__name__)

    # Log the incoming request
    with req_tracer.start_as_current_span(f"[{request.method}] {request.url.__str__()}") as span:
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.headers", json.dumps(dict(request.headers)))
        span.set_attribute("http.query_params", json.dumps(dict(request.query_params)))

        if request.method.lower() != 'get':
            body = await request.body()
            span.set_attribute("http.request_body", body.decode("utf-8"))

        # Proceed with request
        response = await call_next(request)
        
        # Log outgoing reords
        span.set_attribute("http.response_status", response.status_code)
        span.set_attribute("http.response_headers", json.dumps(dict(response.headers)))
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        
        span.set_attribute("http.response_body", response_body.decode("utf-8"))

        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))


# Start application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port = int(os.getenv("PORT", "8000")), reload=True)