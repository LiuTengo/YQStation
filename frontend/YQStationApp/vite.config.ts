import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import basicSsl from '@vitejs/plugin-basic-ssl'

export default defineConfig({
    plugins: [
        vue(),
        basicSsl()
    ],

    server:
    {
        host:'0.0.0.0',

        https:{},

        proxy:
        {
            '/api':
            {
                target:
                    'http://192.168.1.6:8000',

                changeOrigin:true,

                secure:false
            }
        }
    }
})