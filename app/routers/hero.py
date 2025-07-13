from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Hero as HeroModel
from ..schemas import Hero as HeroSchema, HeroCreate
from ..crud import get_hero_by_name, create_hero
from ..dependencies import get_db
from ..external.superhero import fetch_hero_stats, SuperHeroAPIError

post_router = APIRouter(prefix="/hero", tags=["hero"])

@post_router.post("/", response_model=HeroSchema, status_code=status.HTTP_201_CREATED)
async def add_hero(
    payload: HeroCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await get_hero_by_name(db, payload.name)
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"Hero '{payload.name}' already exists")
    try:
        stats = await fetch_hero_stats(payload.name)
    except SuperHeroAPIError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))

    hero = await create_hero(db, stats)
    return hero


get_router = APIRouter(prefix="/heroes", tags=["heroes"])

@get_router.get("/", response_model=List[HeroSchema])
async def list_heroes(
    name: Optional[str] = Query(None, description="Exact match by name"),
    intelligence: Optional[int] = Query(None),
    intelligence_ge: Optional[int] = Query(None),
    intelligence_le: Optional[int] = Query(None),
    strength: Optional[int] = Query(None),
    strength_ge: Optional[int] = Query(None),
    strength_le: Optional[int] = Query(None),
    speed: Optional[int] = Query(None),
    speed_ge: Optional[int] = Query(None),
    speed_le: Optional[int] = Query(None),
    power: Optional[int] = Query(None),
    power_ge: Optional[int] = Query(None),
    power_le: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    filters = []
    if name:
        filters.append(HeroModel.name == name)

    def apply(field, eq, ge, le):
        if eq is not None:
            return field == eq
        clauses = []
        if ge is not None:
            clauses.append(field >= ge)
        if le is not None:
            clauses.append(field <= le)
        return and_(*clauses) if clauses else None

    for field, eq, ge, le in [
        (HeroModel.intelligence, intelligence, intelligence_ge, intelligence_le),
        (HeroModel.strength,     strength,     strength_ge,     strength_le),
        (HeroModel.speed,        speed,        speed_ge,        speed_le),
        (HeroModel.power,        power,        power_ge,        power_le),
    ]:
        clause = apply(field, eq, ge, le)
        if clause is not None:
            filters.append(clause)

    query = select(HeroModel)
    if filters:
        query = query.where(*filters)

    result = await db.execute(query)
    heroes = result.scalars().all()

    if not heroes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No heroes found with given parameters",
        )
    return heroes
