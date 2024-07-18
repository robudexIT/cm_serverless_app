import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


import { createApp, defineAsyncComponent } from 'vue';


import App from './App.vue'
import BaseContainer from  './components/layout/BaseContainer.vue'
import BaseTable from './components/layout/BaseTable.vue'
//import BaseSpinner from './components/layout/BaseSpinner.vue'
//import BaseDialog from './components/layout/BaseDialog.vue'

//async-lazy download good for production
const BaseDialog = defineAsyncComponent(() => import('./components/layout/BaseDialog.vue'))
const BaseSpinner = defineAsyncComponent(() => import('./components/layout/BaseSpinner.vue'))

import store from './store/index.js'
import router from './router.js'


const app = createApp(App)


app.component('base-container',BaseContainer)
app.component('base-table', BaseTable)
app.component('base-spinner',BaseSpinner)
app.component('base-dialog',BaseDialog)


app.use(store)
app.use(router)

console.log('this is main')

app.mount('#app')


