import apiProtected from "./axiosInstance";

export type ProfileResponseDto = {
    id: string;
    direction: string;
    bio: string | null;
    experience_level: string;
    achievements: string | null;
    timezone: string;
    visibility: string;
    tech_stack: TechStackDto[];
};

export type TechStackDto = {
    tag:{
        id: string;
        name: string;
        slug: string;
        kind: string;
    };
    level: number;
};

export const getProfile = async () => {
    const response = await apiProtected.get<ProfileResponseDto>('/users/me/profile');
    return response.data;
}

export type ProfileListDto = {
    items: ProfileResponseDto[];
    next_cursor: string | null;
}

export const getProfilesList = async (cursor: string | null, limit: number) => {
    const response = await apiProtected.get<ProfileListDto>('/profiles', { params: { cursor, limit } });
    return response.data;
}