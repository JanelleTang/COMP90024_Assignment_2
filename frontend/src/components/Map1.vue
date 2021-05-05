

<template>
<section class='text-container'>
<div id = 'gmap'><GmapMap
  :center='center'
  :zoom="7"
  map-type-id="terrain"
  style="width: 600px; height: 400px"
>
  <GmapMarker
    :key="index"
    v-for="(m, index) in markers"
    :position="m.position"
    :clickable="true"
    :draggable="true"
    @click="center=m.position"
  />
</GmapMap>
</div>
</section>
</template>
<script>

export default {
    name: 'Gmap',
    data() {
        return {
            center: "{lat:144.9631, lng:-37.8136}"
        }
    },
    mounted () {
        // At this point, the child GmapMap has been mounted, but
        // its map has not been initialized.
        // Therefore we need to write mapRef.$mapPromise.then(() => ...)
    
        this.$refs.mapRef.$mapPromise.then((map) => {
        map.panTo({lat: 1.38, lng: 103.80})
        })
    }
}
</script>

<style scoped>
#gmap {
  height: 400px;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid darkgrey;
}
.text-container {
  max-width: 600px;
  display: flex;
  flex-direction: column;
  text-align: left;
  align-items: flex-start;
  margin: 0 auto; /* center text container */
}
</style>