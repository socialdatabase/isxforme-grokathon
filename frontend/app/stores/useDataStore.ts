import type { ApiAccount } from "~/types/types";

const STORE_KEY = 'useDataStore';

export default defineStore(STORE_KEY, () => {
  const ids = ref<string[]>();
  const inferredTopic = ref<string>();
  const accounts = ref<ApiAccount[]>();
  const keyword = ref<string>('');

  return {
    ids,
    inferredTopic,
    accounts,
    keyword,
  }
});