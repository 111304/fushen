<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { NCard, NGrid, NGi, NTag, NButton, NSpace, NModal } from 'naive-ui'
import SectionTitle from '@/components/SectionTitle.vue'
import { useCompanyData } from '@/composables/useCompanyData'
import type { Product } from '@/types'

const { products, loading, fetchProducts } = useCompanyData()

const activeCategory = ref<string>('全部')
const selectedProduct = ref<Product | null>(null)
const showModal = ref(false)

// 分类快照：首次全量加载时提取一次，之后筛选只影响卡片列表，按钮数量与位置保持不变
const allCategories = ref<string[]>([])

const categories = computed(() => ['全部', ...allCategories.value])

const filteredProducts = computed(() => {
  if (activeCategory.value === '全部') return products.value
  return products.value.filter((p) => p.category === activeCategory.value)
})

function handleCategoryChange(cat: string) {
  activeCategory.value = cat
}

function handleProductClick(product: Product) {
  selectedProduct.value = product
  showModal.value = true
}

// 全量加载产品，并同步刷新分类快照
async function loadAll() {
  await fetchProducts()
  allCategories.value = Array.from(new Set(products.value.map((p) => p.category)))
}

onMounted(() => loadAll())

watch(activeCategory, (cat) => {
  if (cat === '全部') {
    loadAll()
  } else {
    fetchProducts(cat)
  }
})
</script>

<template>
  <!-- 页面横幅 -->
  <section class="page-banner">
    <div class="banner-overlay">
      <h1 class="banner-title">产品与服务</h1>
      <p class="banner-subtitle">为企业数字化转型提供全方位技术解决方案</p>
    </div>
  </section>

  <!-- 产品列表 -->
  <section class="section">
    <div class="container">
      <SectionTitle title="我们的产品" subtitle="覆盖AI、云计算、数据分析与咨询服务" center />

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

      <!-- 产品网格 -->
      <NGrid :cols="3" :x-gap="24" :y-gap="32" responsive="screen">
        <NGi v-for="product in filteredProducts" :key="product.id" span="1">
          <NCard class="product-card" hoverable @click="handleProductClick(product)">
            <img :src="product.image_url" :alt="product.name" class="product-img" />
            <div class="product-body">
              <div class="product-header">
                <NTag size="small" type="info" :bordered="false">{{ product.category }}</NTag>
              </div>
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-desc">{{ product.description }}</p>
              <div class="product-features">
                <NTag
                  v-for="feat in product.features"
                  :key="feat"
                  size="small"
                  :bordered="false"
                  round
                >
                  {{ feat }}
                </NTag>
              </div>
            </div>
          </NCard>
        </NGi>
      </NGrid>

      <div v-if="!loading && filteredProducts.length === 0" class="empty-state">
        暂无相关产品
      </div>
    </div>
  </section>

  <!-- 产品详情弹窗 -->
  <NModal v-model:show="showModal" preset="card" style="width: 600px" :title="selectedProduct?.name">
    <template v-if="selectedProduct">
      <img :src="selectedProduct.image_url" :alt="selectedProduct.name" class="modal-img" />
      <div class="modal-body">
        <NSpace align="center" :size="8" style="margin-bottom: 12px">
          <NTag type="info" :bordered="false">{{ selectedProduct.category }}</NTag>
        </NSpace>
        <p class="modal-desc">{{ selectedProduct.description }}</p>
        <h4 class="modal-features-title">核心功能</h4>
        <div class="modal-features">
          <NTag
            v-for="feat in selectedProduct.features"
            :key="feat"
            type="success"
            :bordered="false"
            round
          >
            {{ feat }}
          </NTag>
        </div>
      </div>
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.filter-bar {
  text-align: center;
  margin-bottom: 40px;
}

.product-card {
  cursor: pointer;
  overflow: hidden;
  height: 100%;
}

.product-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.product-body {
  padding: 4px 0;
}

.product-header {
  margin-bottom: 8px;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.product-desc {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-features {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #999;
  font-size: 16px;
}

/* 弹窗 */
.modal-img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.modal-desc {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
  margin-bottom: 16px;
}

.modal-features-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
}

.modal-features {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
