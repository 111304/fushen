/** 公司信息 */
export interface CompanyInfo {
  id: number
  name: string
  slogan: string
  description: string
  logo_url: string
  address: string
  phone: string
  email: string
  founded_year: number
  banner_url: string
  about_image_url: string
}

/** 产品服务 */
export interface Product {
  id: number
  name: string
  description: string
  image_url: string
  category: string
  features: string[]
  sort_order: number
}

/** 新闻动态 */
export interface NewsItem {
  id: number
  title: string
  summary: string
  content: string
  cover_url: string
  category: string
  author: string
  published_at: string
}

/** 团队成员 */
export interface TeamMember {
  id: number
  name: string
  title: string
  avatar_url: string
  bio: string
}

/** 联系表单 */
export interface ContactForm {
  name: string
  email: string
  phone: string
  subject: string
  message: string
}

/** 统一 API 响应 */
export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

/** 分页响应 */
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  page_size: number
}
