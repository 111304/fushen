<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  center?: boolean
}>()
</script>

<template>
  <div class="section-title" :class="{ center }">
    <h2 class="title">{{ title }}</h2>
    <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    <div class="underline"></div>
  </div>
</template>

<style scoped>
.section-title {
  margin-bottom: 40px;
}

.section-title.center {
  text-align: center;
}

.title {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 15px;
  color: #888;
}

.center .underline {
  margin: 0 auto;
}

.underline {
  width: 48px;
  height: 3px;
  background: #2d8cf0;
  border-radius: 2px;
  margin-top: 12px;
}
</style>
