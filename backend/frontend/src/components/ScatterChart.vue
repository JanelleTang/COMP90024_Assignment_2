<template>
  <div class="container">
	<select v-model="xSelect" @change="runChart" style="display:inline">
		<option disabled>X Axis</option>
		<option value="n_tweets" selected>Tweet Count</option>
		<option value="sentiment_value">Tweet Sentiment</option>
		<option value="renters">Renter</option>
		<option value="owned">Owner</option>
		<option value="being_purchased">Being Purchased</option>
		<option value="coal_miners">Coal Miner</option>
		<option value="miners">Miner</option>
		<option value="gas_supply">Gas Supply</option>
		<option value="solar_panels">Solar Panels</option>
		<option value="solar_water_heaters">Solar Water Heaters</option>
		<option value="income_3000">Income Over 3000</option>
		<option value="income_1250">Income Under 1250</option>
		<option value="age_35">Age Under 35</option>
		<option value="multi_opinion">Multicultural Opinion</option>
		<option value="homeless">Homelessness</option>
		<option value="aboriginal">Aboriginal Origin</option>
		<option value="gaming">Gambling Losses</option>
		<option value="pleasant">Rated as Pleasant Community</option>
		<option value="students">Students</option>
	</select>
	<select v-model="ySelect" @change="runChart" style="display:inline">
		<option disabled>Y Axis</option>
		<option value="n_tweets">Tweet Count</option>
		<option value="sentiment_value" selected>Tweet Sentiment</option>
		<option value="renter">Renter</option>
		<option value="owned">Owner</option>
		<option value="being_purchased">Being Purchased</option>
		<option value="coal_miner">Coal Miner</option>
		<option value="miner">Miner</option>
		<option value="gas_supply">Gas Supply</option>
		<option value="solar_panel">Solar Panels</option>
		<option value="solar_water_heater">Solar Water Heaters</option>
		<option value="income_3000">Income Over 3000</option>
		<option value="income_1250">Income Under 1250</option>
		<option value="age_35">Age Under 35</option>
		<option value="multi_opinion">Multicultural Opinion</option>
		<option value="homeless">Homelessness</option>
		<option value="aboriginal">Aboriginal Origin</option>
		<option value="gaming">Gambling Losses</option>
		<option value="pleasant">Rated as Pleasant Community</option>
		<option value="students">Students</option>
	</select>
	<bubble-chart
      v-if="loaded"
      :chart-data="newChartData"
	  :options="options"/>
  </div>
</template>

<script>
//import axios from "axios";
import BubbleChart from "@/components/scatter.js"
export default {
  name: "BubbleChartContainer",
  components : {BubbleChart},
  props : ["chartdata","extraOptions","selected"],
  data: () => ({
	loaded: false,
	newChartData: null,
	options: null,
	ySelect: "n_tweets",
	xSelect: "sentiment_value",
	highlighted: null
  }),
  async mounted() {
	this.runChart()
  },
  methods: {
	// set the denominator for each metric
	normalize: function(d, v) {
		switch(v){
			case 'renters': case 'owned': case 'being_purchased': case 'solar_panels': case 'solar_water_heaters':
				return +d[v]/+d['total_homes']
			case 'coal_miners': case 'miners': case 'gas_supply':
				return +d[v]/+d['total_industry']
			case 'income_3000': case 'income_1250': case 'age_35':
				return +d[v]/+d['age_income_total']
			case 'multi_opinion': case 'homeless': case 'aboriginal': case 'gaming': case 'pleasant': case 'students':
				return +d[v]/+d['survey_pop']
			default:
				return +d[v]
		}
	},
	chartDataFormat: function(data, xVar, yVar) {
			data = data.filter((d) => { return xVar in d[1] && yVar in d[1];})
			var pointData =  data.map((d) => {return {'x' : this.normalize(d[1],xVar), 'y' : this.normalize(d[1],yVar), 'r' : 10,
				'label' : d[0]} })
			return {
				datasets: [{
					//label for entire dataset
					label: "Melbourne",
					borderColor: "black",
					backgroundColor: data.map((d) => {
					// highlight supplied dot label as red
					return this.highlighted==d[0]?'red':'blue'}),
					data: pointData,
				}]
			}
		},
	runChart: function(lga) {
	this.loaded = false
	console.log(lga)
	if(typeof(lga) == 'string') {
		this.highlighted = lga
	}
	try {
		new Promise((resolve) =>{
		this.newChartData = this.chartDataFormat(this.chartdata,this.xSelect,this.ySelect) 
		this.options = {
			scales : {
				xAxes: [{
					scaleLabel: {
						labelString: this.xSelect,
						display: true
					}
				}],
				yAxes: [{
					scaleLabel: {
						labelString: this.ySelect,
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
			},
			onClick : (mouse,item) => {
				// on click return label to hightlight point
				this.$emit("bubbleclick",this.newChartData['datasets'][0]['data'][item[0]['_index']]['label'])
				this.runChart(this.newChartData['datasets'][0]['data'][item[0]['_index']]['label'])
			}
		}
		// if any additional options passed apply them to options
		this.extraOptions.forEach((d) => {
			this.options[d.key] = d.values
		})
		resolve('')
		}).then(() => {
		// only create chart once the data is returned from api
			this.loaded=true
		})
		
		
	
	} catch (e) {
		console.error(e)
	}
  }
  
  }
}
</script>

<style>
</style>