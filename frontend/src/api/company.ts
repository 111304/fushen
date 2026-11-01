import { get } from './request'
import type { CompanyInfo, TeamMember } from '@/types'

/** 获取公司信息 */
export function getCompanyInfo() {
  return get<CompanyInfo>('/company/info')
}

/** 获取团队成员列表 */
export function getTeamMembers() {
  return get<TeamMember[]>('/company/team')
}
