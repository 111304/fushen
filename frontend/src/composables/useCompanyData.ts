import { ref } from 'vue'
import type { CompanyInfo, Product, NewsItem, TeamMember } from '@/types'
import { getCompanyInfo, getTeamMembers } from '@/api/company'
import { getProducts } from '@/api/product'
import { getNewsList } from '@/api/news'

/** 默认公司信息（后端未启动时兜底） */
const defaultCompany: CompanyInfo = {
  id: 1,
  name: '星辰科技',
  slogan: '让AI驱动未来',
  description:
    '星辰科技成立于2018年，是一家专注于人工智能与云计算的高新技术企业。我们致力于为企业提供从AI算法、云原生架构到数字化转型咨询的全链路解决方案，已服务超过500家企业客户。',
  logo_url: '/favicon.svg',
  address: '北京市海淀区中关村科技园',
  phone: '010-8888-6666',
  email: 'contact@stellartech.com',
  founded_year: 2018,
  banner_url: 'https://picsum.photos/seed/stellar-hero/1920/600',
  about_image_url: 'https://picsum.photos/seed/stellar-about/600/400',
}

/** 默认产品数据 */
const defaultProducts: Product[] = [
  {
    id: 1,
    name: '星辰AI平台',
    description: '一站式AI模型训练与部署平台，支持从数据标注到模型上线的全流程管理。',
    image_url: 'https://picsum.photos/seed/product-1/400/300',
    category: 'AI平台',
    features: ['模型训练', '自动标注', '在线推理', '模型版本管理'],
    sort_order: 1,
  },
  {
    id: 2,
    name: '云原生架构服务',
    description: '基于Kubernetes的微服务架构设计与实施，助力企业应用现代化改造。',
    image_url: 'https://picsum.photos/seed/product-2/400/300',
    category: '云计算',
    features: ['微服务设计', '容器编排', 'CI/CD流水线', '可观测性'],
    sort_order: 2,
  },
  {
    id: 3,
    name: '智能数据分析',
    description: '基于大数据的实时分析平台，提供可视化看板与智能决策支持。',
    image_url: 'https://picsum.photos/seed/product-3/400/300',
    category: '数据分析',
    features: ['实时计算', '可视化看板', '智能预警', '多维分析'],
    sort_order: 3,
  },
  {
    id: 4,
    name: '数字化咨询',
    description: '资深专家团队提供数字化转型战略规划与落地实施咨询服务。',
    image_url: 'https://picsum.photos/seed/product-4/400/300',
    category: '咨询服务',
    features: ['战略规划', '技术选型', '架构评审', '实施指导'],
    sort_order: 4,
  },
]

/** 默认新闻数据 */
const defaultNews: NewsItem[] = [
  {
    id: 1,
    title: '星辰科技完成B轮融资，加速AI产品研发',
    summary: '本轮融资将用于加大AI核心技术研发投入，扩大市场份额。',
    content: '',
    cover_url: 'https://picsum.photos/seed/news-1/400/250',
    category: '公司动态',
    author: '市场部',
    published_at: '2025-07-15',
  },
  {
    id: 2,
    title: '星辰AI平台3.0版本正式发布',
    summary: '全新版本支持大模型微调与多模态推理，性能提升200%。',
    content: '',
    cover_url: 'https://picsum.photos/seed/news-2/400/250',
    category: '产品发布',
    author: '产品部',
    published_at: '2025-06-28',
  },
  {
    id: 3,
    title: '与某头部企业签署战略合作协议',
    summary: '双方将在AI+工业领域展开深度合作，共建智能工厂。',
    content: '',
    cover_url: 'https://picsum.photos/seed/news-3/400/250',
    category: '合作动态',
    author: '商务部',
    published_at: '2025-05-10',
  },
]

/** 默认团队数据 */
const defaultTeam: TeamMember[] = [
  {
    id: 1,
    name: '张明',
    title: 'CEO & 创始人',
    avatar_url: 'https://picsum.photos/seed/team-1/200/200',
    bio: '清华大学计算机博士，曾任某头部互联网公司技术VP，15年AI领域经验。',
  },
  {
    id: 2,
    name: '李华',
    title: 'CTO',
    avatar_url: 'https://picsum.photos/seed/team-2/200/200',
    bio: '前Google资深工程师，云原生架构专家，主导多个大型分布式系统设计。',
  },
  {
    id: 3,
    name: '王芳',
    title: '产品VP',
    avatar_url: 'https://picsum.photos/seed/team-3/200/200',
    bio: '10年企业级产品经验，擅长AI产品化与商业化落地。',
  },
  {
    id: 4,
    name: '赵强',
    title: '数据科学家',
    avatar_url: 'https://picsum.photos/seed/team-4/200/200',
    bio: 'MIT统计学硕士，Kaggle Grandmaster，专注机器学习与大数据分析。',
  },
]

/** 公司数据 composable */
export function useCompanyData() {
  const company = ref<CompanyInfo>(defaultCompany)
  const team = ref<TeamMember[]>(defaultTeam)
  const products = ref<Product[]>(defaultProducts)
  const news = ref<NewsItem[]>(defaultNews)
  const loading = ref(false)

  async function fetchCompany() {
    try {
      company.value = await getCompanyInfo()
    } catch {
      company.value = defaultCompany
    }
  }

  async function fetchTeam() {
    try {
      team.value = await getTeamMembers()
    } catch {
      team.value = defaultTeam
    }
  }

  async function fetchProducts(category?: string) {
    loading.value = true
    try {
      products.value = await getProducts(category)
    } catch {
      products.value = category
        ? defaultProducts.filter((p) => p.category === category)
        : defaultProducts
    } finally {
      loading.value = false
    }
  }

  async function fetchNews(page = 1, pageSize = 10, category?: string) {
    try {
      const res = await getNewsList({ page, page_size: pageSize, category })
      news.value = res.list
      return res
    } catch {
      const filtered = category
        ? defaultNews.filter((n) => n.category === category)
        : defaultNews
      news.value = filtered
      return { list: filtered, total: filtered.length, page, page_size: pageSize }
    }
  }

  return {
    company,
    team,
    products,
    news,
    loading,
    fetchCompany,
    fetchTeam,
    fetchProducts,
    fetchNews,
  }
}
