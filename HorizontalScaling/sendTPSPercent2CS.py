#!/usr/bin/python

import os
import re
import sys
import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.cloudwatch
from boto.ec2.elb import HealthCheck
from boto.utils import get_instance_metadata
import time
import MySQLdb

AWS_KEY = None
AWS_SECRET = None
MAX_TPS = 148.88
HOST='localhost'
USER='root'
PSW='db15319root'

def count_query():
    conn = MySQLdb.connect(host=HOST,user=USER,passwd=PSW)
    cursor = conn.cursor()
    query = ('show status like \"Queries\";')
    cursor.execute(query)
    count = cursor.fetchone()
    # print count
    return int(count[1])

def get_uptime():
    conn = MySQLdb.connect(host=HOST,user=USER,passwd=PSW)
    cursor = conn.cursor()
    query = ('show status like \"Uptime\";')
    cursor.execute(query)
    uptime = cursor.fetchone()
    # print uptime
    return int(uptime[1])

# main routine
metadata = get_instance_metadata()
instance_id = metadata['instance-id']
elb = boto.ec2.cloudwatch.connect_to_region('us-east-1', aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
old_count = count_query()+6
old_time = get_uptime()
time.sleep(60)

while(True):
    cur_count = count_query()
    cur_time = get_uptime()
    cur_tps = (cur_count - old_count)/(cur_time - old_time)/16
    insert_percent = cur_tps/MAX_TPS*100
    print 'persent:' + str(insert_percent)
    elb.put_metric_data(namespace='tianqiw/TPS',name='TPS3',value=insert_percent,unit='Percent',dimensions=dict(Instance=instance_id))
    old_count = cur_count + 6
    old_time = cur_time
    time.sleep(60)
