#!/bin/bash

ccum_count_ok=0
ccum_count_er=0
ccu0_count_ok=0
ccu0_count_er=0
ccu1_count_ok=0
ccu1_count_er=0
bdcm_count_ok=0
bdcm_count_er=0
cecm_count_ok=0
cecm_count_er=0
chcm_count_ok=0
chcm_count_er=0

while true; do
echo "###############################BASE################################"
    time ./fw_upgrade -d can1 -m CCUM -f sator_base_ccu_main_v1.0.1.bin
    if [ $? -eq 0 ]
    then  
      ((ccum_count_ok++))
    else
        ((ccum_count_er++))
    fi
    echo -e "\e[33mCCUM, Success count: $ccum_count_ok, Fail count: $ccum_count_er\e[0m\r\n\r\n"
    sleep 10

    time ./fw_upgrade -d can1 -m CCU0 -f sator_base_ccu_slave_v1.0.8.bin
    if [ $? -eq 0 ]
    then  
      ((ccu0_count_ok++))
    else
        ((ccu0_count_er++))
    fi
    echo -e "\e[33mCCU0, Success count: $ccu0_count_ok, Fail count: $ccu0_count_er\e[0m\r\n\r\n"
    sleep 1

    time ./fw_upgrade -d can1 -m CCU1 -f sator_base_ccu_slave_v1.0.8.bin
    if [ $? -eq 0 ]
    then  
      ((ccu1_count_ok++))
    else
        ((ccu1_count_er++))
    fi
    echo -e "\e[33mCCU1, mSuccess count: $ccu1_count_ok, Fail count: $ccu1_count_er\e[0m\r\n\r\n"
    sleep 1

    time ./fw_upgrade -d can0 -m BDCM -f sator_base_dcm_app_v1.0.2.bin
    if [ $? -eq 0 ]
    then  
      ((bdcm_count_ok++))
    else
        ((bdcm_count_er++))
    fi
    echo -e "\e[33mBDCM, Success count: $bdcm_count_ok, Fail count: $bdcm_count_er\e[0m\r\n\r\n"
    sleep 1


echo "##############################CUBE################################"
    time ./fw_upgrade -d can2 -m CCUM -f sator_cube_ccu_main_v1.1.0.bin
    if [ $? -eq 0 ]
    then  
      ((ccum_count_ok++))
    else
        ((ccum_count_er++))
    fi
    echo -e "\e[33mCCUM, Success count: $ccum_count_ok, Fail count: $ccum_count_er\e[0m\r\n\r\n"
    sleep 10
    
    time ./fw_upgrade -d can2 -m CCU0 -f sator_cube_ccu_slave_v1.0.7.bin
    if [ $? -eq 0 ]
    then  
      ((ccu0_count_ok++))
    else
        ((ccu0_count_er++))
    fi
    echo -e "\e[33mCCU0,Success count: $ccu0_count_ok, Fail count: $ccu0_count_er\e[0m\r\n\r\n"
    sleep 1

    time ./fw_upgrade -d can2 -m CHCM -f sator_cube_hcm_app_v1.1.4.bin
    if [ $? -eq 0 ]
    then  
      ((chcm_count_ok++))
    else
        ((chcm_count_er++))
    fi
    echo -e "\e[33mCCU0,Success count: $chcm_count_ok, Fail count: $chcm_count_er\e[0m\r\n\r\n"
    sleep 1

    time ./fw_upgrade -d can0 -m CECM -f sator_cube_ecm_app_v1.0.6.bin
    if [ $? -eq 0 ]
    then  
      ((cecm_count_ok++))
    else
        ((cecm_count_er++))
    fi
    echo -e "\e[33mCCU0,Success count: $cecm_count_ok, Fail count: $cecm_count_er\e[0m\r\n\r\n"
    sleep 1

done
