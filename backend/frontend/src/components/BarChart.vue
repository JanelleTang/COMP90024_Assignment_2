<!--# 
============= COMP90024 - Assignment 2 ============= #
#                               
# The University of Melbourne           
# Team 37
#
# ** Authors: **
# 
# JJ Burke              1048105
# Janelle Tang          694209
# Shuang Qiu            980433
# Declan Baird-Watson   640975
# Avinash Rao           1024577 
# 
# Location: Melbourne
# ==================================================== -->
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