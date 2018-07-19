#!/bin/bash
cd /data/jujin-crawler-consumer && nohup python main.py -c Jin10calendar &
cd /data/jujin-crawler-consumer && nohup python main.py -c Jin10kuaixun &
cd /data/jujin-crawler-consumer && nohup python main.py -c Fx678calendar &
cd /data/jujin-crawler-consumer && nohup python main.py -c Fx678kuaixun &
cd /data/jujin-crawler-consumer && nohup python main.py -c Wallstreetcnkuaixun &
cd /data/jujin-crawler-consumer && nohup python main.py -c Article &
cd /data/jujin-crawler-consumer && nohup python main.py -c Filedown &
cd /data/jujin-crawler-consumer && nohup python main.py -c Cftc >> logs/cftc.log &
cd /data/jujin-crawler-consumer && nohup python main.py -c Stock >> logs/stock.log &
cd /data/jujin-crawler-consumer && nohup python main.py -c Fxssi >> logs/Fxssi.log &
cd /data/jujin-crawler-consumer && nohup python main.py -c Niuyan >> logs/Niuyan.log &
cd /data/jujin-crawler-consumer && nohup python main.py -c Viponline >> logs/Viponline.log &
cd /data/jujin-crawler-consumer && nohup python main.py -c Jinsekuaixun >> logs/Jinsekuaixun.log &
