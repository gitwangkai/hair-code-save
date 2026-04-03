#include "can_interface_socketcan.h"
#include "crc.h"
#include "cstring"
#include "decryptfile.h"
#include "iostream"
#include "protocol.h"
#include "string"
#include <fstream>
#include <iomanip>
#include <semaphore.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

char *g_device_name = NULL;
uint16_t g_err_count = 0;
// 显示用法
void usage() {
  printf("Usage: ./fw_upgrade -d <device_name> -b <bitrate> -f <file_path> [-p "
         "<password>] "
         "[-t <timeout_ms>] [-v version]\n");
}

void print_version() { printf("fw_upgrade version 2.0.0\n"); }

void printProgressBar(size_t progress, size_t total, size_t barWidth = 50) {
  // 计算进度百分比
  float percent = static_cast<float>(progress) / total * 100.0f;

  // 打印进度条
  std::cout << "\r[";
  size_t pos = static_cast<size_t>(barWidth * progress / total);
  for (size_t i = 0; i < barWidth; ++i) {
    if (i < pos)
      std::cout << "="; // 已完成部分
    else if (i == pos)
      std::cout << ">"; // 当前进度指示器
    else
      std::cout << " "; // 未完成部分
  }
  std::cout << "] " << std::fixed << std::setprecision(2) << percent << "%";

  // 刷新输出流
  std::cout.flush();
}
int main(int argc, char *argv[]) {

  char *file_path = NULL;
  char *password = NULL;
  int timeout = 200;    // 默认超时时间200ms
  int bitrate = 500000; // 默认波特率500k

  // 解析命令行参数
  int opt;
  while ((opt = getopt(argc, argv, "d:b:f:p:t:vh")) != -1) {
    switch (opt) {
    case 'd':
      g_device_name = optarg;
      break;
    case 'b':
      bitrate = atoi(optarg);
      break;
    case 'f':
      file_path = optarg;
      break;
    case 't':
      timeout = atoi(optarg);
      break;
    case 'p':
      password = optarg;
      break;
    case 'v':
      print_version();
      return 1;
    case 'h':
      usage();
      return 1;
    default:
      usage();
      return 1;
    }
  }

  // 检查参数完整性
  if (g_device_name == NULL || file_path == NULL) {
    usage();
    return 1;
  }

  // 检查 file_path 是否以 .bin 结尾
  if (strlen(file_path) < 4 ||
      strcmp(file_path + strlen(file_path) - 4, ".enc") != 0) {
    printf("Error: file_path must end with .enc\n");
    return 1;
  }

  printf("device:%s, file:%s, timeout:%d ms\r\n", g_device_name, file_path,
         timeout);

  std::shared_ptr<SocketcanInterface> can_interface_ptr =
      std::make_shared<SocketcanInterface>(std::string(g_device_name), bitrate);

  DecryptFile decrypt_file;
  if (false == decrypt_file.StartDecryptFile(std::string(file_path),
                                             std::string(password))) {
    printf("警告:文件解密失败！");
    return 1;
  }
  std::vector<unsigned char> firmware_data;

  decrypt_file.GetBinData(firmware_data);
  int node_addr = decrypt_file.GetCanId();

  // 等待用户确认
  char user_input;
  printf("Do you want to continue? (y/n): ");
  int ret = scanf(" %c", &user_input);
  if (ret == 1 && user_input != 'y' && user_input != 'Y') {
    printf("Operation cancelled by user.\n");
    return 1;
  }
  can_interface_ptr->Init();
  Protocol protocol_bl(can_interface_ptr);

  // 开始升级
  protocol_bl.BL_EnterUpgrade();
  usleep(1000 * 100);
  // 升级节点检测
  uint32_t hardversion, appversion, appType;
  ret = protocol_bl.BL_NodeCheck(node_addr, &hardversion, &appversion, &appType,
                                 1000);
  if (ret == CAN_SUCCESS) {
    // 跳转到boot
    ret = protocol_bl.BL_Excute(node_addr, CAN_BL_BOOT);
    if (ret != CAN_SUCCESS) {
      printf("警告:执行固件程序失败！");
      protocol_bl.BL_ExitUpgrade();
      return 1;
    }
  } else {
    printf("警告:节点检测失败！");
    protocol_bl.BL_ExitUpgrade();
    return 1;
  }

  ret = protocol_bl.BL_NodeCheck(node_addr, &hardversion, &appversion, &appType,
                                 1000);
  if (ret == CAN_SUCCESS) {
    if (appType != CAN_BL_BOOT) { // 当前固件不为Bootloader
      printf("警告:当前固件不为Bootloader固件!");
      protocol_bl.BL_ExitUpgrade();
      return 1;
    }
  } else {

    printf("警告:节点检测失败！");
    protocol_bl.BL_ExitUpgrade();
    return 1;
  }
  ret = protocol_bl.BL_Erase(node_addr, firmware_data.size(), 8000);
  if (ret != CAN_SUCCESS) {

    printf("警告:擦除Flash失败!%d", ret);
    protocol_bl.BL_ExitUpgrade();
    return 1;
  }
  int i = 0;
  int pack_size = 128;
  uint8_t firmware_pack[1026] = {0};
  int read_data_num = 0;
  for (i = 0; i < firmware_data.size(); i += pack_size) {

    read_data_num = 0;
    for (int j = i; j < i + pack_size; j++) {
      firmware_pack[read_data_num] = firmware_data[j];
      read_data_num++;
      if (read_data_num == firmware_data.size()) {
        break;
      }
    }
    int try_cnt = 0;
    do {
      ret =
          protocol_bl.BL_Write(node_addr, i, firmware_pack, read_data_num, 100);
      try_cnt++;
      if (try_cnt > 10) {
        printf("警告:连续10次写Flash数据失败!%d", ret);
        protocol_bl.BL_ExitUpgrade();
        return 1;
      }
    } while (ret != CAN_SUCCESS);
    // printf("%ld%%\r", 100*i/firmware_data.size());
    printProgressBar(i, firmware_data.size());
    fflush(stdout);
  }

  unsigned short crc16 = crc16_check_vector(firmware_data);
  uint32_t sw;
  decrypt_file.GetBinSv((uint8_t *)&sw);
  if (protocol_bl.BL_WriteFinish(node_addr, crc16, sw, 5000) != CAN_SUCCESS) {
    printf("警告:写备份程序到app失败!%d", ret);
    protocol_bl.BL_ExitUpgrade();
    return 1;
  } else {
    printf("\n固件升级成功!\n");
  }

  for (int i = 0; i < 5; i++) {
    // 执行固件
    ret = protocol_bl.BL_Excute(node_addr, CAN_BL_APP);
    if (ret != CAN_SUCCESS) {
      printf("警告:执行固件程序失败！%d", ret);
      return 1;
    }
    ret = protocol_bl.BL_NodeCheck(node_addr, &hardversion, &appversion,
                                   &appType, 1000);
    if (ret == CAN_SUCCESS && appType == CAN_BL_APP) {
      break;
    }
    sleep(1);
  }

  if (ret == CAN_SUCCESS) {
    std::string str;
    if (appType == CAN_BL_BOOT) {
      str = "BOOT";
      printf("固件执行失败，当前执行固件为%s\n", str.c_str());
    } else {
      str = "APP";
      printf("固件执行成功，当前执行固件为%s\n", str.c_str());
    }

    printf("当前硬件版本为: v%d.%d.%d \n", (hardversion >> 16) & 0xFF,
           ((hardversion >> 8) & 0xFF), (hardversion & 0xFF));
    printf("当前软件版本为: v%d.%d.%d \n", (appversion >> 16) & 0xFF,
           ((appversion >> 8) & 0xFF), (appversion & 0xFF));

  } else {
    printf("警告:节点检测失败！");
    return 1;
  }
  protocol_bl.BL_ExitUpgrade();
  return 0;
}
