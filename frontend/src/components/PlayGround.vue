<template>
  <div>
    <font-awesome-icon :icon="myIcon" />
     <button class="btn btn-primary"> CSD <font-awesome-icon :icon="myPhone" /></button>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
import { faPhoneVolume } from '@fortawesome/free-solid-svg-icons'


export default {
  name: 'MyComponent',

  data () {
    return {
      myIcon: faSpinner,
      myPhone : faPhoneVolume
    }
  },

  components: {
    FontAwesomeIcon
  }
}
</script>