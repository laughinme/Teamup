import type {ProfileResponseDto} from '@/shared/api/profile';
import type {ProfileResponse} from './types';
import type {ProfileListDto} from '@/shared/api/profile';
import type {ProfileListResponse} from './types';

export type TechStack = {
    tag:{
        id: string;
        name: string;
        slug: string;
        kind: string;
    };
    level: number;
};

export const toProfileResponse = (dto: ProfileResponseDto): ProfileResponse => ({
    id: dto.id,
    direction: dto.direction,
    bio: dto.bio,
    experienceLevel: dto.experience_level,
    achievements: dto.achievements,
    timezone: dto.timezone,
    visibility: dto.visibility,
    techStack: dto.tech_stack,
});

export const toProfileListResponse = (dto: ProfileListDto): ProfileListResponse => ({
    items: dto.items.map(toProfileResponse),
    nextCursor: dto.next_cursor,
});
