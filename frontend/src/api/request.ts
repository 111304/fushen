import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
})

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('[Request Error]', (error as Error).message)
    return Promise.reject(error)
  },
)

/**
 * 统一 GET 请求
 * 注意：后端接口直接返回业务数据本身（对象/数组/分页对象），
 * 不做 {code, message, data} 包裹，因此这里直接返回响应体，不再解包 .data
 */
export async function get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  return (await request.get(url, { params })) as unknown as T
}

/** 统一 POST 请求（同上，直接返回响应体） */
export async function post<T>(url: string, data?: Record<string, unknown>): Promise<T> {
  return (await request.post(url, data)) as unknown as T
}
