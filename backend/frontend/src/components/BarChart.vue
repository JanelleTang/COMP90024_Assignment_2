<script>
import { Bar } from 'vue-chartjs'
export default {
  extends: Bar,
  props : ["chartData","options"],
  data: () => ({
  }),
  mounted() {
   this.renderChart(this.chartData, this.options)
  }
 }
</script>

<style>
</style>