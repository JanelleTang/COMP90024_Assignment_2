<template>
  <div class="container">
    <bubble-chart
      v-if="loaded"
      :chart-data="chartdata"
	  :options="options"/>
  </div>
</template>

<script>
import axios from "axios";
import BubbleChart from "@/components/scatter.js"

export default {
  name: "BubbleChartContainer",
  components : {BubbleChart},
  data: () => ({
	// api connects to couchbase data from AURIN
	APIAurin : "http://localhost:8000/api/aurin/",
	loaded: false,
	chartdata: null,
	options: null,
  }),
  async mounted() {
	this.loaded = false
	try {
		
		axios.get(this.APIAurin).then((response) => {
		this.chartdata = chartDataFormat(response.data,'pleasant_community','multiculturalism_opinion') 
		
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
		}).then(() => {
			// only create chart once the data is returned from api
			this.loaded=true
		})
		
	
	} catch (e) {
		console.log("test3")
		console.error(e)
	}
	methods : {
		
	}
  }

}
function chartDataFormat(data, xVar, yVar) {
			data = data.filter((d) => { return xVar in d && yVar in d;})
			var pointData =  data.map((d) => {return {'x' : d[xVar], 'y' : d[yVar], 'r' : 10,
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