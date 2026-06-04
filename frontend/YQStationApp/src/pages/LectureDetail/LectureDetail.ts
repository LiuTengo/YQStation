import {
    ref,
    onMounted
} from 'vue'

import {
    useRoute
} from 'vue-router'
import {
    useMessage
} from 'naive-ui'
import router from '../..'


export function
    LectureDetailTS() {

    const message = useMessage()
    const route = useRoute()

    const lecture = ref()
    const student_status = ref<string>()
    const showCheckInModal = ref(false)
    const showReserveModal = ref(false)
    const showCheckOutModal = ref(false)
    const showScanQRCodeModal = ref(false)
    const showSignoutQRCode = ref(false)
    const showStudentSignoutScanner = ref(false)
    const showLectureQRCodeModal = ref(false)

    const base_url = window.location.origin

    const role =
        localStorage.getItem(
            'user_role'
        )
    const start_time_format = ref<string>()
    const checkInStudentId = ref<string>('')

    async function confirmCheckOut() {
        try {
            const managerId =
                localStorage.getItem(
                    'user_id'
                )

            const response =
                await fetch(
                    '/api/signout',
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({
                                manager_id:
                                    managerId,

                                client_id:
                                    checkInStudentId
                                        .value,

                                activity_id:
                                    lecture.value?.id ?? ''
                            })
                    }
                )

            const data =
                await response.json()

            if (
                data.signout_res
            ) {
                message.success(
                    '签退成功'
                )

                showCheckOutModal
                    .value = false

                checkInStudentId
                    .value = ''
            }
            else {
                message.error(
                    '签退失败'
                )
            }
        }
        catch (error) {
            console.error(error)

            message.error(
                '预约失败'
            )
        }
    }

    async function confirmCheckIn() {
        try {
            const managerId =
                localStorage.getItem(
                    'user_id'
                )

            const response =
                await fetch(
                    '/api/signin',
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({
                                manager_id:
                                    managerId,

                                client_id:
                                    checkInStudentId
                                        .value,

                                activity_id:
                                    lecture.value?.id ?? ''
                            })
                    }
                )

            const data =
                await response.json()

            if (
                data.signin_res
            ) {
                message.success(
                    '签到成功'
                )

                showCheckInModal
                    .value = false

                checkInStudentId
                    .value = ''
            }
            else {
                message.error(
                    '签到失败'
                )
            }
        }
        catch (error) {
            console.error(error)

            message.error(
                '签到失败'
            )
        }
    }

    async function confirmReserve() {
        try {
            const managerId =
                localStorage.getItem(
                    'user_id'
                )

            const response =
                await fetch(
                    '/api/reserve',
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({
                                manager_id:
                                    managerId,

                                client_id:
                                    checkInStudentId
                                        .value,

                                activity_id:
                                    lecture.value?.id ?? ''
                            })
                    }
                )

            const data =
                await response.json()

            if (
                data.reserve_res
            ) {
                message.success(
                    '预约成功'
                )

                showReserveModal
                    .value = false

                checkInStudentId
                    .value = ''
            }
            else {
                message.error(
                    '预约失败'
                )
            }
        }
        catch (error) {
            console.error(error)

            message.error(
                '预约失败'
            )
        }
    }

    async function
        getLectureDetail() {
        const response =
            await fetch(
                '/api/lecture/detail'
                +
                `?lecture_id=${route.params.id
                }`
            )

        lecture.value =
            await response.json()

        start_time_format.value = new Date(lecture.value.start_time).toLocaleString(
            'zh-CN',
            {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }
        )

        if (role === 'student') {
            const std_lecture_status_response =
                await fetch('/api/student_lecture_status'
                    + `?student_id=${localStorage.getItem("user_id")}`
                    + `&lecture_id=${route.params.id}`
                )

            const std_lecture_status_data = await std_lecture_status_response.json()
            student_status.value = std_lecture_status_data.status
        }
    }

    onMounted(() => {
        getLectureDetail()
    })

    async function signinQRCode(qrResult: string) {

        try {
            const managerId =
                localStorage.getItem(
                    'user_id'
                )

            const response =
                await fetch(
                    '/api/signin_token',
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({
                                manager_id:
                                    managerId,

                                client_id:
                                    qrResult,

                                activity_id:
                                    lecture.value?.id ?? ''
                            })
                    }
                )

            const data =
                await response.json()

            if (
                data.signin_res
            ) {
                message.success(
                    '签到成功'
                )

                showScanQRCodeModal.value = false
            }
            else {
                message.error(
                    '签到失败'
                )
            }
        }
        catch (error) {
            console.error(error)

            message.error(
                '签到失败'
            )
        }
    }

    async function signoutQRCode(qrResult: string) {
        try {
            const clientId =
                localStorage.getItem(
                    'user_id'
                )

            const response =
                await fetch(
                    '/api/signout',
                    {
                        method: 'POST',

                        headers: {
                            'Content-Type':
                                'application/json'
                        },

                        body:
                            JSON.stringify({
                                manager_id: "None",

                                client_id: clientId,

                                activity_id: qrResult
                            })
                    }
                )

            const data =
                await response.json()

            if (
                data.signout_res
            ) {
                message.success(
                    '签退成功'
                )

                showStudentSignoutScanner.value = false
            }
            else {
                message.error(
                    'fetch success but 签退失败'
                )
            }
        }
        catch(error) {
            console.error(error)

            message.error(`fetch failed and 签退失败 ${qrResult}`)
        }
    }

    async function backToHome() {
        if (role === 'student') {
            router.push('/studenthome')
        }
        else if (role === 'manager') {
            router.push('/managerhome')
        }
    }

    return {
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
    }
}