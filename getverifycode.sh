#!/bin/bash

#手机号
MOBILE=$1

#token 固定不变
TOKEN='4aad16200a92f6342701ba63f58972ae'

#logid
LOGID='28364'

#调用方
CALLER='AndroidAutoTest'

CODE=`curl -s "http://rpc.niceprivate.com/misrpc/authent/getSms?token=$TOKEN&mobile=$MOBILE&caller=$CALLER&request_logid=$LOGID" | awk -F ',' '{print $9;}' | awk -F ':' '{print $3;}' | awk -F '}' '{print $1;}'`

echo $CODE
