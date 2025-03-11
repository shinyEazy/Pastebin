from sqlalchemy import inspect, text
from app.database import engine, Base
from app.models import paste

def create_database():
    inspector = inspect(engine)
    
    if "pastes" in inspector.get_table_names():
        print("Table 'pastes' exists. Dropping...")
        with engine.connect() as connection:
            connection.execute(text("DROP TABLE pastes"))
            connection.commit()
    
    print("Creating 'pastes' table...")
    Base.metadata.create_all(bind=engine)
    print("Database setup complete.")

if __name__ == "__main__":
    create_database()