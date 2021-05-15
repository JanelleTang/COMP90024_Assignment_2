<template>
  <div class="Dashboard">
	<v-app>
		<v-content>
			<v-row>
				<h1 style="text-align: center; width:100%">
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

//import axios from "axios";
import ScatterChart from "@/components/ScatterChart"
import LineChart from "@/components/LineChart"
import BarChart from "@/components/BarChart"
import { mean, sum, min, max } from 'mathjs'

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
	this.loadGraphs('all')
  },
  methods: {
	extent: function(values) {
		try{
			return [min(values),max(values)]
		} catch {
			return [null,null]
		}
	},
	clickedbubble : function(value) {
		this.titleHeader = value;
		this.loadGraphs(value)
	},
	checkNum: function(x) {
		return x>0?x:0
	},
	loadGraphs: function(lga) {
	
	this.loaded = false
	Promise.all([require("@/assets/tempGeoJSON.json"),require("@/assets/aurin.json"),
				require("@/assets/dailyTweets.json")]).then((files) =>{
		var chartdata = files[0]['features'].map((d) => {
			var prop = d.properties
			var aurinLGA = files[1][prop.name]
			return {'lga' : prop.name,
					'city' : prop.city,
					'n_tweets' : prop.n_tweets,
					'sentiment_value' : prop.sentiment_value*prop.n_tweets,
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
					'multi_opinion' : aurinLGA?this.checkNum(aurinLGA['multiculturalism_opinion']*aurinLGA['age_income_tot']):0,
					'homeless' : aurinLGA?this.checkNum(aurinLGA['homeless_perc']*aurinLGA['age_income_tot']):0,
					'aboriginal' : aurinLGA?this.checkNum(aurinLGA['aboriginal_origin']*aurinLGA['age_income_tot']):0,
					'pleasant' : aurinLGA?this.checkNum(aurinLGA['pleasant_community']*aurinLGA['age_income_tot']):0,
					'gaming' : aurinLGA?this.checkNum(aurinLGA['gaming_losses']*aurinLGA['age_income_tot']):0,
					'students' : aurinLGA?this.checkNum(aurinLGA['students']*aurinLGA['age_income_tot']):0,
					'survey_pop' : aurinLGA?this.checkNum((aurinLGA['students']?aurinLGA['age_income_tot']:0)):0
				}
		});
		
		this.chartdata = this.groupBy(chartdata,'city')
		
		this.tweetData = Object.entries(files[2].obj.filter(function(d) {return d.name == lga || lga == 'all'}).reduce(function(a,b) {
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
		this.tweetData = this.tweetData.sort(function(a,b) {if(a[0]<b[0]){return -1}else{return 1}})

		this.scatterOptions = []
		this.linedata = {labels : this.tweetData.map((d) => {return d[0]}),
			datasets: [{
				label: 'Daily Tweets',
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
		var minMax = {
			'renters' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].renters/d[1].total_homes:null})),
			'owned' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].owned/d[1].total_homes:null})),
			'being_purchased' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].being_purchased/d[1].total_homes:null})),
			'coal_miners' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].coal_miners/d[1].industry:0})),
			'gas_supply' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].gas_supply/d[1].industry:null})),
			'miners' : this.extent(this.chartdata.map((d) => {return d[1].industry>0?d[1].miners/d[1].industry:null})),
			'solar_panels' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].solar_panels/d[1].total_homes:null})),
			'solar_water_heaters' : this.extent(this.chartdata.map((d) => {return d[1].total_homes>0?d[1].solar_water_heaters/d[1].total_homes:null})),
			'income_3000' : this.extent(this.chartdata.map((d) => {return d[1].age_income_tot>0?d[1].income_3000/d[1].age_income_tot:null})),
			'income_1250' : this.extent(this.chartdata.map((d) => {return d[1].age_income_tot>0?d[1].income_1250/d[1].age_income_tot:null})),
			'age_35' : this.extent(this.chartdata.map((d) => {return d[1].age_income_tot>0?d[1].age_35/d[1].age_income_tot:null})),
			'multi_opinion' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].multi_opinion/d[1].survey_pop:null})),
			'homeless' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].homeless/d[1].survey_pop:null})),
			'aboriginal' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].aboriginal/d[1].survey_pop:null})),
			'pleasant' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].pleasant/d[1].survey_pop:null})),
			'gaming' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].gaming/d[1].survey_pop:null})),
			'students' : this.extent(this.chartdata.map((d) => {return d[1].survey_pop>0?d[1].students/d[1].survey_pop:null}))
		}
		var barData = this.chartdata.filter((d) => {return d[0] == lga || lga == "all"})
		this.barProp = {labels : ['Renters','Owners','Being Purchased','Coal Miners','Gas Supply','Mining','Solar Panels','SOlar Water Heaters',
									'Income Over 3000','Income Under 1250','Age under 35','Multiculturalism Opinion','Homeless Rate','Aboriginal Origin',
									'Pleasant COmmunity','Gaming Losses','Students'],
			datasets: [{
				label: 'Features',
				data : [
					((sum(barData.map((d) => {return d[1].renters}))/sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['renters'][0])/(minMax['renters'][1]-minMax['renters'][0]),
					((sum(barData.map((d) => {return d[1].owned}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['owned'][0])/(minMax['owned'][1]-minMax['owned'][0]),
					((sum(barData.map((d) => {return d[1].being_purchased}))/
					sum(barData.map((d) => {return (d[1].total_homes)})))-minMax['being_purchased'][0])/(minMax['being_purchased'][1]-minMax['being_purchased'][0]),
					sum(barData.map((d) => {return (d.coal_miners?d.coal_miners:0)})) / sum(barData.map((d) => {return (d.industry?d.industry:0)})),
					sum(barData.map((d) => {return (d.gas_supply?d.gas_supply:0)})) / sum(barData.map((d) => {return (d.industry?d.industry:0)})),
					sum(barData.map((d) => {return (d.miners?d.miners:0)})) / sum(barData.map((d) => {return (d.industry?d.industry:0)})),
					sum(barData.map((d) => {return d.solar_panels?d.solar_panels:0}))/
					sum(barData.map((d) => {return (d.renters?d.renters:0)+(d.owned?d.owned:0)+(d.being_purchased?d.being_purchased:0)})),
					sum(barData.map((d) => {return d.solar_water_heaters?d.solar_water_heaters:0}))/
					sum(barData.map((d) => {return (d.renters?d.renters:0)+(d.owned?d.owned:0)+(d.being_purchased?d.being_purchased:0)})),
					sum(barData.map((d) => {return d.income_3000?d.income_3000:0}))/
					sum(barData.map((d) => {return (d.age_income_tot?d.age_income_tot:0)})),
					sum(barData.map((d) => {return d.income_1250?d.income_1250:0}))/
					sum(barData.map((d) => {return (d.age_income_tot?d.age_income_tot:0)})),
					sum(barData.map((d) => {return d.age_35?d.age_35:0}))/
					sum(barData.map((d) => {return (d.age_income_tot?d.age_income_tot:0)})),
					sum(barData.map((d) => {return (d.multi_opinion&&d.age_income_tot)?d.multi_opinion*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.multi_opinion&&d.age_income_tot)?d.d.age_income_tot:0})),
					sum(barData.map((d) => {return (d.homeless&&d.age_income_tot)?d.homeless*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.homeless&&d.age_income_tot)?d.d.age_income_tot:0})),
					sum(barData.map((d) => {return (d.aboroiginal&&d.age_income_tot)?d.aboroiginal*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.aboroiginal&&d.age_income_tot)?d.d.age_income_tot:0})),
					sum(barData.map((d) => {return (d.pleasant&&d.age_income_tot)?d.pleasant*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.pleasant&&d.age_income_tot)?d.d.age_income_tot:0})),
					sum(barData.map((d) => {return (d.gaming&&d.age_income_tot)?d.gaming*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.gaming&&d.age_income_tot)?d.d.age_income_tot:0})),
					sum(barData.map((d) => {return (d.students&&d.age_income_tot)?d.students*d.age_income_tot:0}))/
					sum(barData.map((d) => {return (d.students&&d.age_income_tot)?d.d.age_income_tot:0}))
						],
				fill: false,
				borderColor: 'red',
			}]
		}
	}).then(() => {
		this.loaded = true
		this.loaded2 = true
	});
	  
	 
	},
	 groupBy : function (data,key) {
		var obj = data.reduce(function (a,b) {
			if(b[key] in a) {
				a[b[key]]['n_tweets'] += b['n_tweets']
				a[b[key]]['sentiment_value'] += b['sentiment_value']
				a[b[key]]['owned'] += b['owned']
				a[b[key]]['renters'] += b['renters']
				a[b[key]]['being_purchased'] += b['being_purchased']
				a[b[key]]['total_homes'] += b['total_homes']
				a[b[key]]['industry'] += b['industry']
				a[b[key]]['coal_miners'] += b['coal_miners']
				a[b[key]]['miners'] += b['miners']
				a[b[key]]['gas_supply'] += b['gas_supply']
				a[b[key]]['solar_panels'] += b['solar_panels']
				a[b[key]]['solar_water_heaters'] += b['solar_water_heaters']
				a[b[key]]['income_3000'] += b['income_3000']
				a[b[key]]['income_1250'] += b['income_1250']
				a[b[key]]['age_35'] += b['age_35']
				a[b[key]]['age_income_total'] += b['age_income_total']
				a[b[key]]['multi_opinion'] += b['multi_opinion']
				a[b[key]]['homeless'] += b['homeless']
				a[b[key]]['aboriginal'] += b['aboriginal']
				a[b[key]]['pleasant'] += b['pleasant']
				a[b[key]]['gaming'] += b['gaming']
				a[b[key]]['students'] += b['students']
				a[b[key]]['survey_pop'] += b['survey_pop']
			} else {
				a[b[key]] = {'n_tweets' : b['n_tweets'], 'sentiment_value' : b['sentiment_value'], 'owned' :  b['owned'], 'renters' : b['renters'],
				'being_purchased' : b['being_purchased'], 'total_homes' : b['total_homes'],
				'industry' : b['industry'], 'coal_miners' : b['coal_miners'], 
				'miners' : b['miners'], 'gas_supply' : b['gas_supply'], 'solar_panels' : b['solar_panels'], 'solar_water_heaters' : b['solar_water_heaters'], 
				'income_3000' : b['income_3000'], 'income_1250' : b['income_1250'], 'age_35' : b['age_35'], 'age_income_total' : b['age_income_total'], 
				'multi_opinion' : b['multi_opinion'], 'homeless' : b['homeless'], 'aboriginal' : b['aboriginal'], 'pleasant' : b['pleasant'], 
				'gaming' : b['gaming'], 'students' : b['students'], 'survey_pop' : b['survey_pop']
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