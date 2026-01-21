import type { ApiAccount, ApiPost } from "~/types/types";

const STORE_KEY = 'useDataStore';

export default defineStore(STORE_KEY, () => {
  const ids = ref<string[]>();
  
  const loading = ref<boolean>(false);
  const error = ref<string | null>(null)

  const inferredTopic = ref<string>();
  
  const accountsLoading = ref<boolean>(false);
  const accounts = ref<ApiAccount[]>();
  
  const keyword = ref<string>('');
  
  const communitySize = ref<string>('--')
  const communitySizeLoading = ref<boolean>(false);

  const posts = ref<ApiPost[]>();
  const postsLoading = ref<boolean>(false);

  return {
    ids,
    inferredTopic,
    accounts,
    keyword,
    communitySize,
    communitySizeLoading,
    posts,
    postsLoading,
    loading, 
    error,
    accountsLoading,
  }
});