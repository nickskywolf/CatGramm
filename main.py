import redis.asyncio as redis
from fastapi import FastAPI, Request, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware
from scr.routes import notes, users, tags, auth, cloud, comments, posts
from scr.conf.config import config

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix="/api")
app.include_router(tags.router, prefix='/api')
app.include_router(comments.router, prefix="/api")
app.include_router(posts.posts_router, prefix='/posts',
                   dependencies=[Depends(RateLimiter(times=2, seconds=5))])
app.include_router(cloud.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0, encoding="utf-8",
                          password=config.REDIS_PASSWORD, decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/")
def read_root():
    return {"message": "Hello World! We are present GatsGramm!!!"}
