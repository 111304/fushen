<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { NLayoutHeader, NMenu, NButton, NDrawer, NDrawerContent } from 'naive-ui'
import type { MenuOption } from 'naive-ui'

const router = useRouter()
const route = useRoute()
const mobileDrawer = ref(false)

const menuOptions: MenuOption[] = [
  { label: '首页', key: 'Home' },
  { label: '关于我们', key: 'About' },
  { label: '产品服务', key: 'Products' },
  { label: '新闻动态', key: 'News' },
  { label: '联系我们', key: 'Contact' },
]

const activeKey = computed(() => (route.name as string) ?? 'Home')

function handleMenuSelect(key: string) {
  router.push({ name: key })
  mobileDrawer.value = false
}
</script>

<template>
  <NLayoutHeader bordered class="header">
    <div class="header-inner">
      <div class="logo" @click="router.push('/')">
        <img src="/favicon.svg" alt="logo" class="logo-img" />
        <span class="logo-text">星辰科技</span>
      </div>

      <NMenu
        mode="horizontal"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleMenuSelect"
        class="desktop-menu"
      />

      <NButton class="mobile-toggle" quaternary @click="mobileDrawer = true">
        菜单
      </NButton>
    </div>

    <NDrawer v-model:show="mobileDrawer" placement="top" :height="320">
      <NDrawerContent title="导航菜单" closable>
        <NMenu :options="menuOptions" :value="activeKey" @update:value="handleMenuSelect" />
      </NDrawerContent>
    </NDrawer>
  </NLayoutHeader>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #2d8cf0;
}

.desktop-menu {
  flex: 1;
  margin-left: 48px;
}

.mobile-toggle {
  display: none;
}

@media (max-width: 768px) {
  .desktop-menu {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }
}
</style>
