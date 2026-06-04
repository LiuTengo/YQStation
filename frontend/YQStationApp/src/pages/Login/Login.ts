import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import { useRoute, useRouter } from 'vue-router'

export function LoginTS() {
    const message = useMessage()
    const router = useRouter()
    const route = useRoute()

    const user_role = ref<'student' | 'manager'>('student')
    const user_id = ref<string>('')
    const user_name = ref<string>('')

    const confirm_login = async () => {
        try {
            const response = await fetch('/api/login',
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        login_role: user_role.value,
                        login_id: user_id.value,
                        login_name: user_name.value
                    })
                }
            )

            const data = await response.json()

            if (data.login_res) {
                message.success("登录成功")
                let redirect = route.query.redirect as string
                if(!redirect){
                    redirect = user_role.value === 'student' ? '/studenthome' : '/managerhome'
                }

                if (data.role == "student") {
                    localStorage.setItem(
                        "login_token",
                        data.token
                    )

                    localStorage.setItem(
                        "student_info",
                        JSON.stringify(
                            data.student_info
                        )
                    )
                    localStorage.setItem(
                        "user_id",
                        data.student_info.id
                    )
                    localStorage.setItem(
                        "user_role", "student")

                    
                    router.push(redirect)
                }
                else if (data.role == "manager") {
                    localStorage.setItem(
                        "login_token",
                        data.token
                    )
                    localStorage.setItem(
                        "manager_info",
                        JSON.stringify(
                            data.manager_info
                        )
                    )
                    localStorage.setItem(
                        "user_id",
                        data.manager_info.id
                    )

                    localStorage.setItem(
                        "user_role", "manager")

                    router.push(redirect)
                }
            }
            else {
                message.error("登录失败")
            }
        }
        catch (error) {
            message.error("fetch failed 登录失败")
        }
    }

    return {
        user_role,
        user_id,
        user_name,
        confirm_login
    }
}