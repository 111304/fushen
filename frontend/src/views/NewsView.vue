<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { NCard, NTag, NPagination, NSpace, NButton, NModal, NEmpty } from 'naive-ui'
import SectionTitle from '@/components/SectionTitle.vue'
import { useCompanyData } from '@/composables/useCompanyData'
import type { NewsItem, PageResult } from '@/types'

const { fetchNews } = useCompanyData()

const activeCategory = ref<string>('全部')
const currentPage = ref(1)
const pageSize = ref(9)
const total = ref(0)
const selectedNews = ref<NewsItem | null>(null)
const showModal = ref(false)

const pageResult = reactive<{ list: NewsItem[]; total: number }>({
  list: [],
  total: 0,
})

// 分类快照：进页面时拉一次大分页提取全部分类，之后筛选/翻页不再改变按钮数量与位置
const allCategories = ref<string[]>([])

const categories = computed(() => ['全部', ...allCategories.value])

async function loadData() {
  const cat = activeCategory.value === '全部' ? undefined : activeCategory.value
  const res: PageResult<NewsItem> = await fetchNews(currentPage.value, pageSize.value, cat)
  pageResult.list = res.list
  pageResult.total = res.total
  total.value = res.total
}

function handleCategoryChange(cat: string) {
  activeCategory.value = cat
  currentPage.value = 1
}

function handlePageChange(page: number) {
  currentPage.value = page
}

function handleNewsClick(item: NewsItem) {
  selectedNews.value = item
  showModal.value = true
}

// 拉一次大分页（当前数据量远小于 100 条），确保按钮包含所有分类
async function loadCategories() {
  const res: PageResult<NewsItem> = await fetchNews(1, 100)
  allCategories.value = Array.from(new Set(res.list.map((n) => n.category)))
}

onMounted(() => {
  loadData()
  loadCategories()
})

watch([activeCategory, currentPage], loadData)
</script>

<template>
  <!-- 页面横幅 -->
  <section class="page-banner">
    <div class="banner-overlay">
      <h1 class="banner-title">新闻动态</h1>
      <p class="banner-subtitle">了解星辰科技的最新资讯与行业洞察</p>
    </div>
  </section>

  <!-- 新闻列表 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="最新动态" subtitle="公司新闻、产品发布与行业观点" center />

      <!-- 分类筛选 -->
      <div class="filter-bar">
        <NSpace>
          <NButton
            v-for="cat in categories"
            :key="cat"
            :type="activeCategory === cat ? 'primary' : 'default'"
            size="small"
            @click="handleCategoryChange(cat)"
          >
            {{ cat }}
          </NButton>
        </NSpace>
      </div>

      <!-- 新闻列表 -->
      <div v-if="pageResult.list.length > 0" class="news-list">
        <NCard
          v-for="item in pageResult.list"
          :key="item.id"
          class="news-item"
          hoverable
          @click="handleNewsClick(item)"
        >
          <div class="news-item-inner">
            <img :src="item.cover_url" :alt="item.title" class="news-cover" />
            <div class="news-content">
              <NSpace align="center" :size="8">
                <NTag size="small" type="info" :bordered="false">{{ item.category }}</NTag>
                <span class="news-date">{{ item.published_at }}</span>
                <span class="news-author">{{ item.author }}</span>
              </NSpace>
              <h3 class="news-title">{{ item.title }}</h3>
              <p class="news-summary">{{ item.summary }}</p>
              <NButton text type="primary">阅读全文 →</NButton>
            </div>
          </div>
        </NCard>
      </div>

      <NEmpty v-else description="暂无新闻" style="padding: 60px 0" />

      <!-- 分页 -->
      <div v-if="total > pageSize" class="pagination">
        <NPagination
          v-model:page="currentPage"
          :page-count="Math.ceil(total / pageSize)"
          :page-size="pageSize"
          show-quick-jumper
          @update:page="handlePageChange"
        />
      </div>
    </div>
  </section>

  <!-- 新闻详情弹窗 -->
  <NModal v-model:show="showModal" preset="card" style="width: 700px" :title="selectedNews?.title">
    <template v-if="selectedNews">
      <img :src="selectedNews.cover_url" :alt="selectedNews.title" class="modal-img" />
      <div class="modal-meta">
        <NTag size="small" type="info" :bordered="false">{{ selectedNews.category }}</NTag>
        <span class="news-date">{{ selectedNews.published_at }}</span>
        <span class="news-author">作者：{{ selectedNews.author }}</span>
      </div>
      <p class="modal-summary">{{ selectedNews.summary }}</p>
      <div v-if="selectedNews.content" class="modal-content" v-html="selectedNews.content" />
      <p v-else class="modal-content">详细内容请关注官方公众号获取完整报道。</p>
    </template>
  </NModal>
</template>

<style scoped>
.page-banner {
  height: 280px;
  background: linear-gradient(135deg, #1a1a2e, #2d8cf0);
  display: flex;
  align-items: center;
  justify-content: center;
}

.banner-overlay {
  text-align: center;
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

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

.filter-bar {
  text-align: center;
  margin-bottom: 40px;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.news-item {
  cursor: pointer;
}

.news-item-inner {
  display: flex;
  gap: 20px;
}

.news-cover {
  width: 200px;
  height: 140px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.news-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.news-date {
  font-size: 13px;
  color: #aaa;
}

.news-author {
  font-size: 13px;
  color: #aaa;
}

.news-title {
  font-size: 18px;
  font-weight: 600;
  margin: 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.news-summary {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}

/* 弹窗 */
.modal-img {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.modal-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.modal-summary {
  font-size: 16px;
  color: #333;
  line-height: 1.8;
  margin-bottom: 16px;
  font-weight: 500;
}

.modal-content {
  font-size: 15px;
  color: #555;
  line-height: 2;
}

@media (max-width: 768px) {
  .news-item-inner {
    flex-direction: column;
  }

  .news-cover {
    width: 100%;
    height: 180px;
  }
}
</style>
