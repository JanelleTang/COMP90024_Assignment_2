

<script>
import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  props : ["chartData","options"],
  data: () => ({
  }),
  mounted() {
	console.log(this.options)
   this.renderChart(this.chartData, this.options)
  }
 }

</script>

<style>
</style>