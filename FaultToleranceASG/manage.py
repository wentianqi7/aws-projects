#!/usr/bin/env python

import sys
import os
import boto
import boto.ec2
import boto.ec2.elb
import boto.ec2.autoscale
import boto.ec2.cloudwatch
from boto.ec2.elb import HealthCheck
from boto.ec2.autoscale import LaunchConfiguration
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.autoscale import Tag
from boto.ec2.autoscale import ScalingPolicy
from boto.ec2.cloudwatch import MetricAlarm
import time
import httplib
import urllib2

# add your credentials here
AWS_Access_Key_Id = None
AWS_Secret_Key = None

conn_region = 'us-east-1'
dataCenterAMI = 'ami-3c8f3a54'
loadGeneratorAMI = 'ami-7aba0c12'
data_center_instance_type = 'm1.medium'
load_generator_instance_type = 'm3.medium'
key_name = None
tag_key = 'Project'
tag_value = '2.3'
security_group_name = None
elb_name = 'tianqiwELB'
asg_name = 'tianqiwASG'
security_group_id = None
subnet_id = 'subnet-76d60301'
arn = None
notification = ['autoscaling:EC2_INSTANCE_LAUNCH', 'autoscaling:EC2_INSTANCE_LAUNCH_ERROR', 
                'autoscaling:EC2_INSTANCE_TERMINATE', 'autoscaling:EC2_INSTANCE_TERMINATE_ERROR', 
                'autoscaling:TEST_NOTIFICATION']

MIN_SIZE = 1
MAX_SIZE = 6
DESIRED_SIZE = 1
    
# run new instance
def createNewInstance(ami):
    reservation = conn.run_instances(ami, key_name = key_name, instance_type = load_generator_instance_type,
                                        security_group_ids = [security_group_id], subnet_ids = [subnet_id])
    instance = reservation.instances[0]

    # wait until the instance is running
    status = instance.update()
    print 'wait for instance to run'
    while status == 'pending':
        time.sleep(5)
        status = instance.update()
        
    if status != 'running':
        print 'Instance Status: ' + status
        sys.exit(1)

    # ensure that instance is already running
    # add tag to instances
    instance.add_tag(tag_key, tag_value)
    public_dns_name = instance.public_dns_name
    print 'public dns name = ' + public_dns_name

    # authorization
    time.sleep(60)
    httpConn = httplib.HTTPConnection(public_dns_name)
    httpConn.request('HEAD', '/username?username=tianqiw')
    return instance

# main routine
conn = boto.ec2.connect_to_region(conn_region, aws_access_key_id = AWS_Access_Key_Id, aws_secret_access_key = AWS_Secret_Key)

# create load generator
load_generator_instance = createNewInstance(loadGeneratorAMI)
load_dns_name = load_generator_instance.public_dns_name
print 'load generator started'
print load_dns_name

# create ELB
print 'start to create ELB'
elb_conn = boto.ec2.elb.connect_to_region(conn_region, aws_access_key_id = AWS_Access_Key_Id, 
                                            aws_secret_access_key = AWS_Secret_Key)

hc = HealthCheck(
    interval = 30,
    timeout = 5,
    target = 'HTTP:80/heartbeat?username=tianqiw'
)

zones = ['us-east-1a']
listener = [(80, 80, 'http')]
lb = elb_conn.create_load_balancer(elb_name, zones, listener)
lb.configure_health_check(hc)
elb_conn.apply_security_groups_to_lb(elb_name, security_group_id)
print 'ELB created. DNS = '
print lb.dns_name

# create launch configuration
print 'start creating launch configuration'
asg_conn = boto.ec2.autoscale.connect_to_region(conn_region, aws_access_key_id = AWS_Access_Key_Id,
                                                aws_secret_access_key = AWS_Secret_Key)
launch_config = LaunchConfiguration(name = 'tianqiw_2.2_config', image_id = dataCenterAMI,
                            key_name = key_name, security_groups = [security_group_id],
                            instance_type = data_center_instance_type, instance_monitoring = True)
                            
asg_conn.create_launch_configuration(launch_config)
print 'launch configuration created'

# create AutoScaling Group
print 'start creating autoscaling group'
asg = AutoScalingGroup(group_name = asg_name, load_balancers = [elb_name],
                        availability_zones = ['us-east-1a'],
                        health_check_type = 'ELB',
                        health_check_period = 300,
                        launch_config = launch_config,
                        min_size = MIN_SIZE, max_size = MAX_SIZE, 
                        desired_capacity = DESIRED_SIZE, connection = asg_conn)
                 
asg_conn.create_auto_scaling_group(asg)

# Create a Tag for the auto scaling group
asg_tag = Tag(key = tag_key,
            value = tag_value,
            propagate_at_launch = True,
            resource_id = asg_name)

# Add the tag to the auto scaling group
asg_conn.create_or_update_tags([asg_tag])

print 'autoscaling group created'

# put notification
asg_conn.put_notification_configuration(autoscale_group = asg, topic = arn, notification_types = notification)

# create scaling policy
print 'start creating scaling policy'
scale_up_policy = ScalingPolicy(
            name = 'scale_up', adjustment_type = 'ChangeInCapacity',
            as_name = asg_name, scaling_adjustment = 1, cooldown = 60)

scale_down_policy = ScalingPolicy(
            name = 'scale_down', adjustment_type = 'ChangeInCapacity',
            as_name = asg_name, scaling_adjustment = -1, cooldown = 60)


asg_conn.create_scaling_policy(scale_up_policy)
asg_conn.create_scaling_policy(scale_down_policy)

scale_up_policy = asg_conn.get_all_policies(as_group = asg_name, policy_names=['scale_up'])[0]
scale_down_policy = asg_conn.get_all_policies(as_group = asg_name, policy_names=['scale_down'])[0]

print 'scaling policy created'
                
# create cloud watch for scaling policy
print 'start creating cloud watch'
cloudwatch_conn = boto.ec2.cloudwatch.connect_to_region(conn_region, aws_access_key_id = AWS_Access_Key_Id,
                                                        aws_secret_access_key = AWS_Secret_Key)
alarm_dimensions = {"AutoScalingGroupName": asg_name}

scale_up_alarm = MetricAlarm(
            name = 'scale_up_on_cpu', namespace = 'AWS/EC2',
            metric = 'CPUUtilization', statistic = 'Average',
            comparison = '>=', threshold = '75',
            period = '60', evaluation_periods = 2,
            alarm_actions = [scale_up_policy.policy_arn, arn],
            dimensions = alarm_dimensions)
            
scale_down_alarm = MetricAlarm(
            name = 'scale_down_on_cpu', namespace = 'AWS/EC2',
            metric = 'CPUUtilization', statistic = 'Average',
            comparison = '<=', threshold='65',
            period = '60', evaluation_periods = 2,
            alarm_actions = [scale_down_policy.policy_arn, arn],
            dimensions = alarm_dimensions)
            
cloudwatch_conn.create_alarm(scale_up_alarm)
cloudwatch_conn.create_alarm(scale_down_alarm)
print 'cloud watch created'

time.sleep(300)

# warm-up ELB
print 'warmup start'
warmup_round = 2
elb_dns_name = lb.dns_name

for i in range(1, warmup_round):
    print 'warmup round ' + str(i)
    request_conn = httplib.HTTPConnection(load_dns_name)
    request_str = '/warmup?dns=' + elb_dns_name + '&testId=newTest' + str(i)
    request_conn.request('GET', request_str)
    time.sleep(10)
    url = 'http://' + load_dns_name + '/view-logs?name=warmup_tianqiw.txt'
    lines = urllib2.urlopen(url).readlines()
    print lines[1]
    if not lines[1].startswith('Warm-up launched'): 
        print 'error'
        sys.exit(1)
    else: 
        print 'warmup round ' + str(i) +' start'
        time.sleep(300)

    while(1):
        lines = reversed(urllib2.urlopen(url).readlines())
        completed = False;
        completed = False;
        for line in lines:
            if line.strip().startswith('Warm-up completed'): 
                completed = True
                break
                
        if completed:
            time.sleep(10)
            break
        else:
            print 'wait for warmup to complete'
            time.sleep(15);
    
print 'warmup complete'
time.sleep(5)

# start phase-3
print 'start phase-3'
request_conn = httplib.HTTPConnection(load_dns_name)
request_str = '/begin-phase-3?dns=' + elb_dns_name + '&testId=newTest'
request_conn.request('HEAD', request_str)
time.sleep(6000)
url = 'http://' + load_dns_name + '/view-logs?name=result_tianqiw_newTest.txt'
while(1):
    print 'wait for phase-3 to complete'
    lines = reversed(urllib2.urlopen(url).readlines())
    for line in lines:
        if line.strip().startswith('Total Bonus Minutes'):
            asg.shutdown_instances()
            time.sleep(5)
            asg.delete(force_delete = True)
            print 'phase-3 complete'
            exit(0)
    time.sleep(10)
