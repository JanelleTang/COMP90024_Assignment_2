<template>
	<v-app>
		<v-content>
			<v-row>
				<v-col cols="12" md="12" lg="12">
					<vue-word-cloud
					style="height:80vh"
					:words='words'
					:color="() =>  Math.random() > .75 ? 'DeepPink' : Math.random() > .67 ? 'RoyalBlue' : Math.random() > .5 ? 'lightgreen' : 'Indigo'"
					v-if="loaded"
					>
					
					</vue-word-cloud>
				</v-col>
			</v-row>
		</v-content>
	</v-app>
</template>


<script>
import VueWordCloud from 'vuewordcloud';
import axios from "axios";
export default {
  components: {
    VueWordCloud,
  },
  data: () => ({
	loaded: false,
	words: [['word',10], ['other', 12], ['climate', 2]]
  }),
  async mounted() {
  this.loaded = false
  Promise.all([axios.get("api/tweet/hashtags")]).then((d) =>{
	var data = d[0]['data']['obj'].sort(function(a,b) {return a[1] > b[1]})
	data = data.slice(0,100)
	data = data.map((d) => {return [d[0], Math.log(d[1])]})
	console.log(data)
	this.words = data
  }).then(() => {this.loaded = true});
  },
};


</script>