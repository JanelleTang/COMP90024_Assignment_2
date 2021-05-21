<template>
  <div class="Dashboard">
	<v-app>
		<v-content>
			<v-row>
				<h1 style="text-align: center; width:100%"
				 @click="clickedbubble('all')">
				{{ titleHeader }}
				</h1>
			</v-row>
			<v-row>
				<v-col cols="12" md="12" lg="6">
					<ScatterChart
						v-if="loaded2"
						:chartdata="chartdata"
						:extra-options="scatterOptions"
						:selected="titleHeader"
						@bubbleclick="clickedbubble"></ScatterChart>
				</v-col>
				<v-col cols="12" md="12" lg="6">
					<LineChart
						v-if="loaded"
						:chart-data="linedata"
						:options="timeSeries"></LineChart>
				
				</v-col>
				
			
			</v-row>
			<v-row>
				<v-col cols="12" md="12" lg="6">
					<BarChart
						v-if="loaded"
						:chart-data="barProp"
						:options="barOptions"></BarChart>
				</v-col>
				<v-col cols="12" md="12" lg="6">
					<BarChart
						v-if="loaded"
						:chart-data="barTweets"
						:options="timeSeries"></BarChart>
				</v-col>
			
			</v-row>
		</v-content>
	</v-app>
  </div>
</template>

<script>
import axios from "axios";
import ScatterChart from "@/components/ScatterChart"
import LineChart from "@/components/LineChart"
import BarChart from "@/components/BarChart"
import { sum, min, max } from 'mathjs'
export default {
  name: "Dashboard",
  components: {
	ScatterChart,
	LineChart,
	BarChart,
  },
  data: () => ({
	chartdata: null,
	linedata: null,
	barTweets: null,
	// 0 to 1 scale on this chart as all data is indexed to max and min values
	barOptions: {
		scales: {
			
				yAxes: [{
					ticks : {
						min: 0,
						max: 1
					}
				}]
			}
		},
	barProp: null,
	// loaded variables keep charts from displaying before api data is returned
	loaded: false,
	loaded2: false,
	extraOptions: null,
	titleHeader: "All LGAs",
	timeSeries: {
        scales: {
            xAxes: [{
                type:"time",
				time:{
					unit: 'day'
				}
			}]
        }
	}
  }),
  async mounted() {
	// initialize graphs with no object selected yet
	this.loadGraphs('all')
  },
  methods: {
	extent: function(values) {
		try{
			// return mins and maxes even if nulls in data
			return [min(values.map(function(d) {return d==null?Infinity:d})),max(values.map(function(d) {return d==null?-Infinity:d}))]
		} catch {
			return [null,null]
		}
	},
	// when a dot is selected in graph, change header, highlight in graph, and limit data in other graphs to only that subdivision
	clickedbubble : function(value) {
		this.titleHeader = value;
		this.loadGraphs(value)
	},
	// used to check if demoninators are valid numbers
	checkNum: function(x) {
		return x>0?x:0
	},
	loadGraphs: function(lga) {
	
	this.loaded = false
	// pull lga info and tweet data from apis and aurin data from static file
	Promise.all([axios.get("api/location/lga"),require("@/assets/aurin.json"),
				axios.get("api/location/dates")]).then((files) =>{
		var chartdata = files[0]['data']['obj'].map((d) => {
			var prop = Object.values(d)[0]
			// lga data is - separated, convert to aurin space separated format
			var aurinLGA = files[1][prop.name.split("-").join(" ")]
			return {'lga' : prop.name,
					'city' : prop.city,
					'n_tweets' : prop.total_tweets,
					'sentiment_value' : prop.total_sentiment*prop.total_tweets,
					'state' : prop.state,
					'owned' : aurinLGA?this.checkNum(aurinLGA['owned']):0,
					'renters' : aurinLGA?this.checkNum(aurinLGA['renters']):0,
					'being_purchased' : aurinLGA?this.checkNum(aurinLGA['being_purcahsed']):0,
					'total_homes' : aurinLGA?(this.checkNum(aurinLGA['being_purcahsed'])+this.checkNum(aurinLGA['owned'])+this.checkNum(aurinLGA['renters'])):0,
					'industry' : aurinLGA?this.checkNum(aurinLGA['industry_total_pop']):0,
					'coal_miners' : aurinLGA?this.checkNum(aurinLGA['ind_coal']):0,
					'miners' : aurinLGA?this.checkNum(aurinLGA['ind_mining']):0,
					'gas_supply' : aurinLGA?this.checkNum(aurinLGA['ind_gas_supply']):0,
					'solar_panels' : aurinLGA?this.checkNum(aurinLGA['solarPanels']):0,
					'solar_water_heaters' : aurinLGA?this.checkNum(aurinLGA['solarWaterHeaters']):0,
					'income_3000' : aurinLGA?this.checkNum(aurinLGA['weekly_income_over_3000']):0,
					'income_1250' : aurinLGA?this.checkNum(aurinLGA['weekly_income_under_1250']):0,
					'age_35' : aurinLGA?this.checkNum(aurinLGA['age_under_35']):0,
					'age_income_total' : aurinLGA?this.checkNum(aurinLGA['age_income_tot']):0,
					'multi_opinion' : aurinLGA?this.checkNum(aurinLGA['multiculturalism_opinion']*aurinLGA['age_income_tot']/100):0,
					'homeless' : aurinLGA?this.checkNum(aurinLGA['homeless_perc']*aurinLGA['age_income_tot']/100):0,
					'aboriginal' : aurinLGA?this.checkNum(aurinLGA['aboriginal_origin']*aurinLGA['age_income_tot']/100):0,
					'pleasant' : aurinLGA?this.checkNum(aurinLGA['pleasant_community']*aurinLGA['age_income_tot']/100):0,
					'gaming' : aurinLGA?this.checkNum(aurinLGA['gaming_losses']*aurinLGA['age_income_tot']/100):0,
					'students' : aurinLGA?this.checkNum(aurinLGA['students']):0,
					'survey_pop' : aurinLGA?this.checkNum((aurinLGA['students']?aurinLGA['age_income_tot']:0)):0
				}
		});
		
		this.chartdata = this.groupBy(chartdata,'city')
		
		this.tweetData = Object.entries(files[2].data.obj.filter(function(d) {return d.name == lga || lga == 'all'}).reduce(function(a,b) {
			Object.entries(b['dates']).forEach(function(d) {
				if(d[0] in a) {
					a[d[0]]['total_sentiment'] += d[1]['total_sentiment']
					a[d[0]]['total_tweets'] += d[1]['total_tweets']
				} else {
					a[d[0]] = {'total_sentiment': d[1]['total_sentiment'], 'total_tweets' : d[1]['total_tweets']}
				}
			})
			return a
		},{}))
		// sort tweet data by date so renders properly on graphs
		this.tweetData = this.tweetData.sort(function(a,b) {if(a[0]<b[0]){return -1}else{return 1}})
		this.scatterOptions = []
		this.linedata = {labels : this.tweetData.map((d) => {return d[0]}),
			datasets: [{
				label: 'Tweet Sentiment',
				data : Object.values(this.tweetData).map((d) => {return d[1]['total_sentiment']/d[1]['total_tweets']}),
				fill: false,
				borderColor: 'red',
			}]
		}
		this.barTweets = {labels : this.tweetData.map((d) => {return d[0]}),
			datasets: [{
				label: 'Daily Tweets',
				data :  Object.values(this.tweetData).map((d) => {return d[1]['total_tweets']}),
				borderColor: 'red',
			}]
		}
		// get the min and max values by geographic subdivision for each factor
		var minMax = {
			'renters' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].renters/d[1].total_homes:null})),
			'owned' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].owned/d[1].total_homes:null})),
			'being_purchased' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].being_purchased/d[1].total_homes:null})),
			'coal_miners' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].coal_miners/d[1].industry:0})),
			'gas_supply' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].gas_supply/d[1].industry:null})),
			'miners' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].miners/d[1].industry:null})),
			'solar_panels' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].solar_panels/d[1].total_homes:null})),
			'solar_water_heaters' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].solar_water_heaters/d[1].total_homes:null})),
			'income_3000' : this.extent(this.chartdata.map((d) => {return d[1].age_income_total>0?d[1].income_3000/d[1].age_income_total:null})),
			'income_1250' : this.extent(this.chartdata.map((d) => {return d[1].age_income_total>0?d[1].income_1250/d[1].age_income_total:null})),
			'age_35' : this.extent(this.chartdata.map((d) => {return d[1].age_income_total>0?d[1].age_35/d[1].age_income_total:null})),
			'multi_opinion' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].multi_opinion/d[1].survey_pop:null})),
			'homeless' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].homeless/d[1].survey_pop:null})),
			'aboriginal' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].aboriginal/d[1].survey_pop:null})),
			'pleasant' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].pleasant/d[1].survey_pop:null})),
			'gaming' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].gaming/d[1].survey_pop:null})),
			'students' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].students/d[1].survey_pop:null}))
		}
		// bar chart renders with x axis as all properties and y axis as 0 to 1 index
		var barData = this.chartdata.filter((d) => {return d[0] == lga || lga == "all"})
		console.log(barData)
		console.log(minMax)
		var barLabels = ['Renters','Owners','Being Purchased','Coal Miners','Gas Supply','Mining','Solar Panels','Solar Water Heaters',
									'Income Over 3000','Income Under 1250','Age under 35','Multiculturalism Opinion','Homeless Rate','Aboriginal Origin',
									'Pleasant COmmunity','Gaming Losses','Students']
		var barFactorData = [
					((sum(barData.map((d) => {return d[1].renters}))/sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['renters'][0])/(minMax['renters'][1]-minMax['renters'][0]),
					((sum(barData.map((d) => {return d[1].owned}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['owned'][0])/(minMax['owned'][1]-minMax['owned'][0]),
					((sum(barData.map((d) => {return d[1].being_purchased}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['being_purchased'][0])/(minMax['being_purchased'][1]-minMax['being_purchased'][0]),
					((sum(barData.map((d) => {return d[1].coal_miners}))/
					sum(barData.map((d) => {return (d[1].industry)})))-minMax['coal_miners'][0])/(minMax['coal_miners'][1]-minMax['coal_miners'][0]),
					((sum(barData.map((d) => {return d[1].gas_supply}))/
					sum(barData.map((d) => {return (d[1].industry)})))-minMax['gas_supply'][0])/(minMax['gas_supply'][1]-minMax['gas_supply'][0]),
					((sum(barData.map((d) => {return d[1].miners}))/
					sum(barData.map((d) => {return (d[1].industry)})))-minMax['miners'][0])/(minMax['miners'][1]-minMax['miners'][0]),
					((sum(barData.map((d) => {return d[1].solar_panels}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['solar_panels'][0])/(minMax['solar_panels'][1]-minMax['solar_panels'][0]),
					((sum(barData.map((d) => {return d[1].solar_water_heaters}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['solar_water_heaters'][0])/(minMax['solar_water_heaters'][1]-minMax['solar_water_heaters'][0]),
					((sum(barData.map((d) => {return d[1].income_3000}))/
					sum(barData.map((d) => {return (d[1].age_income_total)})))-minMax['income_3000'][0])/(minMax['income_3000'][1]-minMax['income_3000'][0]),
					((sum(barData.map((d) => {return d[1].income_1250}))/
					sum(barData.map((d) => {return (d[1].age_income_total)})))-minMax['income_1250'][0])/(minMax['income_1250'][1]-minMax['income_1250'][0]),
					((sum(barData.map((d) => {return d[1].age_35}))/
					sum(barData.map((d) => {return (d[1].age_income_total)})))-minMax['age_35'][0])/(minMax['age_35'][1]-minMax['age_35'][0]),
					((sum(barData.map((d) => {return d[1].multi_opinion}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['multi_opinion'][0])/(minMax['multi_opinion'][1]-minMax['multi_opinion'][0]),
					((sum(barData.map((d) => {return d[1].homeless}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['homeless'][0])/(minMax['homeless'][1]-minMax['homeless'][0]),
					((sum(barData.map((d) => {return d[1].aboriginal}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['aboriginal'][0])/(minMax['aboriginal'][1]-minMax['aboriginal'][0]),
					((sum(barData.map((d) => {return d[1].pleasant}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['pleasant'][0])/(minMax['pleasant'][1]-minMax['pleasant'][0]),
					((sum(barData.map((d) => {return d[1].gaming}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['gaming'][0])/(minMax['gaming'][1]-minMax['gaming'][0]),
					((sum(barData.map((d) => {return d[1].students}))/
					sum(barData.map((d) => {return (d[1].survey_pop)})))-minMax['students'][0])/(minMax['students'][1]-minMax['students'][0])
						]
		console.log(barFactorData);
		// only plot properties that have information to display
		barLabels = barLabels.filter(function(d,i) { return !Number.isNaN(barFactorData[i]);})
		barFactorData = barFactorData.filter(function(d) {return !Number.isNaN(d);})
		this.barProp = {labels : barLabels,
			datasets: [{
				label: 'Features',
				data : barFactorData,
				fill: false,
				borderColor: 'red',
			}]
		}
	}).then(() => {
		// load charts when data has been retrieved
		this.loaded = true
		this.loaded2 = true
	});
	  
	 
	},
	// get sums for grouping by key supplied
	 groupBy : function (data,key) {
		var obj = data.reduce((a,b) => {
			if(b[key] in a) {
				a[b[key]]['n_tweets'] += this.checkNum(b['n_tweets'])
				a[b[key]]['sentiment_value'] += this.checkNum(b['sentiment_value'])
				a[b[key]]['owned'] += this.checkNum(b['owned'])
				a[b[key]]['renters'] += this.checkNum(b['renters'])
				a[b[key]]['being_purchased'] += this.checkNum(b['being_purchased'])
				a[b[key]]['total_homes'] += this.checkNum(b['total_homes'])
				a[b[key]]['industry'] += this.checkNum(b['industry'])
				a[b[key]]['coal_miners'] += this.checkNum(b['coal_miners'])
				a[b[key]]['miners'] += this.checkNum(b['miners'])
				a[b[key]]['gas_supply'] += this.checkNum(b['gas_supply'])
				a[b[key]]['solar_panels'] += this.checkNum(b['solar_panels'])
				a[b[key]]['solar_water_heaters'] += this.checkNum(b['solar_water_heaters'])
				a[b[key]]['income_3000'] += this.checkNum(b['income_3000'])
				a[b[key]]['income_1250'] += this.checkNum(b['income_1250'])
				a[b[key]]['age_35'] += this.checkNum(b['age_35'])
				a[b[key]]['age_income_total'] += this.checkNum(b['age_income_total'])
				a[b[key]]['multi_opinion'] += this.checkNum(b['multi_opinion'])
				a[b[key]]['homeless'] += this.checkNum(b['homeless'])
				a[b[key]]['aboriginal'] += this.checkNum(b['aboriginal'])
				a[b[key]]['pleasant'] += this.checkNum(b['pleasant'])
				a[b[key]]['gaming'] += this.checkNum(b['gaming'])
				a[b[key]]['students'] += this.checkNum(b['students'])
				a[b[key]]['survey_pop'] += this.checkNum(b['survey_pop'])
			} else {
				a[b[key]] = {'n_tweets' : this.checkNum(b['n_tweets']), 'sentiment_value' : this.checkNum(b['sentiment_value']), 
				'owned' :  this.checkNum(b['owned']), 'renters' : this.checkNum(b['renters']),'being_purchased' : this.checkNum(b['being_purchased']), 
				'total_homes' : this.checkNum(b['total_homes']),'industry' : this.checkNum(b['industry']), 'coal_miners' : this.checkNum(b['coal_miners']), 
				'miners' : this.checkNum(b['miners']), 'gas_supply' : this.checkNum(b['gas_supply']), 'solar_panels' : this.checkNum(b['solar_panels']), 
				'solar_water_heaters' : this.checkNum(b['solar_water_heaters']),'income_3000' : this.checkNum(b['income_3000']), 
				'income_1250' : this.checkNum(b['income_1250']), 'age_35' : this.checkNum(b['age_35']), 'age_income_total' : this.checkNum(b['age_income_total']), 
				'multi_opinion' : this.checkNum(b['multi_opinion']), 'homeless' : this.checkNum(b['homeless']), 'aboriginal' : this.checkNum(b['aboriginal']), 
				'pleasant' : this.checkNum(b['pleasant']),'gaming' : this.checkNum(b['gaming']), 
				'students' : this.checkNum(b['students']), 'survey_pop' : this.checkNum(b['survey_pop'])
				}
			}
			return a
		},{})
		return Object.entries(obj)
	  }
  },
};
</script>

<style>
.home{
  height:100vh
}
/* #background-wrapper {
        background:linear-gradient(0deg, rgba(255, 255, 255, 0.3), rgba(0, 0, 0, 0.7)), url(../assets/abstract_low_poly_elegant_banner_design_0111.jpg);
        -webkit-background-size: cover;
        -moz-background-size: cover;
        background-size: cover;
        -o-background-size: cover;
        z-index:1
    } */
#start-btn {
  animation: MoveUpDown 1.1s linear infinite;
  position: fixed;
  top: 40%;
  left: 50%;
  /* bring your own prefixes */
  transform: translate(-50%, -50%);
  text-decoration: none;
}
@keyframes MoveUpDown {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}
</style>