
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import configparser
import os

# Read alembic.ini
config = configparser.ConfigParser()
config.read('alembic.ini')
url = config['alembic']['sqlalchemy.url']

print(f"Connecting to: {url}")

async def check_db():
    try:
        engine = create_async_engine(url)
        async with engine.connect() as conn:
            print("Connection successful!")
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
            tables = result.fetchall()
            print("Tables found in database:")
            for table in tables:
                print(f"- {table[0]}")
            
            # Check alembic version
            try:
                result_ver = await conn.execute(text("SELECT * FROM alembic_version;"))
                version = result_ver.scalar()
                print(f"Alembic Version: {version}")
            except Exception as e:
                print("Could not query alembic_version (table might not exist).")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check_db())
