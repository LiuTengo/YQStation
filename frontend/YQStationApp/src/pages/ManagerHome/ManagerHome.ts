import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import { useRouter } from 'vue-router'


export interface ManagerInfo {
    id: string
    name: string
}

export interface LectureInfo {
    id: number
    name: string
    description: string
    start_time: string
    created_time: string
}

export function ManagerHomeTS() {
  const message = useMessage()
  const router = useRouter()

  const manager = computed<ManagerInfo>(() => {
    const data = localStorage.getItem("manager_info")

    if (!data) {
      return {
        id: '',
        name: ''
      }
    }

    return JSON.parse(data)
  })

  const AllLectures = ref<LectureInfo[]>([])

  const showAllLecturesModal = ref(false)
  const showCreateLectureModal = ref(false)

  async function getAllLectures() {
    try {
        const response = await fetch('/api/all_lectures')

        const data = await response.json()

        AllLectures.value = data
        for (const lecture of AllLectures.value) {
            lecture.start_time = new Date(lecture.start_time).toLocaleString(            
              'zh-CN',
            {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            })
            lecture.created_time = new Date(lecture.created_time).toLocaleString(            
              'zh-CN',
            {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            })
        }

        showAllLecturesModal.value = true
    }
    catch (error) {
        console.error(error)
        message.error('获取活动列表失败')
    }
  }

  async function quitLogin() {
    localStorage.removeItem("login_token")
    localStorage.removeItem("manager_info")
    localStorage.removeItem("user_role")
    localStorage.removeItem("user_id")

    router.push('/')
  }

  return {
    manager,
    showAllLecturesModal,
    showCreateLectureModal,
    AllLectures,
    getAllLectures,
    quitLogin
  }
}