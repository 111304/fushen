<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NGrid, NGi, NSpace, NAvatar } from 'naive-ui'
import SectionTitle from '@/components/SectionTitle.vue'
import { useCompanyData } from '@/composables/useCompanyData'

const { company, team, fetchCompany, fetchTeam } = useCompanyData()

const milestones = ref([
  { year: '2018', event: '星辰科技成立，入驻中关村科技园' },
  { year: '2019', event: '发布首款AI数据分析产品，获得首批企业客户' },
  { year: '2020', event: '完成A轮融资，团队扩展至50人' },
  { year: '2021', event: '推出星辰AI平台1.0，服务客户突破100家' },
  { year: '2022', event: '通过国家高新技术企业认证，获多项技术专利' },
  { year: '2023', event: '云原生架构服务上线，签约头部制造业客户' },
  { year: '2024', event: 'AI平台3.0发布，支持大模型微调与多模态推理' },
  { year: '2025', event: '完成B轮融资，加速核心技术研发与市场拓展' },
])

const values = ref([
  { icon: '🎯', title: '使命', desc: '用AI技术驱动企业创新与增长' },
  { icon: '🌟', title: '愿景', desc: '成为最受信赖的企业级AI解决方案提供商' },
  { icon: '💎', title: '价值观', desc: '客户第一、技术驱动、诚信务实、协作共赢' },
])

onMounted(async () => {
  await Promise.all([fetchCompany(), fetchTeam()])
})
</script>

<template>
  <!-- 页面横幅 -->
  <section
    class="page-banner"
    :style="{ backgroundImage: `url(${company.about_image_url})` }"
  >
    <div class="banner-overlay">
      <h1 class="banner-title">关于我们</h1>
      <p class="banner-subtitle">{{ company.slogan }} · {{ company.name }}</p>
    </div>
  </section>

  <!-- 公司简介 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="公司简介" subtitle="了解星辰科技的发展历程" />
      <div class="about-grid">
        <div class="about-text">
          <p>{{ company.description }}</p>
          <p>
            {{ company.name }}成立于{{ company.founded_year }}年，总部位于{{ company.address }}。
            作为一家高新技术企业，我们拥有超过200名员工，其中研发团队占比超过70%。
            公司专注于人工智能、云计算和大数据三大核心技术方向，
            为金融、制造、零售、医疗等多个行业提供深度的数字化转型解决方案。
          </p>
          <NSpace vertical :size="12">
            <div class="info-row">
              <span class="info-label">公司全称：</span>
              <span>{{ company.name }}科技有限公司</span>
            </div>
            <div class="info-row">
              <span class="info-label">成立时间：</span>
              <span>{{ company.founded_year }}年</span>
            </div>
            <div class="info-row">
              <span class="info-label">总部地址：</span>
              <span>{{ company.address }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">联系电话：</span>
              <span>{{ company.phone }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">企业邮箱：</span>
              <span>{{ company.email }}</span>
            </div>
          </NSpace>
        </div>
        <div class="about-image">
          <img :src="company.about_image_url" alt="公司环境" />
        </div>
      </div>
    </div>
  </section>

  <!-- 使命愿景 -->
  <section class="section section-gray">
    <div class="container">
      <SectionTitle title="使命与愿景" subtitle="我们为什么而存在" center />
      <NGrid :cols="3" :x-gap="24" responsive="screen">
        <NGi v-for="item in values" :key="item.title" span="1">
          <div class="value-card">
            <div class="value-icon">{{ item.icon }}</div>
            <h3 class="value-title">{{ item.title }}</h3>
            <p class="value-desc">{{ item.desc }}</p>
          </div>
        </NGi>
      </NGrid>
    </div>
  </section>

  <!-- 发展历程 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="发展历程" subtitle="一路走来的重要里程碑" center />
      <div class="timeline">
        <div v-for="(item, idx) in milestones" :key="idx" class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <span class="timeline-year">{{ item.year }}</span>
            <p class="timeline-event">{{ item.event }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- 核心团队 -->
  <section class="section section-gray">
    <div class="container">
      <SectionTitle title="核心团队" subtitle="来自顶尖企业与研究机构的行业专家" center />
      <NGrid :cols="4" :x-gap="24" :y-gap="24" responsive="screen">
        <NGi v-for="member in team" :key="member.id" span="1">
          <NCard class="team-card" hoverable>
            <div class="team-avatar">
              <NAvatar :size="100" :src="member.avatar_url" round />
            </div>
            <h3 class="team-name">{{ member.name }}</h3>
            <p class="team-title">{{ member.title }}</p>
            <p class="team-bio">{{ member.bio }}</p>
          </NCard>
        </NGi>
      </NGrid>
    </div>
  </section>
</template>

<style scoped>
.page-banner {
  height: 320px;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner-overlay {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(45, 140, 240, 0.5));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.banner-title {
  font-size: 36px;
  font-weight: 700;
}

.banner-subtitle {
  font-size: 16px;
  opacity: 0.9;
  margin-top: 8px;
}

.section {
  padding: 80px 0;
}

.section-gray {
  background: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* 公司简介 */
.about-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 48px;
  align-items: start;
}

.about-text p {
  font-size: 16px;
  line-height: 2;
  color: #555;
  margin-bottom: 20px;
}

.info-row {
  font-size: 15px;
  color: #555;
}

.info-label {
  font-weight: 600;
  color: #333;
}

.about-image img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

/* 使命愿景 */
.value-card {
  text-align: center;
  padding: 32px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  height: 100%;
}

.value-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.value-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #2d8cf0;
}

.value-desc {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
}

/* 发展历程 */
.timeline {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  padding-left: 32px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #2d8cf0, #5cadff);
}

.timeline-item {
  position: relative;
  margin-bottom: 32px;
}

.timeline-dot {
  position: absolute;
  left: -32px;
  top: 4px;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #2d8cf0;
  border: 3px solid #fff;
  box-shadow: 0 0 0 2px #2d8cf0;
}

.timeline-year {
  font-size: 18px;
  font-weight: 700;
  color: #2d8cf0;
}

.timeline-event {
  font-size: 15px;
  color: #555;
  margin-top: 4px;
  line-height: 1.6;
}

/* 团队 */
.team-card {
  text-align: center;
  height: 100%;
}

.team-avatar {
  margin-bottom: 16px;
}

.team-name {
  font-size: 18px;
  font-weight: 600;
}

.team-title {
  font-size: 14px;
  color: #2d8cf0;
  margin: 4px 0 12px;
}

.team-bio {
  font-size: 13px;
  color: #888;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .about-grid {
    grid-template-columns: 1fr;
  }
}
</style>
