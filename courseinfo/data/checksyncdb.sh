#!/usr/bin/env bash

# 前端：
# 1. 没有此状态文件时，对登陆用户就正常显示同步按钮。
# 2. 有此文件时，对登陆用户就显示一个 <Span> ，不是 button，写 “同步中，请等待””
# 3. 用户点击按钮后，在后台create一个文件，里面写0，表示待同步

syncdbfilepath="/home/www/ecustCourseInfo/src/courseinfo/data/syncdbstatus.txt"

[ ! -f ${syncdbfilepath} ] && echo "2.6 exit" && exit
syncdbflag=$(cat ${syncdbfilepath})
# [ "x${syncdbflag}" != "x0" ] && ["x${syncdbflag}" != "x1" ] && rm -rf ${syncdbfilepath} && echo "2.5 rm file & exit" && exit
