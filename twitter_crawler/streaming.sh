#!/bin/bash
nohup python3 -u ./twitter_streaming2.py > output2.log &
sleep 10s
nohup python3 -u ./twitter_streaming3.py > output3.log &
sleep 10s
nohup python3 -u ./twitter_streaming4.py > output4.log &