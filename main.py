import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0",  port=7000,reload=True) # 127.0.0.1 ,  port=7000, ,reload=True