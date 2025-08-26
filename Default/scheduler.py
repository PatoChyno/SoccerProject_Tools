import schedule
import time

import training

schedule.every().day.at("06:30", "Europe/Amsterdam").do(training.run_app())
schedule.every().day.at("10:15", "Europe/Amsterdam").do(training.run_app())
schedule.every().day.at("14:15", "Europe/Amsterdam").do(training.run_app())
schedule.every().day.at("18:15", "Europe/Amsterdam").do(training.run_app())
schedule.every().day.at("22:15", "Europe/Amsterdam").do(training.run_app())

while True:
    schedule.run_pending()
    time.sleep(1)
