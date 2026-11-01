import { post } from './request'
import type { ContactForm } from '@/types'

/** 提交联系表单 */
export function submitContact(form: ContactForm) {
  return post<void>('/contact', form as unknown as Record<string, unknown>)
}
