<template>
    <management-nav></management-nav>
    <router-view></router-view>
</template>


<script>
import ManagementNav from './nav/ManangementNav.vue'
export default {
    components: {
        ManagementNav
    }
}
</script>