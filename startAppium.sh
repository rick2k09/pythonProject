pm2 start appium -- -a 127.0.0.1
# nohup appium --address 127.0.0.1 --port 4723 --session-override --log-timestamp --local-timezone  >> appium.log 2>&1&