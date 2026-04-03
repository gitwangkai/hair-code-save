# 嵌入式固件升级工具
## 简介

嵌入式固件升级工具，仅支持加密固件。

## 依赖
- cmake
- libssl
- libcrypto
- libboost
- libarchive

## 安装依赖
```shell
sudo apt install cmake libssl-dev libboost-all-dev libarchive-dev
```

## 编译
```shell
mkdir build && cd build && cmake .. && make
```
## 运行

```shell
./fw_upgrade -d can0 -b 500000 -f ../test.tar.enc -p password -t 100
```
### 参数说明：
- -d: can名称
- -b: 波特率
- -f: 固件文件路径
- -p: 加密密码
- -t: 超时时间
