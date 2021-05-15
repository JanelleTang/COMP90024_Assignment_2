<template>
  <div class="container">
	<bubble-chart
      v-if="loaded"
      :chart-data="newChartData"
	  :options="options"/>
  </div>
</template>

<script>
import BubbleChart from "@/components/scatter.js"

export default {
  name: "BubbleChartContainer",
  components : {BubbleChart},
  props : ["chartdata"],
  data: () => ({
	loaded: false,
	newChartData: null,
	options: null
  }),
  async mounted() {
	this.loaded = false
	try {
		new Promise((resolve) =>{
		this.newChartData = chartDataFormat(this.chartdata,'n_tweets','sentiment_value') 
		this.options = {
			scales : {
				xAxes: [{
					scaleLabel: {
						labelString: 'Pleasant Community',
						display: true
					}
				}],
				yAxes: [{
					scaleLabel: {
						labelString: 'Multiculturalism Opinion',
						display: true
					}
				}]
			},
			tooltips : {
				callbacks: {
					// specify label on mouseover tooltip
					label : function(item,data) {
					return data['datasets'][0]['data'][item['index']]['label']}
				}
			}
		}
		resolve('')
		}).then(() => {
		// only create chart once the data is returned from api
			this.loaded=true
		})
		
		
	
	} catch (e) {
		console.log("test3")
		console.error(e)
	}
  }

}
function chartDataFormat(data, xVar, yVar) {
			data = data.filter((d) => { return xVar in d && yVar in d;})
			var pointData =  data.map((d) => {return {'x' : +d[xVar], 'y' : +d[yVar], 'r' : 10,
				'label' : d['lga']} })
			return {
				datasets: [{
					//label for entire dataset
					label: "Melbourne",
					borderColor: "black",
					backgroundColor: "blue",
					data: pointData,

				}]
			}
		}

</script>

<style>
</style>