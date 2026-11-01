<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import {
  NCard,
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSpace,
  useMessage,
  type FormInst,
  type FormRules,
} from 'naive-ui'
import SectionTitle from '@/components/SectionTitle.vue'
import { useCompanyData } from '@/composables/useCompanyData'
import { submitContact } from '@/api/contact'
import type { ContactForm } from '@/types'

const message = useMessage()
const { company, fetchCompany } = useCompanyData()
fetchCompany()

const formRef = ref<FormInst | null>(null)
const submitting = ref(false)

const formModel = reactive<ContactForm>({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
})

const rules: FormRules = {
  name: { required: true, message: '请输入姓名', trigger: 'blur' },
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  subject: { required: true, message: '请输入主题', trigger: 'blur' },
  message: { required: true, message: '请输入留言内容', trigger: 'blur' },
}

const contactInfo = computed(() => [
  { icon: '📍', label: '公司地址', value: company.value.address },
  { icon: '📞', label: '联系电话', value: company.value.phone },
  { icon: '✉️', label: '电子邮箱', value: company.value.email },
])

async function handleSubmit() {
  try {
    // 1. 先校验表单
    await formRef.value?.validate()

    // 2. 校验通过才设置"正在提交"状态(按钮转圈圈)
    submitting.value = true

    // 3. 真正提交:把 formModel 整个对象丢给后端接口
    await submitContact(formModel)

    // 4. 成功后提示 + 清空表单
    message.success('提交成功，我们将尽快与您联系！')
    formRef.value?.restoreValidation()
    Object.assign(formModel, { name: '', email: '', phone: '', subject: '', message: '' })

  } catch (err) {
    // 校验失败时 naive-ui 抛的不是 Error 对象,静默返回(不弹错误提示)
    if (!(err instanceof Error)) return
    message.error('提交失败，请稍后重试或直接致电联系我们')

  } finally {
    // 不管成功还是失败,最后都关掉"正在提交"
    submitting.value = false
  }
}

</script>

<template>
  <!-- 页面横幅 -->
  <section class="page-banner">
    <div class="banner-overlay">
      <h1 class="banner-title">联系我们</h1>
      <p class="banner-subtitle">期待与您携手共创未来</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <SectionTitle title="联系方式" subtitle="如有合作意向或咨询需求，请随时联系我们" center />

      <div class="contact-grid">
        <!-- 联系信息 -->
        <div class="contact-info">
          <NCard v-for="item in contactInfo" :key="item.label" class="info-card" hoverable>
            <div class="info-item">
              <span class="info-icon">{{ item.icon }}</span>
              <div>
                <p class="info-label">{{ item.label }}</p>
                <p class="info-value">{{ item.value }}</p>
              </div>
            </div>
          </NCard>

          <div class="qr-section">
            <h4 class="qr-title">关注我们</h4>
            <p class="qr-desc">扫描下方二维码，关注官方公众号</p>
            <div class="qr-placeholder">
              <span>公众号二维码</span>
            </div>
          </div>
        </div>

        <!-- 联系表单 -->
        <div class="contact-form">
          <NCard title="在线留言" hoverable>
            <NForm ref="formRef" :model="formModel" :rules="rules" label-placement="top">
              <NFormItem label="姓名" path="name">
                <NInput v-model:value="formModel.name" placeholder="请输入您的姓名" />
              </NFormItem>
              <NFormItem label="邮箱" path="email">
                <NInput v-model:value="formModel.email" placeholder="请输入您的邮箱" />
              </NFormItem>
              <NFormItem label="电话" path="phone">
                <NInput v-model:value="formModel.phone" placeholder="请输入您的联系电话（选填）" />
              </NFormItem>
              <NFormItem label="主题" path="subject">
                <NInput v-model:value="formModel.subject" placeholder="请输入咨询主题" />
              </NFormItem>
              <NFormItem label="留言内容" path="message">
                <NInput
                  v-model:value="formModel.message"
                  type="textarea"
                  placeholder="请输入您想咨询的内容"
                  :rows="4"
                />
              </NFormItem>
              <NSpace justify="end">
                <NButton
                  type="primary"
                  :loading="submitting"
                  @click="handleSubmit"
                >
                  提交留言
                </NButton>
              </NSpace>
            </NForm>
          </NCard>
        </div>
      </div>
    </div>
  </section>
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
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 32px;
  align-items: start;
}

/* 联系信息 */
.info-card {
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-icon {
  font-size: 28px;
}

.info-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 4px;
}

.info-value {
  font-size: 15px;
  color: #333;
  font-weight: 500;
}

.qr-section {
  margin-top: 24px;
  text-align: center;
}

.qr-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.qr-desc {
  font-size: 13px;
  color: #888;
  margin-bottom: 16px;
}

.qr-placeholder {
  width: 160px;
  height: 160px;
  margin: 0 auto;
  background: #f0f2f5;
  border: 2px dashed #d0d4dc;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 13px;
}

/* 表单 */
.contact-form {
  min-width: 0;
}

@media (max-width: 768px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
}
</style>
