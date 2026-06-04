<script setup lang="ts">
import {
  NButton,
  NCard,
  NInput,
  NSpace,
  NTabs,
  NTabPane
} from 'naive-ui'

import { LoginTS } from './Login'

const {
  user_id,
  user_name,
  user_role,
  confirm_login
} = LoginTS()
</script>

<template>
  <div class="container">

    <n-card
      title="应签 登录界面"
      class="login-card"
    >

      <n-space vertical size="large">

        <div class="role-title">
          用户身份
        </div>

        <n-tabs
          type="segment"
          animated
          v-model:value="user_role"
        >
          <n-tab-pane
            name="student"
            tab="学生"
          />

          <n-tab-pane
            name="manager"
            tab="管理员/教师"
          />
        </n-tabs>

        <n-input
          v-model:value="user_id"
          :placeholder="
            user_role === 'student'
            ? '输入学号'
            : '输入工号'
          "
        />

        <n-input
          v-model:value="user_name"
          placeholder="输入姓名"
        />

        <n-button
          type="primary"
          block
          @click="confirm_login()"
        >
          确认
        </n-button>

      </n-space>

    </n-card>
  </div>
</template>

<style scoped>
.container
{
  min-height:100vh;

  display:flex;

  justify-content:center;

  align-items:center;

  padding:24px;
}

.login-card
{
  width:420px;
}

.role-title
{
  text-align:center;

  font-size:18px;

  font-weight:600;
}
</style>