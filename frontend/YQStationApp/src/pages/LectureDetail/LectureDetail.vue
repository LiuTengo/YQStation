<script setup lang="ts">
import {
    NCard,
    NButton,
    NSpace,
    NModal,
    NInput,
    backTopDark
} from 'naive-ui'

import {
    LectureDetailTS
} from './LectureDetail'

import QRScannerModal from
    '../../components/QRScannerModal.vue'

import QRCode from '../../components/QRCode.vue'

const {
    lecture,
    student_status,
    showCheckInModal,
    showReserveModal,
    showCheckOutModal,
    showScanQRCodeModal,
    showSignoutQRCode,
    showStudentSignoutScanner,
    showLectureQRCodeModal,
    base_url,
    start_time_format,
    role,
    checkInStudentId,
    confirmCheckIn,
    confirmReserve,
    confirmCheckOut,
    signinQRCode,
    signoutQRCode,
    backToHome
} =
    LectureDetailTS()
</script>

<template>

    <div class="container">

        <n-card class="detail-card" :title="lecture?.name
            ">

            <n-space vertical size="large">

                <div>
                    <strong>
                        开始时间：
                    </strong>

                    {{
                        start_time_format
                    }}
                </div>

                <div>
                    <strong>
                        地点：
                    </strong>

                    {{
                        lecture?.location
                    }}
                </div>

                <div>
                    <strong>
                        描述：
                    </strong>

                    {{
                        lecture?.description
                    }}
                </div>

                <n-button type="primary" @click="showLectureQRCodeModal = true">
                    查看课程二维码
                </n-button>

                <n-modal v-model:show="showLectureQRCodeModal">
                    <n-card style="width:350px" title="课程二维码" closable @close="showLectureQRCodeModal = false">
                        <QRCode :token="`${base_url}/lecture/${lecture?.id}`" />
                    </n-card>
                </n-modal>


                <!-- 学生 -->

                <template v-if="
                    role ===
                    'student'
                ">

                    <div>
                        <strong>
                            我的状态：
                        </strong>

                        {{
                            student_status
                        }}
                    </div>

                    <div class="button-container">

                        <n-button type="primary" @click="showReserveModal = true">
                            预约活动
                        </n-button>

                        <n_button type="error" @click="showStudentSignoutScanner = true">
                            扫码签退
                        </n_button>

                    </div>

                </template>

                <QRScannerModal v-model:show="showStudentSignoutScanner" title="扫码签退" 
                v-on:success="signoutQRCode" />

                <!-- 管理员 -->

                <template v-if="
                    role ===
                    'manager'
                ">

                    <div class="button-container">

                        <n-space>

                            <n-button type="primary" @click="showScanQRCodeModal = true">
                                扫码签到
                            </n-button>

                            <n-button type="primary" @click="showCheckInModal = true">
                                开始签到
                            </n-button>

                            <n-button type="primary" @click="showReserveModal = true">
                                帮学生预约该活动
                            </n-button>

                            <n-button type="warning" @click="showSignoutQRCode = true">
                                开始签退
                            </n-button>

                            <n_button type="warning" @click="showCheckOutModal = true">
                                输入学生号签退
                            </n_button>

                        </n-space>

                    </div>

                </template>

                <n-modal v-model:show="showCheckInModal" class="manager_modal">
                    <n-card title="
            填写学生学号完成签到
        " closable @close="
            showCheckInModal =
            false
            ">

                        <n-space vertical>

                            <n-input v-model:value="checkInStudentId
                                " placeholder="
                    请输入学生学号
                " />

                            <n-button type="primary" block @click="
                                confirmCheckIn()
                                ">
                                确认签到
                            </n-button>

                        </n-space>

                    </n-card>
                </n-modal>

                <n-modal v-model:show="showReserveModal
                    " class="manager_modal">
                    <n-card title="
            帮学生预约该活动
        " closable @close="
            showReserveModal =
            false
            ">

                        <n-space vertical>

                            <n-input v-model:value="checkInStudentId
                                " placeholder="
                    请输入学生学号
                " />

                            <n-button type="primary" block @click="
                                confirmReserve()
                                ">
                                确认预约
                            </n-button>

                        </n-space>

                    </n-card>
                </n-modal>

                <n-modal v-model:show="showCheckOutModal" class="manager_modal">
                    <n-card title="
            输入学生学号完成签退
        " closable @close="
            showCheckOutModal =
            false
            ">

                        <n-space vertical>

                            <n-input v-model:value="checkInStudentId
                                " placeholder="
                    请输入学生学号
                " />

                            <n-button type="primary" block @click="
                                confirmCheckOut()
                                ">
                                确认签退
                            </n-button>

                        </n-space>

                    </n-card>
                </n-modal>

                <n-modal v-model:show="showSignoutQRCode">
                    <n-card style="width:350px" title="课程签退二维码" closable @close="showSignoutQRCode = false">
                        <QRCode :token="lecture?.id ?? ''" />
                    </n-card>
                </n-modal>

                <QRScannerModal v-model:show="showScanQRCodeModal" title="扫码签到" 
                v-on:success="signinQRCode"/>


            </n-space>
 

            <n-button @click="backToHome()">
                返回个人主页
            </n-button>
        </n-card>

    </div>

</template>

<style scoped>
.container {
    padding: 40px;

    display: flex;

    justify-content: center;
}

.detail-card {
    width: 700px;
}

.manager_modal {
    width: 400px;
}

.button-container {
    display: flex;

    justify-content: center;

    margin-top: 10px;
}
</style>