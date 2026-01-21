export interface ApiAccount {
  id: string
  username: string
  name: string
  description: string
  profile_image_url: string
  verified: boolean
  public_metrics: {
    followers_count: number
    following_count: number
    tweet_count: number
  }
}

export interface ApiPost {
  post: {
    id: string
    text: string
    created_at: string
    account_id: string
    retweet_count: number | null
    reply_count: number | null
    like_count: number | null
    impression_count: number | null
    media: Array<{ url?: string; preview_image_url?: string; type?: string }> | null
  }
  account: {
    id: string
    username: string
    name: string
    verified: boolean | null
    profile_image_url: string | null
  }
}