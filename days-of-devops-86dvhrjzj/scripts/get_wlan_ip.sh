#!/bin/bash
ifconfig -a |awk '/wlan/{getline; print $2}'
