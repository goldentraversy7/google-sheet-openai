# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import main

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(main, 'interval', seconds=30)

scheduler.start()
