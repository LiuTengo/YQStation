<script setup lang="ts">
import {
  NButton,
  NCard,
  NSpace,
  NModal,
  NScrollbar
} from 'naive-ui'

import CreateLectureModal from '../../components/CreateLectureModal.vue'
import { ManagerHomeTS } from './ManagerHome'

const {
  manager,
  showAllLecturesModal,
  showCreateLectureModal,
  AllLectures,
  getAllLectures,
  quitLogin
} = ManagerHomeTS()
</script>
<template>
  <div class="container">

    <n-card title="应签 管理员/教师主页" class="manager-card">
      <n-space vertical>

        <div class="welcome-text">
          欢迎您，
          {{ manager.name }}！
        </div>

        <n-button @click="getAllLectures()">
          查看所有活动
        </n-button>

        <n-button @click="showCreateLectureModal =true">
          创建新活动
        </n-button>

        <n-button @click="quitLogin()">
          退出登录
        </n-button>

        <CreateLectureModal v-model:show="showCreateLectureModal" />

      </n-space>
    </n-card>

    <!-- 所有活动弹窗 -->
    <n-modal v-model:show="showAllLecturesModal
      ">
      <n-card class="lecture-modal" title="所有活动" closable @close="
        showAllLecturesModal =
        false
        ">

        <div class="table-header">

          <span>
            活动名称
          </span>

          <span>
            活动时间
          </span>

        </div>

        <n-scrollbar style="
            max-height:400px
          ">

          <div v-for="
lecture
  in AllLectures
            " :key="lecture.id
              " class="lecture-item" @click="
                $router.push(
                  `/lecture/${lecture.id}`
                )
                ">

            <span>
              {{
                lecture.name
              }}
            </span>

            <span>
              {{
                lecture.start_time
              }}
            </span>

          </div>

        </n-scrollbar>

        <div class="close-area">
          <n-button @click="
            showAllLecturesModal =
            false
            ">
            关闭
          </n-button>
        </div>

      </n-card>
    </n-modal>

  </div>
</template>

<style scoped>
.container {
  padding: 40px;

  display: flex;

  justify-content: center;
}

.manager-card {
  width: 500px;
}

.welcome-text {
  font-size: 18px;

  font-weight: 600;
}

.lecture-modal {
  width: 700px;
}

.table-header {
  display: flex;

  justify-content:
    space-between;

  padding: 16px;

  font-size: 18px;

  font-weight: 600;

  border-bottom:
    2px solid #ddd;
}

.lecture-item {
  display: flex;

  justify-content:
    space-between;

  align-items: center;

  padding: 18px;

  border-bottom:
    1px solid #ddd;

  cursor: pointer;

  transition:
    background 0.2s;
}

.lecture-item:hover {
  background:
    rgba(0,
      0,
      0,
      0.05);
}

.close-area {
  margin-top: 20px;

  display: flex;

  justify-content: center;
}
</style>