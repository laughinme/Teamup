
export type ProfileResponse = {
    id: string;
    direction: string;
    bio: string | null;
    experienceLevel: string;
    achievements: string | null;
    timezone: string | null;
    visibility: string;
    techStack: TechStack[];
}

export type TechStack = {
    tag:{
        id: string;
        name: string;
        slug: string;
        kind: string;
    };
    level: number;
};