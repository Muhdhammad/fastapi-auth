# libraries
from fastapi import FastAPI
from starlette.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
import uvicorn

# Local app modules
from routers import auth_routes
from database.database import get_db, create_table


limiter = Limiter(key_func=get_remote_address, default_limits=["100/day"])   # IP based rate limiting

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()  # SQLAlchemy sync function, no await
    yield

app = FastAPI(title="auth", version="1.0.0", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


app.include_router(auth_routes.router)

@app.get('/')
def root():
    return {"message": "api is running"}

@app.get('/health')
def health_check():
    return {"status": "ok"}

# get_db()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)