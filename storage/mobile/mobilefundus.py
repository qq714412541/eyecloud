# -*- coding: utf-8 -*-

from tasks.celery_config import celery
from celery.result import AsyncResult
import os, json
from services.logger_service import LogService
from services.download_service import DownloadService
from services.upload_service import UploadService
from algorithms.dr.classify import DRDectect
import tensorflow as tf
import numpy as np
import requests
from services.afterpro import pyc
from FundusAnalysis import FundusAnalysis

import random

download_service = DownloadService()
logger = LogService()
upload_service = UploadService()

# filePath = "2018/8/26/c0de15f2b75f5f8098349299867b2ea9-1535291315852.jpeg"
# DOWNLOAD_PATH = './download'
# BACKEND_HOST = 'localhost:5000'
# BACKEND_NOTIFY_URL = 'http://' + BACKEND_HOST + '/api/notify/fundusImage'
CONFIG_PATH = './algorithms/mobile/online_report/config.py'

CALL_CELERY = False
fundusAnalysis = None


@celery.task
def dr_classify(taskid, reportid, name, image_path, callback):
    global fundusAnalysis, CALL_CELERY
    print(CALL_CELERY)

    if not CALL_CELERY:
        CALL_CELERY = True
        os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >./tmp')
        memory_gpu = [int(x.split()[2]) for x in open('./tmp', 'r').readlines()]
        print(memory_gpu)
        with tf.variable_scope('', reuse=tf.AUTO_REUSE):
            os.environ['CUDA_VISIBLE_DEVICES'] = str(os.getenv('ENV_PORT'))
            print('now use', str(os.getenv('ENV_PORT')))
            fundusAnalysis = FundusAnalysis()
            fundusAnalysis.initial(record_dir='./', model_dir='./models')
            os.system('rm tmp')





    report, _, _ = fundusAnalysis.analysis(
            [image_path],[name], [reportid]

        )
    print(report)
    
    post_pdf = report[0]['report_path']
    dr = report[0]['dr']

    result = {
        
        'taskid' : taskid,
        'abnormal': dr

    }
    print(result)



    # tranfrom into json
    #results_json = json.dumps(results, ensure_ascii=False)



    # 3. Notify the backend

    files = {'file': open(post_pdf, 'rb')}
    res = requests.post(url=callback, data=result, files=files)
    print(res.text)
    print(res)
    
    return result
    



