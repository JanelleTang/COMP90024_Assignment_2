<template>
  <div class="Dashboard">
	<v-app>
		<v-content>
			<v-row>
				<v-col cols="12" md="6" lg="4">
					<ScatterChart
						v-if="loaded"
						:chartdata="chartdata"></ScatterChart>
				</v-col>
				<v-col cols="12" md="12" lg="4">
					<LineChart
						v-if="loaded"
						:chart-data="linedata"></LineChart>
				
				</v-col>
				<v-col cols="12" md="6" lg="4">
				
				</v-col>
				
			
			</v-row>
			<v-row>
				<v-col cols="12" md="6" lg="4">
					<BarChart
						v-if="loaded"
						:chart-data="barProp"></BarChart>
				</v-col>
				<v-col cols="12" md="6" lg="4">
					<BarChart
						v-if="loaded"
						:chart-data="barTweets"></BarChart>
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
import { mean, sum } from 'mathjs'

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
	barProp: null,
	loaded: false
  }),
  async mounted() {
	this.loaded = false
	Promise.all([require("@/assets/tempGeoJSON.json"),require("@/assets/aurin.json"),
				require("@/assets/dailyTweets.json")]).then((files) =>{
		this.chartdata = files[0]['features'].map((d) => {
			var prop = d.properties
			var aurinLGA = files[1][prop.name]
			return {'lga' : prop.name,
					'n_tweets' : prop.n_tweets,
					'sentiment_rank' : prop.sentiment_rank,
					'sentiment_value' : prop.sentiment_value,
					'state' : prop.state,
					'owned' : aurinLGA?aurinLGA['owned']:null,
					'renters' : aurinLGA?aurinLGA['renters']:null,
					'being_purchsed' : aurinLGA?aurinLGA['being_purcahsed']:null,
					'industry' : aurinLGA?aurinLGA['industry_total_pop']:null,
					'coal_miners' : aurinLGA?aurinLGA['ind_coal']:null,
					'miners' : aurinLGA?aurinLGA['ind_mining']:null,
					'gas_supply' : aurinLGA?aurinLGA['ind_gas_supply']:null,
					'solar_panels' : aurinLGA?aurinLGA['solarPanels']:null,
					'solar_water_heaters' : aurinLGA?aurinLGA['solarWaterHeaters']:null,
					'income_3000' : aurinLGA?aurinLGA['weekly_income_over_3000']:null,
					'income_1250' : aurinLGA?aurinLGA['weekly_income_under_1250']:null,
					'age_35' : aurinLGA?aurinLGA['age_under_35']:null,
					'age_income_total' : aurinLGA?aurinLGA['age_income_tot']:null,
					'multi_opinion' : aurinLGA?aurinLGA['multiculturalims_opinion']:null,
					'homeless' : aurinLGA?aurinLGA['homeless_perc']:null,
					'aboroiginal' : aurinLGA?aurinLGA['aboriginal_origin']:null,
					'pleasant' : aurinLGA?aurinLGA['pleasant_community']:null,
					'gaming' : aurinLGA?aurinLGA['gaming_losses']:null,
					'sudents' : aurinLGA?aurinLGA['students']:null
				}
		});
		this.linedata = {labels : files[2].map((d) => {return d.date}),
			datasets: [{
				label: 'Daily Tweets',
				data : files[2].map((d) => {return d.sentiment}),
				fill: false,
				borderColor: 'red',
			}]
		}
		this.barTweets = {labels : files[2].map((d) => {return d.date}),
			datasets: [{
				label: 'Daily Tweets',
				data : files[2].map((d) => {return d.n_tweets}),
				fill: false,
				borderColor: 'red',
			}]
		}
		this.barProp = {labels : ['Renters','Owners','Being Purchased','Coal Miners','Gas Supply','Mining','Solar Panels','SOlar Water Heaters',
									'Income Over 3000','Income Under 1250','Age under 35','Multiculturalism Opinion','Homeless Rate','Aboriginal Origin',
									'Pleasant COmmunity','Gaming Losses','Students'],
			datasets: [{
				label: 'Features',
				data : [sum(files[2].map((d) => {return d.renters?d.renters:0}))/sum(files[2].map((d) => {return (d.renters?d.renters:0)+(d.owners?d.owners:0)+(d.being_purchased?d.being_purchased:0)})),
					.7,.9,.1,.2,.6,.7,.2,.3,.1,.23,.7,.4,.14,.9,.2,.1,.3
						],
				fill: false,
				borderColor: 'red',
			}]
		}
	}).then(() => {
		this.loaded = true
	});
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