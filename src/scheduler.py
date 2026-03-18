import sys
sys.path.append('src')
sys.path.append('.')
from main import executar_pipeline
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

scheduler.add_job(executar_pipeline, 'cron', id='etl', hour=11, minute=0, replace_existing=True)

try:
    print('Scheduler iniciando. Pressione Ctrl+C para poder parar.')
    scheduler.start()
except (KeyboardInterrupt, SystemExit) as e:
    print(f'Scheduler Error: {e}')
finally:
    scheduler.shutdown()