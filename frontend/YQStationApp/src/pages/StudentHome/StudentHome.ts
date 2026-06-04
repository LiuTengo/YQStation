import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { useRouter } from 'vue-router'


export interface StudentInfo {
    id: string
    name: string
    grade: string
    major: string
}

export interface ReservedLectureInfo {
    lecture_id: number
    lecture_name: string
    start_time: string
    status: string
}

export function StudentHomeTS() {
    const message = useMessage()
    const router = useRouter()

    const userToken = localStorage.getItem("login_token") ?? ''
    const student =
        computed<StudentInfo>(() => {
            const data =
                localStorage.getItem(
                    "student_info"
                )

            if (!data) {
                return {
                    id: '',
                    name: '',
                    grade: '',
                    major: ''
                }
            }

            return JSON.parse(data)
        })

    const showModal = ref(false)
    const lectures = ref<ReservedLectureInfo[]>([])

    async function getReservedLectures() {
        try {
            const response =
                await fetch(
                    '/api/reserved_lectures'
                    +
                    `?student_id=${student.value.id}`,
                    {
                        method: 'GET'
                    }
                )

            const data = await response.json()

            lectures.value = data

            showModal.value = true
        }
        catch (error) {
            console.error(error)

            message.error('获取活动列表失败')
        }
    }

    async function quitLogin() {
        localStorage.removeItem("login_token")
        localStorage.removeItem("student_info")
        localStorage.removeItem("user_role")
        localStorage.removeItem("user_id")

        router.push('/')
    }

    return {
        userToken,
        student,
        showModal,
        lectures,
        getReservedLectures,
        quitLogin
    }
}