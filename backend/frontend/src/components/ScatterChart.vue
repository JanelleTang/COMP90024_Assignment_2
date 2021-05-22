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


function tooltipText(d,xVar,yVar) {
		var returnArray = []
		var varArray = [xVar,yVar]
		var varsUsed = [xVar,yVar]
		varArray.forEach((e) => {
			returnArray.push(e+": "+Math.round(+d['data'][e]*100)/100)
			console.log(e)
			switch(e){
			case 'renters': case 'owned': case 'being_purchased': case 'solar_panels': case 'solar_water_heaters':
				console.log("test1")
				if(!varsUsed.includes('total_homes')){
					console.log("test 2")
					returnArray.push("Total Homes: "+Math.round(+d['data']['total_homes']))
					varsUsed.push('total_homes')
				}
				break;
			case 'coal_miners': case 'miners': case 'gas_supply':
				if(!varsUsed.includes('industry')){
					returnArray.push("Industry Total: "+Math.round(+d['data']['industry']))
					varsUsed.push('industry')
				}
				break;
			case 'income_3000': case 'income_1250': case 'age_35':
				if(!varsUsed.includes('age_income_total')){
					returnArray.push("Total Population: "+Math.round(+d['data']['age_income_total']))
					varsUsed.push('age_income_total')
				}
				break;
			case 'multi_opinion': case 'homeless': case 'aboriginal': case 'gaming': case 'pleasant': case 'students':
				if(!varsUsed.includes('survey_pop')){
					returnArray.push("Survey Population: "+Math.round(+d['data']['survey_pop']))
					varsUsed.push('survey_pop')
				}
				break;
			case 'sentiment_value':
				if(!varsUsed.includes('n_tweets')){
					returnArray.push("Tweet Count: "+Math.round(+d['data']['n_tweets']))
					varsUsed.push('n_tweets')
				}
				break;
		}
		})
		return returnArray;
	}
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
				return +d[v]/+d['industry']
			case 'income_3000': case 'income_1250': case 'age_35':
				return +d[v]/+d['age_income_total']
			case 'multi_opinion': case 'homeless': case 'aboriginal': case 'gaming': case 'pleasant': case 'students':
				return +d[v]/+d['survey_pop']
			case 'sentiment_value':
				return +d[v]/+d['n_tweets']
			default:
				return +d[v]
		}
	},
	chartDataFormat: function(data, xVar, yVar) {
			data = data.filter((d) => { return xVar in d[1] && yVar in d[1];})
			var pointData =  data.map((d) => {return {'x' : this.normalize(d[1],xVar), 'y' : this.normalize(d[1],yVar), 'r' : 10,
				'label' : d[0], 'data' : d[1]} })
			return {
				datasets: [{
					//label for entire dataset
					label: "Cities",
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
					// convert label to proper case and replace - with space
					label : ((item,data) => {
					return (data['datasets'][0]['data'][item['index']]['label']).split("-").map(d => d[0].toUpperCase() + d.substr(1)).join(" ")}),
					afterLabel: ((item,data) => {
					return tooltipText(data['datasets'][0]['data'][item['index']],this.xSelect,this.ySelect)
					
					})
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