import os
import random
from uuid import uuid4
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# Получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URI")

if not DATABASE_URL:
    raise ValueError("Database connection string is missing. Set SQLALCHEMY_DATABASE_URI.")

# Создаем подключение к базе
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# Определяем модель Product
class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

# Список весёлых татами-продуктов 😃
tatami_products = [
    {"name": "Sunny Tatami Mat", "description": "A tatami mat that brings sunshine to your home.", "price": 79.99, "stock": 50},
    {"name": "Cozy Winter Tatami", "description": "Stay warm with this cozy winter-style tatami mat.", "price": 89.99, "stock": 40},
    {"name": "Sakura Blossom Tatami", "description": "Inspired by cherry blossoms, this tatami mat adds elegance to any room.", "price": 99.99, "stock": 35},
    {"name": "Zen Garden Tatami", "description": "Perfect for meditation and relaxation.", "price": 109.99, "stock": 30},
    {"name": "Tatami of the Future", "description": "Futuristic tatami with smart temperature control.", "price": 129.99, "stock": 25},
    {"name": "Tatami Cloud", "description": "So soft, it feels like walking on clouds.", "price": 119.99, "stock": 20},
    {"name": "Lucky Bamboo Tatami", "description": "Infused with bamboo energy for positive vibes.", "price": 79.99, "stock": 55},
    {"name": "Samurai Warrior Tatami", "description": "Designed for warriors who need comfort.", "price": 149.99, "stock": 15},
    {"name": "Mountain Breeze Tatami", "description": "Feel the fresh mountain air in your home.", "price": 89.99, "stock": 45},
    {"name": "Tatami Midnight", "description": "Deep black tatami for an elegant and modern look.", "price": 99.99, "stock": 38},
    {"name": "Fire Dragon Tatami", "description": "Ignite your space with fiery red energy.", "price": 139.99, "stock": 18},
    {"name": "Ocean Wave Tatami", "description": "Inspired by the calming waves of the ocean.", "price": 129.99, "stock": 22},
    {"name": "Tatami Rainbow", "description": "Brighten up your home with a multi-color tatami mat.", "price": 79.99, "stock": 60},
    {"name": "Golden Sun Tatami", "description": "Luxury tatami mat with a golden finish.", "price": 159.99, "stock": 12},
    {"name": "Starlight Tatami", "description": "Tatami that sparkles in the dark.", "price": 99.99, "stock": 27},
    {"name": "Tatami Chill", "description": "Perfect for lazy Sunday afternoons.", "price": 89.99, "stock": 33},
    {"name": "Tatami Cloud 2.0", "description": "Even softer than before!", "price": 129.99, "stock": 28},
    {"name": "Nature Harmony Tatami", "description": "Brings the peace of nature into your home.", "price": 109.99, "stock": 31},
    {"name": "Lava Rock Tatami", "description": "Dark and powerful like a volcanic rock.", "price": 119.99, "stock": 26},
    {"name": "Neon Tatami", "description": "Glows under UV light for a cyberpunk feel.", "price": 139.99, "stock": 19},
    {"name": "Tatami Adventure", "description": "For those who like to take risks!", "price": 99.99, "stock": 40},
]

# Добавляем продукты в базу
def populate_products():
    session = SessionLocal()

    # Удаляем все существующие товары (опционально)
    session.query(Product).delete()
    session.commit()

    # Создаем и добавляем новые товары
    for product in tatami_products:
        new_product = Product(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            stock=product["stock"],
            image_url="https://media.licdn.com/dms/image/v2/C4E12AQH2ZsbtTuI2pg/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1520084713474?e=2147483647&v=beta&t=CRm-G4EddJQzS-siLFOjYmy--ZYFeyRIYEFP0W-ArLw",
            is_active=True
        )
        session.add(new_product)

    session.commit()
    session.close()
    print(f"✅ Successfully added {len(tatami_products)} Tatami products!")

if __name__ == "__main__":
    populate_products()