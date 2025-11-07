from __future__ import annotations

from uuid import UUID

from sqlalchemy import select

from database.relational_db import (
    Profile,
    ProfileTechTag,
    ProfilesInterface,
    ProfileTechTagsInterface,
    TechTagsInterface,
    UoW,
)
from domain.profiles import ProfileUpdate


class ProfileService:
    def __init__(
        self,
        uow: UoW,
        profiles: ProfilesInterface,
        tech_links: ProfileTechTagsInterface,
        tech_tags: TechTagsInterface,
    ) -> None:
        self.uow = uow
        self.profiles = profiles
        self.tech_links = tech_links
        self.tech_tags = tech_tags

    async def get_profile(self, user_id: UUID) -> Profile | None:
        return await self.profiles.get_by_id(user_id)

    async def list_profiles(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Profile]:
        stmt = select(Profile).limit(limit).offset(offset)
        result = await self.uow.session.scalars(stmt)
        return result.unique().all()

    async def upsert_profile(self, user_id: UUID, payload: ProfileUpdate) -> Profile:
        data = payload.model_dump(exclude_unset=True, exclude={"tech_stack"})
        profile = await self.get_profile(user_id)

        creating = profile is None
        if creating:
            required_fields = {"direction", "experience_level", "time_commitment", "timezone"}
            missing = [field for field in required_fields if field not in data]
            if missing:
                missing_fields = ", ".join(sorted(missing))
                raise ValueError(f"Missing fields for new profile: {missing_fields}")
            profile = Profile(id=user_id, **data)
            profile = await self.profiles.add(profile)
        else:
            for field, value in data.items():
                setattr(profile, field, value)

        if payload.tech_stack is not None:
            await self._sync_tech_stack(profile, payload)
        await self.uow.commit()
        await self.uow.session.refresh(profile)
        return profile

    async def _sync_tech_stack(self, profile: Profile, payload: ProfileUpdate) -> None:
        if payload.tech_stack is None:
            return

        await self.uow.session.execute(
            ProfileTechTag.__table__.delete().where(ProfileTechTag.profile_id == profile.id)
        )

        if not payload.tech_stack:
            await self.uow.session.flush()
            return

        links: list[ProfileTechTag] = []
        for link in payload.tech_stack:
            links.append(
                ProfileTechTag(
                    profile_id=profile.id,
                    tech_tag_id=link.tag_id,
                    level=link.level,
                )
            )
        self.uow.session.add_all(links)
        await self.uow.session.flush()


