from crontab import CronTab

# Create a new crontab object
cron = CronTab()

# Add a new cron job to run the script every day at 6 AM
job = cron.new(command='python orchestration.py')

job.setall('0 1 *')


# Write the job to the user's crontab
cron.write()