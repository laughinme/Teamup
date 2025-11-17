import type {ProfileResponseDto} from '@/shared/api/profile';
import type {ProfileResponse} from './types';

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
