<script setup lang="ts">
import {
    NButton,
    NCard,
    NModal,
    NScrollbar,
} from 'naive-ui'

import { StudentHomeTS } from './StudentHome'
import StudentQRCode from '../../components/QRCode.vue'

const {
    userToken,
    student,
    showModal,
    lectures,
    getReservedLectures,
    quitLogin
} = StudentHomeTS()
</script>

<template>
    <div class="student-page">

        <div class="student-card">

            <h1>
                学生签到信息
            </h1>

            <div class="info">

                <div class="row">
                    <span>姓名</span>
                    <span>
                        {{ student.name }}
                    </span>
                </div>

                <div class="row">
                    <span>学号</span>
                    <span>
                        {{ student.id }}
                    </span>
                </div>

                <div class="row">
                    <span>年级</span>
                    <span>
                        {{ student.grade }}
                    </span>
                </div>

                <div class="row">
                    <span>专业</span>
                    <span>
                        {{ student.major }}
                    </span>
                </div>

            </div>

            <StudentQRCode :token=userToken />

            <p class="hint">
                请向老师出示二维码完成签到
            </p>

            <div class="button-area">

                <n-button type="primary" @click="getReservedLectures()">
                    查看参与活动
                </n-button>

                <n-button @click="quitLogin()">
                    退出登录
                </n-button>

            </div>

        </div>
        <n-modal v-model:show="showModal">
            <n-card class="lecture-modal" title="参与活动列表" closable @close="showModal = false">
                <div class="table-header">
                    <span>
                        活动名称
                    </span>

                    <span>
                        活动状态
                    </span>
                </div>

                <n-scrollbar style="
                max-height:400px
            ">
                    <div v-for="
lecture
    in lectures
                " :key="lecture.lecture_id
                    " class="lecture-item" @click="
                        $router.push(
                            `/lecture/${lecture.lecture_id}`
                        )
                        ">
                        <span>
                            {{
                                lecture
                                    .lecture_name
                            }}
                        </span>

                        <span>
                            {{
                                lecture
                                    .status
                            }}
                        </span>
                    </div>
                </n-scrollbar>

                <div class="close-area">
                    <n-button @click="showModal = false">
                        关闭
                    </n-button>
                </div>
            </n-card>
        </n-modal>

    </div>
</template>

<style scoped>
.lecture-modal {
    width: 400px;
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

    padding: 20px 16px;

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