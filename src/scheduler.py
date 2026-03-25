import sys
sys.path.append('src')
sys.path.append('.')
from main import executar_pipeline
from apscheduler.schedulers.blocking import BlockingScheduler
from logging_config import logger

scheduler = BlockingScheduler()

scheduler.add_job(executar_pipeline, 'cron', id='etl', hour=11, minute=0, replace_existing=True)

try:
    logger.info('Scheduler iniciando. Pressione Ctrl+C para poder parar.')
    scheduler.start()
except (KeyboardInterrupt, SystemExit) as e:
    logger.error(f'Scheduler Error: {e}')
finally:
    scheduler.shutdown()