from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Hero as HeroModel

async def get_hero_by_name(db: AsyncSession, name: str):
    q = select(HeroModel).where(HeroModel.name == name)
    result = await db.execute(q)
    return result.scalars().first()

async def create_hero(db: AsyncSession, hero_data: dict):
    hero = HeroModel(**hero_data)
    db.add(hero)
    await db.commit()
    await db.refresh(hero)
    return hero
