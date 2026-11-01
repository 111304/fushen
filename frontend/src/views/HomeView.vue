<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  NButton,
  NGrid,
  NGi,
  NCard,
  NStatistic,
  NSpace,
  NTag,
} from 'naive-ui'
import SectionTitle from '@/components/SectionTitle.vue'
import { useCompanyData } from '@/composables/useCompanyData'

const router = useRouter()
const { company, products, news, fetchCompany, fetchProducts, fetchNews } = useCompanyData()

const stats = ref([
  { label: '服务客户', value: 500, suffix: '+' },
  { label: '团队成员', value: 200, suffix: '+' },
  { label: '技术专利', value: 80, suffix: '+' },
  { label: '行业经验', value: 7, suffix: '年' },
])

const advantages = ref([
  {
    icon: '🤖',
    title: 'AI技术领先',
    desc: '自研AI算法引擎，多项核心技术获得国家发明专利',
  },
  {
    icon: '☁️',
    title: '云原生架构',
    desc: '基于Kubernetes的弹性架构，支持百万级并发',
  },
  {
    icon: '📊',
    title: '数据驱动',
    desc: '实时数据分析平台，让每一个决策都有据可依',
  },
  {
    icon: '🛡️',
    title: '安全可靠',
    desc: '通过等保三级认证，全方位保障数据安全',
  },
])

const latestNews = computed(() => news.value.slice(0, 3))

onMounted(async () => {
  await Promise.all([fetchCompany(), fetchProducts(), fetchNews(1, 3)])
})
</script>

<template>
  <!-- Hero Banner -->
  <section class="hero" :style="{ backgroundImage: `url(${company.banner_url})` }">
    <div class="hero-overlay">
      <div class="hero-content">
        <h1 class="hero-title">{{ company.slogan }}</h1>
        <p class="hero-desc">{{ company.description }}</p>
        <NSpace>
          <NButton type="primary" size="large" @click="router.push('/products')">
            了解产品
          </NButton>
          <NButton size="large" ghost class="hero-contact-btn" @click="router.push('/contact')">
            联系我们
          </NButton>
        </NSpace>
      </div>
    </div>
  </section>

  <!-- 公司简介 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="关于星辰科技" subtitle="专注AI与云计算，赋能企业数字化转型" center />
      <div class="intro-grid">
        <div class="intro-text">
          <p>{{ company.description }}</p>
          <p>
            自{{ company.founded_year }}年成立以来，我们始终坚持以技术创新为核心驱动力，
            为企业提供从战略咨询到技术落地的全链路服务。目前团队规模超过200人，
            核心成员来自国内外顶尖科技企业与研究机构。
          </p>
          <NButton type="primary" ghost @click="router.push('/about')">查看更多 →</NButton>
        </div>
        <div class="intro-image">
          <img :src="company.about_image_url" alt="关于我们" />
        </div>
      </div>
    </div>
  </section>

  <!-- 核心优势 -->
  <section class="section section-gray">
    <div class="container">
      <SectionTitle title="核心优势" subtitle="为什么选择星辰科技" center />
      <NGrid :cols="4" :x-gap="24" :y-gap="24" responsive="screen">
        <NGi v-for="item in advantages" :key="item.title" span="1">
          <NCard class="advantage-card" hoverable>
            <div class="advantage-icon">{{ item.icon }}</div>
            <h3 class="advantage-title">{{ item.title }}</h3>
            <p class="advantage-desc">{{ item.desc }}</p>
          </NCard>
        </NGi>
      </NGrid>
    </div>
  </section>

  <!-- 数据统计 -->
  <section class="section section-dark">
    <div class="container">
      <NGrid :cols="2" :x-gap="24" :y-gap="24" responsive="screen">
        <NGi v-for="stat in stats" :key="stat.label" span="1">
          <div class="stat-item">
            <NStatistic :value="stat.value" tabular-nums>
              <template #label>
                <span class="stat-label">{{ stat.label }} </span>
              </template>
              <template #suffix>
                <span class="stat-suffix">{{ stat.suffix }} </span>
              </template>
            </NStatistic>
          </div>
        </NGi>
      </NGrid>
    </div>
  </section>

  <!-- 产品概览 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="产品与服务" subtitle="为企业提供全方位技术解决方案" center />
      <NGrid :cols="4" :x-gap="24" :y-gap="24" responsive="screen">
        <NGi v-for="product in products.slice(0, 4)" :key="product.id" span="1">
          <NCard class="product-card" hoverable @click="router.push('/products')">
            <img :src="product.image_url" :alt="product.name" class="product-img" />
            <div class="product-body">
              <NTag size="small" type="info" :bordered="false">{{ product.category }}</NTag>
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-desc">{{ product.description }}</p>
            </div>
          </NCard>
        </NGi>
      </NGrid>
      <div class="section-more">
        <NButton type="primary" ghost @click="router.push('/products')">查看全部产品</NButton>
      </div>
    </div>
  </section>

  <!-- 最新动态 -->
  <section class="section section-gray">
    <div class="container">
      <SectionTitle title="最新动态" subtitle="了解星辰科技的最新资讯" center />
      <NGrid :cols="3" :x-gap="24" :y-gap="24" responsive="screen">
        <NGi v-for="item in latestNews" :key="item.id" span="1">
          <NCard class="news-card" hoverable @click="router.push('/news')">
            <img :src="item.cover_url" :alt="item.title" class="news-img" />
            <div class="news-body">
              <NTag size="small" :bordered="false">{{ item.category }}</NTag>
              <h3 class="news-title">{{ item.title }}</h3>
              <p class="news-summary">{{ item.summary }}</p>
              <span class="news-date">{{ item.published_at }}</span>
            </div>
          </NCard>
        </NGi>
      </NGrid>
    </div>
  </section>
</template>

<style scoped>
.hero {
  height: 520px;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
}

.hero-overlay {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.85), rgba(45, 140, 240, 0.6));
  display: flex;
  align-items: center;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  width: 100%;
  color: #fff;
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  margin-bottom: 16px;
}

.hero-desc {
  font-size: 18px;
  line-height: 1.8;
  max-width: 640px;
  margin-bottom: 32px;
  opacity: 0.95;
}



/* 副按钮：改成白描边幽灵按钮，不再是主题色描边 */
.hero-content :deep(.hero-contact-btn) {
  color: #ffffff;
  border: 1px solid rgba(49, 124, 230, 0.68);
  /* border-radius: 8px; */
  font-weight: 500;
  padding: 0 28px;
  background: rgba(255, 255, 255, 0.08);
}


/* .hero-contact-btn :deep(.n-button__border) {
  border: 1px solid #1bbc20;
} */

.section {
  padding: 80px 0;
}

.section-gray {
  background: #f5f7fa;
}

.section-dark {
  background: #538bc6;
  padding: 60px 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 公司简介 */
.intro-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 48px;
  align-items: center;
}

.intro-text p {
  font-size: 16px;
  line-height: 2;
  color: #555;
  margin-bottom: 16px;
}

.intro-image img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

/* 核心优势 */
.advantage-card {
  text-align: center;
  height: 100%;
}

.advantage-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.advantage-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.advantage-desc {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
}


/* 数据统计 */
.section-dark {
  background: #ffffff;
  padding: 72px 0;
}

.stat-item {
  background: #f0f7ff;
  border-radius: 16px;
  padding: 48px 20px;
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-label {
  color: #64748b;
  font-size: 15px;
  letter-spacing: 2px;
  margin-bottom: 16px;
  line-height: 1;
}

.stat-item :deep(.n-statistic) {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-item :deep(.n-statistic-value) {
  color: #2d8cf0 !important;
  font-size: 48px !important;
  font-weight: 800;
  line-height: 1;
}

.stat-item :deep(.n-statistic-value__suffix) {
  color: rgba(45, 140, 240, 0.7) !important;
  font-size: 22px !important;
  font-weight: 600;
  margin-left: 4px;
}



/* 产品卡片 */
.product-card {
  cursor: pointer;
  overflow: hidden;
  height: 100%;
}

.product-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.product-body {
  padding: 4px 0;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  margin: 8px 0;
}

.product-desc {
  font-size: 13px;
  color: #888;
  line-height: 1.6;
}

/* 新闻卡片 */
.news-card {
  cursor: pointer;
  overflow: hidden;
  height: 100%;
}

.news-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.news-title {
  font-size: 16px;
  font-weight: 600;
  margin: 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-summary {
  font-size: 13px;
  color: #888;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-date {
  font-size: 12px;
  color: #aaa;
}

.section-more {
  text-align: center;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 28px;
  }

  .hero-desc {
    font-size: 15px;
  }

  .intro-grid {
    grid-template-columns: 1fr;
  }
}
</style>
