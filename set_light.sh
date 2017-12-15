#!/bin/bash

rostopic pub /set_light led_driver/Light "warm: '$1'
bright: '$2'"
