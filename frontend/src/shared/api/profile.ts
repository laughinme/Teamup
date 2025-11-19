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

export const getProfile = async (): Promise<ProfileResponseDto> => {
    const response = await apiProtected.get('/users/me/profile');
    return response.data;
}
