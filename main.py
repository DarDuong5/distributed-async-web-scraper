import uvicorn
from app import app
from database import engine, Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)