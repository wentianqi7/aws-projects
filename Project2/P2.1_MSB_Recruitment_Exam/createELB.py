#!/usr/bin/env python

import sys
import os
import boto
import boto.ec2
import boto.route53
import time
import httplib
import urllib2

# add your credentials here
AWS_Access_Key_Id = None
AWS_Secret_Key = None

dataCenterAMI = 'ami-324ae85a'
loadGeneratorAMI = 'ami-1810b270'
instance_type = 'm3.medium'
key_name = '15619_1.1'
tag_key = 'Project'
tag_value = '2.1'
interval = 120
security_group_name = 'tianqiw_project2.1_group'

# create new security group if not exist
def createSecurityGroup():
    security_group = None
    security_groups = conn.get_all_security_groups()
    for temp_security_group in security_groups:
        if temp_security_group.name == security_group_name:
            security_group = temp_security_group
            print 'Security group already exists: ' + security_group.name
            
    if not security_group:
        security_group = conn.create_security_group(security_group_name, 'Security Group for 15619 Project 2.1')
        # enable inbound HTTP access on port 80
        security_group.authorize('tcp', 80, 80, '0.0.0.0/0')
        security_group.authorize('tcp', 22, 22, '0.0.0.0/0')
        print 'Security group successfully created'
        
    return security_group

# run new instance
def createNewInstance(ami, security_group):
    print security_group.rules
    reservation = conn.run_instances(ami, key_name = key_name, instance_type = instance_type, security_groups = [security_group])
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
conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id = AWS_Access_Key_Id, aws_secret_access_key = AWS_Secret_Key)
security_group = createSecurityGroup()
# create load generator
load_generator_instance = createNewInstance(loadGeneratorAMI, security_group)
load_dns_name = load_generator_instance.public_dns_name
print load_dns_name


sum = 0
# create data center instances
while(sum < 3600):
    print 'start a new data center instance'
    data_center_instance = createNewInstance(dataCenterAMI, security_group)
    data_center_dns_name = data_center_instance.public_dns_name
    print data_center_dns_name
    
    request_conn = httplib.HTTPConnection(load_dns_name)
    request_str = '/part/one/i/want/more?dns=' + data_center_dns_name + '&testId=Test'
    request_conn.request('HEAD', request_str)
    time.sleep(90)
    url = 'http://' + load_dns_name + '/view-logs?name=result_tianqiw_Test.txt'
    lines = reversed(urllib2.urlopen(url).readlines())
    sum = 0
    
    # retrieve current rps
    for line in lines:
        if line.startswith('minute '): break
        if line.startswith('ec2-'):
            words = line.strip().split(' ')
            sum += float(words[-3])
    
    print sum
    print 'start sleep 2min'
    time.sleep(interval)
    
print 'Finished'
