// import prebuilt chart from chart.js
import { Bubble, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Bubble,
  // reactive prop used for updates to chart
  mixins: [reactiveProp],
  props: ['options'],
  mounted () {
	  console.log(this.options)
	  console.log(this.chartData)
    this.renderChart(this.chartData, this.options)
  }
}