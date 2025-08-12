import uuid
from fastapi import Request

#This function will be exectuted between client and server
# It can act as a wrapper bfr going to the endpoint/client

#Example for microservices -> id to traceability
async def add_request_id(request: Request, call_next):
    #Before endpoint
    req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    #Call endpoint
    response = await call_next(request)
    #Before client
    response.headers["X-Request-ID"] = req_id
    return response