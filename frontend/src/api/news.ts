import { get } from './request'
import type { NewsItem, PageResult } from '@/types'

/** 获取新闻列表（分页） */
export function getNewsList(params: { page: number; page_size: number; category?: string }) {
  return get<PageResult<NewsItem>>('/news', params as Record<string, unknown>)
}

/** 获取新闻详情 */
export function getNewsDetail(id: number) {
  return get<NewsItem>(`/news/${id}`)
}
