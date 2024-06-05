#  Copyright (c) 2024. @Aiseed
#  Author: Andrew Lee

from fastapi import FastAPI
import uvicorn
from threading import Timer

app = FastAPI()

no_request_timer = None


def no_request_handler():
    print("No request from any service")


def reset_timer():
    global no_request_timer
    if no_request_timer:
        no_request_timer.cancel()
    no_request_timer = Timer(1, no_request_handler)
    no_request_timer.start()


@app.get("/")
async def read_root():
    reset_timer()
    return {"message": "Hello World"}


if __name__ == "__main__":
    reset_timer()
    uvicorn.run(app, host="0.0.0.0", port=8000)
