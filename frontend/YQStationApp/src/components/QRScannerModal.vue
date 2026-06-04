<script setup lang="ts">
import {
    ref,
    watch,
    onUnmounted,
    nextTick
}
from 'vue'

import {
    Html5Qrcode
}
from 'html5-qrcode'

import {
    NModal,
    NCard,
    useMessage
}
from 'naive-ui'

interface Props
{
    show:boolean

    title?:string

    onSuccess?:
        (
            result:string
        ) =>
        void |
        Promise<void>

    onError?:
        (
            error:unknown
        ) =>
        void |
        Promise<void>
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

let scanner:
Html5Qrcode | null
= null

const isScanning =
ref(false)

const scannerError =
ref('')

async function
startScanner()
{
    try
    {
        scanner =
        new Html5Qrcode(
            'reader'
        )

        await scanner.start(
            {
                facingMode:
                    'environment'
            },

            {
                fps:10,
                qrbox:250
            },

            async(
                decodedText
            ) =>
            {
                if(
                    isScanning
                    .value
                )
                {
                    return
                }

                isScanning
                    .value =
                    true

                try
                {
                    await props
                        .onSuccess
                        ?.
                        (
                            decodedText
                        )
                }
                catch(
                    error
                )
                {
                    console
                    .error(
                        error
                    )

                    await props
                        .onError
                        ?.
                        (
                            error
                        )
                }
            },

            (
                errorMessage
            ) =>
            {
                console
                .debug(
                    errorMessage
                )
            }
        )
    }
    catch(error)
    {
        console.error(
            error
        )

        scannerError
            .value =
            String(error)

        await props
            .onError
            ?.
            (
                error
            )

        message.error(
            '打开摄像头失败'
        )
    }
}

async function
stopScanner()
{
    try
    {
        if(scanner)
        {
            await scanner
                .stop()

            await scanner
                .clear()

            scanner =
                null
        }
    }
    catch(error)
    {
        console.error(
            error
        )
    }

    isScanning
        .value =
        false
}

watch(
    () =>
        props.show,

    async(show)=>
    {
        if(show)
        {
            await nextTick()

            isScanning
                .value =
                false

            await
            startScanner()
        }
        else
        {
            await
            stopScanner()
        }
    }
)

onUnmounted(
    async()=>
    {
        await
        stopScanner()
    }
)
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
        :title="
            title ??
            '扫码'
        "
        closable
        style="
            width:600px
        "
        @close="
            emit(
                'update:show',
                false
            )
        "
    >

        <div id="reader" />

        <p class="error-text">
            {{
                scannerError
            }}
        </p>

    </n-card>

</n-modal>

</template>

<style scoped>
#reader
{
    width:100%;
}
</style>