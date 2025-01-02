from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from src.schemas import CommonFilters

class CommonService:

    @classmethod
    async def list(self, model, filters: CommonFilters, session: AsyncSession):
        stm = select(model).offset(filters.offset).limit(filters.page_size)
        if filters.sort_by:
            stm = stm.order_by(desc(filters.sort_by)) if filters.order == "desc" else stm.order_by(filters.sort_by)
        res = await session.execute(statement=stm)
        return res.scalars().all()