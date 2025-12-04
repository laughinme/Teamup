import { useInfiniteQuery, type InfiniteData } from "@tanstack/react-query";
import { getProfilesList, type ProfileListDto } from "@/shared/api/profile";
import { toProfileListResponse } from "./adapters";
import type { ProfileListResponse } from "./types";

export function useProfilesList(limit = 20) {
    const queryKey = ["profiles", limit] as const;

    const query = useInfiniteQuery<ProfileListDto, Error, InfiniteData<ProfileListDto, string | null>, typeof queryKey, string | null>({
        queryKey,
        queryFn: ({ pageParam }) => getProfilesList(pageParam, limit),
        initialPageParam: null,
        getNextPageParam: (lastPage) => lastPage.next_cursor ?? undefined,
    });

    const pages: ProfileListResponse[] = (query.data?.pages ?? []).map(toProfileListResponse);
    const items = pages.flatMap((page) => page.items);

    return { ...query, pages, items };
}
