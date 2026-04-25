from fastapi import FastAPI
app = FastAPI(title='Origin AI by Origin')

@app.get('/')
def root():
    return {'message': "Hello, I'm Origin AI — Origin's central intelligence. How can I help build the future today?"}
