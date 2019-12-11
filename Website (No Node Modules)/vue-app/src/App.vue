<template>
  <div id="app">
      <div class="bg-light">
        <Display />
      </div>
  </div>
</template>

<script>
import Display from './components/Display.vue'

export default {
  name: 'app',
  methods: {
  },
  components: {
    Display,
  }
}
</script>

<style>
.flush-left{
  padding-left: 0 !important;
  margin-left: 0 !important;
}
.flush-right{
  padding-right: 0 !important;
  margin-right: 0 !important;
}

</style>
