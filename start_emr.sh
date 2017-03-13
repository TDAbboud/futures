#!/usr/bin/env bash

# Start without bootstrap
aws emr create-cluster --applications Name=Spark --ec2-attributes '{"KeyName":"aws-personal-key","InstanceProfile":"EMR_EC2_DefaultRole","AvailabilityZone":"us-east-1a","EmrManagedSlaveSecurityGroup":"sg-27c32b58","EmrManagedMasterSecurityGroup":"sg-2bc32b54"}' --service-role EMR_DefaultRole --release-label emr-5.2.0 --name 'Spark Cluster' --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m3.xlarge","Name":"MASTER"},{"InstanceCount":1,"InstanceGroupType":"CORE","InstanceType":"m3.xlarge","Name":"CORE"}]' --scale-down-behavior TERMINATE_AT_INSTANCE_HOUR --region us-east-1

# Start with bootstrap
# aws emr create-cluster --applications Name=Spark --bootstrap-actions '[{"Path":"s3://tickerdata/bootstrap/install-jupyter-notebook","Name":"Bootstrap action"}]' --ec2-attributes '{"KeyName":"aws-personal-key","InstanceProfile":"EMR_EC2_DefaultRole","AvailabilityZone":"us-east-1a","EmrManagedSlaveSecurityGroup":"sg-27c32b58","EmrManagedMasterSecurityGroup":"sg-2bc32b54"}' --service-role EMR_DefaultRole --release-label emr-5.2.0 --name 'Spark Cluster' --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"m3.xlarge","Name":"MASTER"},{"InstanceCount":1,"InstanceGroupType":"CORE","InstanceType":"m3.xlarge","Name":"CORE"}]' --scale-down-behavior TERMINATE_AT_INSTANCE_HOUR --region us-east-1

