import useDataStore from "~/stores/useDataStore"
import type { ApiAccount, ApiPost } from '~/types/types';

export default () => {
  const config = useRuntimeConfig()
  const { ids, timelinePosts, timelinePostsLoading, accountsLoading, keyword, accounts, communitySize, communitySizeLoading, posts, postsLoading, loading, error  } = storeToRefs(useDataStore())

  async function fetchIds() {
    try {
      const idsResponse = await $fetch<{ ids: string[] }>(
        `${config.public.apiBase}/grokathon/fetch-ids/?input_query=${encodeURIComponent(keyword.value)}`
      )

      if (idsResponse.ids) {
        ids.value = idsResponse.ids
      }
    } catch (err) {
      console.error('Error fetching ids:', err)
      error.value = 'No community found for this topic'
    } finally {

    }
  }

  async function fetchAccounts() {
    if (!ids.value || ids.value.length === 0) return;

    try {
      accountsLoading.value = true;
      const idsParams = ids.value?.slice(0, 100).map((id: string) => `ids=${id}`).join('&');
      const accountsResponse = await $fetch<{ accounts: ApiAccount[] }>(
        `${config.public.apiBase}/grokathon/fetch-accounts/?${idsParams}`
      )

      if (accountsResponse.accounts && accountsResponse.accounts.length > 0) {
        accounts.value = accountsResponse.accounts;
      }
    } catch (err) {
      error.value = 'Could not load accounts'
    } finally {
      accountsLoading.value = false;
    }
  }

  async function fetchSize() {
    if (!ids.value || ids.value.length === 0) return;

    try {
      communitySizeLoading.value = true;
      const idsParams = ids.value?.slice(0, 20).map((id: string) => `ids=${id}`).join('&');
      const sizeResponse = await $fetch<{ size: string }>(
        `${config.public.apiBase}/grokathon/fetch-grokathon-size/?${idsParams}`
      )

      if (sizeResponse.size) {
        communitySize.value = sizeResponse.size + '+'
      } else {
        communitySize.value = '--'
      }
    } catch (err) {
      console.error('No communitySize found')
    } finally {
      communitySizeLoading.value = false;
    } 
  }

  async function fetchTimelinePosts() {
    if (!ids.value || ids.value.length === 0) return;

    try {
      timelinePostsLoading.value = true;
      const idsParams = ids.value?.slice(0, 50).map((id: string) => `ids=${id}`).join('&');
      const postsResponse = await $fetch<{ posts: ApiPost[] }>(
        `${config.public.apiBase}/grokathon/fetch-posts-timeline/?${idsParams}`
      )
      
      if (postsResponse.posts && postsResponse.posts.length > 0) {
        timelinePosts.value = postsResponse.posts;
      }
    } catch (err) {

    } finally {
      timelinePostsLoading.value = false;
    }
  }

  async function fetchPosts() {
    if (!ids.value || ids.value.length === 0) return;

    try {
      postsLoading.value = true;
      const idsParams = ids.value?.slice(0, 50).map((id: string) => `ids=${id}`).join('&');
      const postsResponse = await $fetch<{ posts: ApiPost[] }>(
        `${config.public.apiBase}/grokathon/fetch-posts/?${idsParams}`
      )
      
      if (postsResponse.posts && postsResponse.posts.length > 0) {
        posts.value = postsResponse.posts;
      }
    } catch (err) {

    } finally {
      postsLoading.value = false;
    }
  }

  async function inferTopic() {
    $fetch<{ topic: string | null }>(
        `${config.public.apiBase}/grokathon/infer-topic-in-query/?input_query=${encodeURIComponent(keyword.value)}`
    )
  }

  return {
    fetchIds,
    fetchAccounts,
    fetchSize,
    fetchPosts,
    fetchTimelinePosts,
  }
}