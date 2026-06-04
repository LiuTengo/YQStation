<script setup lang="ts">
import VueQrcode from 'vue-qrcode'

defineProps<{
  token: string
}>()
</script>

<template>
  <div class="qr-wrapper">
    <VueQrcode
      :value="token"
      type="image/png"
      :color="{
        dark:'#000000',
        light:'#ffffff'
      }"
      :width="220"
    />
    
  </div>
</template>

<style scoped>
.qr-wrapper
{
    display:flex;

    justify-content:center;

    align-items:center;

    width:100%;

    padding:20px 0;
}
</style>