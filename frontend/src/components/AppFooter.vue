<script setup lang="ts">
import { NSpace } from 'naive-ui'

const year = new Date().getFullYear()

const quickLinks = [
  { label: '首页', path: '/' },
  { label: '关于我们', path: '/about' },
  { label: '产品服务', path: '/products' },
  { label: '新闻动态', path: '/news' },
  { label: '联系我们', path: '/contact' },
]
</script>

<template>
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-col">
        <h4 class="footer-title">星辰科技</h4>
        <p class="footer-desc">让AI驱动未来，为企业数字化转型提供全方位解决方案</p>
      </div>

      <div class="footer-col">
        <h4 class="footer-title">快速导航</h4>
        <NSpace vertical :size="8">
          <RouterLink
            v-for="link in quickLinks"
            :key="link.path"
            :to="link.path"
            class="footer-link"
          >
            {{ link.label }}
          </RouterLink>
        </NSpace>
      </div>

      <div class="footer-col">
        <h4 class="footer-title">联系方式</h4>
        <NSpace vertical :size="8">
          <span>地址：北京市海淀区中关村科技园</span>
          <span>电话：010-8888-6666</span>
          <span>邮箱：contact@stellartech.com</span>
        </NSpace>
      </div>
    </div>

    <div class="footer-copyright">
      © {{ year }} 星辰科技 StellarTech. 保留所有权利.
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #1a1a2e;
  color: #ccc;
  padding: 48px 24px 0;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr;
  gap: 48px;
  padding-bottom: 32px;
}

.footer-title {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 16px;
}

.footer-desc {
  font-size: 14px;
  line-height: 1.8;
  color: #999;
}

.footer-link {
  font-size: 14px;
  color: #999;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #2d8cf0;
}

.footer-copyright {
  text-align: center;
  padding: 16px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 13px;
  color: #666;
}

@media (max-width: 768px) {
  .footer-inner {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>
