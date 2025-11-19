import {getProfile} from '@/shared/api/profile'
import {toProfileResponse} from './adapters'
import { useQuery } from "@tanstack/react-query";

export function useProfileData(){
  return useQuery({
    queryKey: ["profile"],
    queryFn: () =>
      getProfile(),
    select: toProfileResponse,
  });   
}