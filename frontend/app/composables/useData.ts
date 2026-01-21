import useDataStore from "~/stores/useDataStore"
import type { ApiAccount } from '~/types/types';

export default () => {
  const config = useRuntimeConfig()
  const { ids, keyword, accounts } = storeToRefs(useDataStore())

  async function fetchIds() {
    const idsResponse = await $fetch<{ ids: string[] }>(
          `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword.value)}`
    )

    if (idsResponse.ids) {
      ids.value = idsResponse.ids
    }
  }

  async function fetchAccounts() {
    if (!ids.value || ids.value.length === 0) return;

    const idsParams = ids.value?.slice(0, 50).map((id: string) => `ids=${id}`).join('&');
    const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
      `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
    )

    if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
      accounts.value = accountsResponse.accounts;
    }
  }

  return {
    fetchIds,
    fetchAccounts,
  }
}