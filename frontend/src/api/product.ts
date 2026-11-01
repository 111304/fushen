import { get } from './request'
import type { Product } from '@/types'

/** 获取产品列表 */
export function getProducts(category?: string) {
  return get<Product[]>('/products', category ? { category } : undefined)
}

/** 获取产品详情 */
export function getProductDetail(id: number) {
  return get<Product>(`/products/${id}`)
}
