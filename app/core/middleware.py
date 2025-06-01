import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.exceptions import RateLimitExceededError
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.2f}s"
        )
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 100, time_window: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.requests = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old requests
        self.requests = {
            ip: timestamps 
            for ip, timestamps in self.requests.items()
            if current_time - timestamps[-1] < self.time_window
        }
        
        # Check rate limit
        if client_ip in self.requests:
            timestamps = self.requests[client_ip]
            if len(timestamps) >= self.rate_limit:
                raise RateLimitExceededError("API")
            timestamps.append(current_time)
        else:
            self.requests[client_ip] = [current_time]
        
        return await call_next(request)
