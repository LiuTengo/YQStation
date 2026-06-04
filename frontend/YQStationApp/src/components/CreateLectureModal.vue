<script setup lang="ts">
import {
    ref
} from 'vue'

import {
    NModal,
    NCard,
    NInput,
    NButton,
    NSpace,
    NDatePicker,
    useMessage
} from 'naive-ui'

interface Props
{
    show: boolean
}

const props =
defineProps<Props>()

const emit =
defineEmits<{
    (
        e:'update:show',
        value:boolean
    ):void
}>()

const message =
    useMessage()

const name =
    ref('')

const description =
    ref('')

const location =
    ref('')

const activityTime =
    ref<number | null>(
        null
    )

async function
createLecture()
{
    try
    {
        const response =
            await fetch(
                '/api/lecture/create',
                {
                    method:'POST',

                    headers:{
                        'Content-Type':
                        'application/json'
                    },

                    body:
                    JSON.stringify({
                        name:
                            name.value,

                        description:
                            description.value,

                        time:
                            activityTime.value
                            ?
                            new Date(
                                activityTime.value
                            )
                            .toISOString()
                            :
                            '',

                        location:
                            location.value
                    })
                }
            )

        const data =
            await response.json()

        if(data.code === 200)
        {
            message.success(
                '活动创建成功'
            )

            emit(
                'update:show',
                false
            )

            resetForm()
        }
        else
        {
            message.error(
                '活动创建失败'
            )
        }
    }
    catch(error)
    {
        console.error(
            error
        )

        message.error(
            '创建活动失败'
        )
    }
}

function resetForm()
{
    name.value = ''

    description.value = ''

    location.value = ''

    activityTime.value =
        null
}
</script>

<template>

<n-modal
    :show="show"
    @update:show="
        emit(
            'update:show',
            $event
        )
    "
>
    <n-card
        class="create-modal"
        title="创建新活动"
        closable
        @close="
            emit(
                'update:show',
                false
            )
        "
    >

        <n-space
            vertical
            size="large"
        >

            <n-input
                v-model:value="
                    name
                "
                placeholder="
                    活动名称
                "
            />

            <n-input
                v-model:value="
                    description
                "
                type="textarea"
                placeholder="
                    活动描述
                "
            />

            <n-input
                v-model:value="
                    location
                "
                placeholder="
                    活动地点
                "
            />

            <n-date-picker
                v-model:value="
                    activityTime
                "
                type="datetime"
                clearable
            />

            <n-button
                type="primary"
                block
                @click="
                    createLecture()
                "
            >
                创建活动
            </n-button>

        </n-space>

    </n-card>

</n-modal>

</template>

<style scoped>
.create-modal
{
    width:600px;
}
</style>