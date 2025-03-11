from app.database import Base, engine
from app.models import paste

def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()