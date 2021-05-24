# ============= COMP90024 - Assignment 2 ============= #
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
# ==================================================== 

#!/bin/bash
nohup python3 -u ./twitter_streaming2.py > output2.log &
sleep 10s
nohup python3 -u ./twitter_streaming3.py > output3.log &
sleep 10s
nohup python3 -u ./twitter_streaming4.py > output4.log &
