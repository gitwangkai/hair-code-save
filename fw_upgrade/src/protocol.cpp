#include "protocol.h"
#include "chrono"
#include "crc.h"
#include <cstdint>
#include <cstring>
#include <iostream>
#include <thread>

/**
 * @brief Protocol类的构造函数
 *
 * 初始化Protocol对象，并设置CAN接口。
 *
 * @param can_interface CAN接口的智能指针，用于与CAN总线进行通信。
 */
Protocol::Protocol(std::shared_ptr<CanInterface> can_interface)
    : can_interface_(can_interface) {}

Protocol::~Protocol() {}
/**
 * @brief 发送CAN消息
 *
 * 该函数将CAN消息通过CAN接口发送出去，并等待接收回显。
 *
 * @param pCanSendMsg 要发送的CAN消息指针
 * @param timeout_ms 等待回显的超时时间（毫秒）
 * @return 如果成功发送并接收到回显，则返回true；否则返回false
 */
bool Protocol::SendMsg(PCAN_MSG pCanSendMsg, int timeout_ms) {

  struct can_frame frame;

  // 填充 CAN 帧数据
  frame.can_id = pCanSendMsg->ID;
  if (pCanSendMsg->ExternFlag) {
    frame.can_id |= CAN_EFF_FLAG; // 扩展帧标志
  }
  if (pCanSendMsg->RemoteFlag) {
    frame.can_id |= CAN_RTR_FLAG; // 远程帧标志
  }
  frame.can_dlc = pCanSendMsg->DataLen;
  memcpy(frame.data, pCanSendMsg->Data, pCanSendMsg->DataLen);
  can_interface_->send_message(frame);
  while (can_interface_->read_message(frame) == true) {
    if ((frame.can_id & CAN_EFF_MASK) == (pCanSendMsg->ID & CAN_EFF_MASK)) {
      return true;
    } else if (timeout_ms <= 0) {
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
    timeout_ms -= 1;
  }

  return true;
}

/**
 * @brief 从 CAN 总线获取消息
 *
 * 从指定的 CAN 接口读取一条 CAN 消息，并将其填充到传入的 PCAN_MSG 结构中。
 *
 * @param pCanGetMsg 指向 PCAN_MSG 结构的指针，用于存储读取的 CAN 消息
 *
 * @return 成功时返回 true，失败时返回 false
 */
bool Protocol::GetMsg(PCAN_MSG pCanGetMsg) {
  struct can_frame frame;

  if (can_interface_->read_message(frame) == false) {
    return false;
  }

  // 填充接收到的 CAN 消息
  pCanGetMsg->ID = frame.can_id & CAN_EFF_MASK; // 去掉扩展帧标志
  pCanGetMsg->ExternFlag = (frame.can_id & CAN_EFF_FLAG) ? 1 : 0;
  pCanGetMsg->RemoteFlag = (frame.can_id & CAN_RTR_FLAG) ? 1 : 0;
  pCanGetMsg->DataLen = frame.can_dlc;
  memcpy(pCanGetMsg->Data, frame.data, frame.can_dlc);

  // 生成时间戳
  auto now = std::chrono::system_clock::now();
  auto now_ms = std::chrono::duration_cast<std::chrono::milliseconds>(
                    now.time_since_epoch())
                    .count();
  pCanGetMsg->TimeStamp = static_cast<unsigned int>(now_ms);

  return true;
}
/**
 * @brief 等待并获取指定ID的CAN消息
 *
 * 在指定的超时时间内，不断检查是否有新的CAN消息到达，如果有，则检查其ID是否与指定的ID匹配。
 * 如果匹配，则将消息复制到输出参数中并返回true；否则，如果在超时时间内没有找到匹配的消息，则返回false。
 *
 * @param id 需要等待的CAN消息的ID
 * @param CanGetMsg 用于存储找到的匹配消息的变量
 * @param timeout_ms 等待超时时间（毫秒）
 *
 * @return 如果在超时时间内找到了匹配的CAN消息，则返回true；否则返回false
 */
bool Protocol::WaitMsg(uint32_t id, CAN_MSG &CanGetMsg, int timeout_ms) {
  CAN_MSG CanMsg;
  while (timeout_ms > 0) {
    while (GetMsg(&CanMsg) == false) {
      std::this_thread::sleep_for(std::chrono::milliseconds(1));
      timeout_ms -= 1;
      if (timeout_ms <= 0) {
        return false;
      }
    }
    if (CanMsg.ID == id) {
      CanGetMsg = CanMsg;
      return true;
    }
  }
  return false;
}
/**
 * @brief 等待接收指定ID的CAN消息
 *
 * 在指定的超时时间内，等待接收指定ID的CAN消息。
 *
 * @param id1 第一个等待接收的消息ID
 * @param id2 第二个等待接收的消息ID
 * @param CanGetMsg 用于存储接收到的CAN消息的变量
 * @param timeout_ms 超时时间，单位：毫秒
 *
 * @return 如果在超时时间内接收到指定ID的消息，则返回true；否则返回false
 */
bool Protocol::WaitMsg(uint32_t id1, uint32_t id2, CAN_MSG &CanGetMsg,
                       int timeout_ms) {
  CAN_MSG CanMsg;
  while (timeout_ms > 0) {
    while (GetMsg(&CanMsg) == false) {
      std::this_thread::sleep_for(std::chrono::milliseconds(1));
      timeout_ms -= 1;
      if (timeout_ms <= 0) {
        return false;
      }
    }
    if (CanMsg.ID == id1 || CanMsg.ID == id2) {
      CanGetMsg = CanMsg;
      return true;
    }
  }
  return false;
}

bool Protocol::GetStatus(PCAN_STATUS pCANStatus) { return true; }

/**
 * @brief 初始化协议栈
 *
 * 初始化协议栈，配置CAN接口和命令列表。
 *
 * @param DevHandle 设备句柄，用于标识设备。
 * @param CANIndex CAN索引，用于指定要使用的CAN接口。
 * @param pInitConfig 指向PCAN_INIT_CONFIG结构体的指针，用于配置CAN接口参数。
 * @param pCmdList 指向PCBL_CMD_LIST结构体的指针，用于指定命令列表。
 *
 * @return 返回值始终为1，表示初始化成功。
 */
int Protocol::BL_Init(PCAN_INIT_CONFIG pInitConfig, PCBL_CMD_LIST pCmdList) {

  return 1;
}

/**protocol_bl
 * @brief 节点检查函数
 *
 * 该函数用于通过CAN总线发送节点检查命令，并接收节点返回的硬件版本、软件版本和类型信息。
 *
 * @param DevHandle 设备句柄
 * @param CANIndex CAN索引
 * @param NodeAddr 节点地址
 * @param pHardVersion 指向用于存储硬件版本的指针
 * @param pSoftVersion 指向用于存储软件版本的指针
 * @param pType 指向用于存储节点类型的指针
 * @param TimeOut 超时时间（毫秒）
 *
 * @return 返回值表示函数执行结果。返回CAN_SUCCESS表示成功，其他值表示失败。
 */
int Protocol::BL_NodeCheck(unsigned short NodeAddr, unsigned int *pHardVersion,
                           unsigned int *pSoftVersion, unsigned int *pType,
                           unsigned int TimeOut) {

  CAN_MSG CanGetMsg, CanSendMsg;

  unsigned short MsgNodeAddr, MsgTargAddr, cmd;
  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (Check << 16);
  CanSendMsg.DataLen = 0;
  CanSendMsg.RemoteFlag = 1;
  CanSendMsg.ExternFlag = 1;
  int send_cnt = 0;
  while (send_cnt < 3) {
    send_cnt++;
    if (SendMsg(&CanSendMsg, 10) == false) {
      if (send_cnt >= 2)
        return CAN_BL_ERR_SEND;
      else
        continue;
    }
    uint32_t wait_id = NodeAddr | (LOCAL_ID << 8) | (Check << 16);

    if (WaitMsg(wait_id, CanGetMsg, TimeOut / 3) == false) {
      if (send_cnt >= 3)
        return CAN_BL_ERR_TIME_OUT;
      else
        continue;
    } else {
      break;
    }
  }

  *pHardVersion = (CanGetMsg.Data[0] << 16) | (CanGetMsg.Data[1] << 8) |
                  (CanGetMsg.Data[2]);
  *pSoftVersion = (CanGetMsg.Data[3] << 16) | (CanGetMsg.Data[4] << 8) |
                  (CanGetMsg.Data[5]);
  *pType = (CanGetMsg.Data[7] << 8) | (CanGetMsg.Data[6]);
  return CAN_SUCCESS;
}

/**
 * @brief 擦除设备上的Flash存储
 *
 * 该函数通过CAN总线向指定节点发送擦除Flash存储的命令，并等待节点的响应。
 *
 * @param DevHandle 设备句柄，表示与设备的连接。
 * @param CANIndex CAN总线索引，表示通过哪条CAN总线发送命令。
 * @param NodeAddr 目标节点的地址。
 * @param FlashSize 需要擦除的Flash大小，以字节为单位。
 * @param TimeOut 等待响应的超时时间，以毫秒为单位。
 *
 * @return 返回执行结果，具体返回值如下：
 *   - CAN_SUCCESS: 命令执行成功。
 *   - CAN_BL_ERR_SEND: 发送命令失败。
 *   - CAN_BL_ERR_TIME_OUT: 等待响应超时。
 *   - CAN_ERR_CMD_FAIL: 命令执行失败。
 */
int Protocol::BL_Erase(unsigned short NodeAddr, unsigned int FlashSize,
                       unsigned int TimeOut) {

  CAN_MSG CanGetMsg, CanSendMsg;

  unsigned short MsgNodeAddr, MsgTargAddr, cmd;
  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (Erase << 16);
  CanSendMsg.DataLen = 4;
  CanSendMsg.RemoteFlag = 0;
  CanSendMsg.ExternFlag = 1;
  CanSendMsg.Data[0] = (FlashSize >> 24) & 0xff;
  CanSendMsg.Data[1] = (FlashSize >> 16) & 0xff;
  CanSendMsg.Data[2] = (FlashSize >> 8) & 0xff;
  CanSendMsg.Data[3] = (FlashSize >> 0) & 0xff;

  int send_cnt = 0;
  while (send_cnt < 3) {
    send_cnt++;
    if (SendMsg(&CanSendMsg, 10) == false)
      return CAN_BL_ERR_SEND;

    uint32_t wait_id1 = NodeAddr | (LOCAL_ID << 8) | (CmdSuccess << 16);
    uint32_t wait_id2 = NodeAddr | (LOCAL_ID << 8) | (CmdFaild << 16);

    if (WaitMsg(wait_id1, wait_id2, CanGetMsg, TimeOut) == false) {
      return CAN_BL_ERR_TIME_OUT;
    } else {
      break;
    }
  }

  if (((CanGetMsg.ID >> 16) & 0xff) == CmdSuccess)
    return CAN_SUCCESS;
  else
    return CAN_ERR_CMD_FAIL;
}
/**
 * @brief 向指定节点写入信息
 *
 * 通过CAN总线向指定节点写入指定地址偏移量处的一定数量的数据。
 *
 * @param NodeAddr 目标节点地址
 * @param AddrOffset 地址偏移量
 * @param DataNum 要写入的数据数量
 * @param TimeOut 超时时间（单位：毫秒）
 *
 * @return 写入结果，具体返回值如下：
 *         - CAN_SUCCESS：写入成功
 *         - CAN_ERR_CMD_FAIL：命令执行失败
 *         - CAN_BL_ERR_SEND：发送失败
 *         - CAN_BL_ERR_TIME_OUT：超时
 */
int Protocol::BL_Write_Info(unsigned short NodeAddr, unsigned int AddrOffset,
                            unsigned int DataNum, unsigned int TimeOut) {
  CAN_MSG CanGetMsg, CanSendMsg;

  unsigned short MsgNodeAddr, MsgTargAddr, cmd;
  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (WriteInfo << 16);
  CanSendMsg.DataLen = 8;
  CanSendMsg.RemoteFlag = 0;
  CanSendMsg.ExternFlag = 1;
  CanSendMsg.Data[0] = (AddrOffset >> 24) & 0xff;
  CanSendMsg.Data[1] = (AddrOffset >> 16) & 0xff;
  CanSendMsg.Data[2] = (AddrOffset >> 8) & 0xff;
  CanSendMsg.Data[3] = (AddrOffset >> 0) & 0xff;
  CanSendMsg.Data[4] = (DataNum >> 24) & 0xff;
  CanSendMsg.Data[5] = (DataNum >> 16) & 0xff;
  CanSendMsg.Data[6] = (DataNum >> 8) & 0xff;
  CanSendMsg.Data[7] = (DataNum >> 0) & 0xff;
  int send_cnt = 0;
  while (send_cnt < 3) {
    send_cnt++;
    if (SendMsg(&CanSendMsg, 10) == false)
      return CAN_BL_ERR_SEND;
    uint32_t wait_id1 = NodeAddr | (LOCAL_ID << 8) | (CmdSuccess << 16);
    uint32_t wait_id2 = NodeAddr | (LOCAL_ID << 8) | (CmdFaild << 16);

    if (WaitMsg(wait_id1, wait_id2, CanGetMsg, TimeOut) == false) {
      continue;
    }
    cmd = (CanGetMsg.ID >> 16) & 0xff;
    if (cmd == CmdSuccess)
      return CAN_SUCCESS;
    if (cmd == CmdFaild)
      return CAN_ERR_CMD_FAIL;
  }

  return CAN_BL_ERR_TIME_OUT;
}
/**
 * @brief 向指定节点写入数据
 *
 * 该函数通过CAN总线向指定节点写入数据。
 *
 * @param NodeAddr 节点地址
 * @param index 数据索引
 * @param pData 要写入的数据指针
 * @param DataNum 要写入的数据长度
 *
 * @return 写入结果，成功返回CAN_SUCCESS，失败返回CAN_BL_ERR_SEND
 */
int Protocol::BL_Write_Data(unsigned short NodeAddr, uint8_t index,
                            unsigned char *pData, unsigned int DataNum) {
  CAN_MSG CanSendMsg;

  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (Write << 16);
  CanSendMsg.DataLen = DataNum + 1;
  CanSendMsg.RemoteFlag = 0;
  CanSendMsg.ExternFlag = 1;
  CanSendMsg.Data[0] = index;
  memcpy(CanSendMsg.Data + 1, pData, DataNum);
  if (SendMsg(&CanSendMsg, 10) == false)
    return CAN_BL_ERR_SEND;
  return CAN_SUCCESS;
}
/**
 * @brief 进入升级模式
 *
 * 该函数用于使设备进入升级模式。
 *
 * @return 返回操作结果，成功返回 CAN_SUCCESS，失败返回 CAN_BL_ERR_SEND。
 */
int Protocol::BL_EnterUpgrade() {
  CAN_MSG CanSendMsg;

  CanSendMsg.ID = 0xff << 8 | LOCAL_ID | (EnterUpgrade << 16);
  CanSendMsg.DataLen = 0;
  CanSendMsg.RemoteFlag = 1;
  CanSendMsg.ExternFlag = 1;
  if (SendMsg(&CanSendMsg, 10) == false)
    return CAN_BL_ERR_SEND;
  return CAN_SUCCESS;
}
/**指令类型
 * @brief 退出升级协议
 *
 * 发送退出升级指令到CAN总线
 *
 * @return 返回值表示发送结果：
 *         - CAN_SUCCESS: 发送成功
 *         - CAN_BL_ERR_SEND: 发送失败
 */
int Protocol::BL_ExitUpgrade() {
  CAN_MSG CanSendMsg;

  CanSendMsg.ID = 0xff << 8 | LOCAL_ID | (ExitUpgrade << 16);
  CanSendMsg.DataLen = 0;
  CanSendMsg.RemoteFlag = 1;
  CanSendMsg.ExternFlag = 1;
  if (SendMsg(&CanSendMsg, 10) == false)
    return CAN_BL_ERR_SEND;

  return CAN_SUCCESS;
}

/**
 * @brief 向指定设备写入数据
 *
 * 该函数用于向指定的设备地址写入数据，支持分块传输和CRC校验。
 *
 * @param DevHandle 设备句柄
 * @param CANIndex CAN通道索引
 * @param NodeAddr 设备节点地址
 * @param AddrOffset 地址偏移量
 * @param pData 指向要写入的数据的指针
 * @param DataNum 要写入的数据字节数
 * @param TimeOut 超时时间（毫秒）
 *
 * @return 返回操作结果
 *         - CAN_SUCCESS: 操作成功
 *         - CAN_BL_ERR_SEND: 发送数据失败
 *         - CAN_BL_ERR_TIME_OUT: 超时
 *         - CAN_ERR_CMD_FAIL: 命令执行失败
 */
int Protocol::BL_Write(unsigned short NodeAddr, unsigned int AddrOffset,
                       unsigned char *pData, unsigned int DataNum,
                       unsigned int TimeOut) {

  CAN_MSG CanGetMsg;
  int package_num;
  int end_num;

  unsigned char sendbuff[1026] = {0};
  int sendsize = DataNum + 2;
  package_num = sendsize / 7;
  end_num = sendsize % 7;
  memcpy(sendbuff, pData, DataNum);
  unsigned short crc16 = crc16_check((const unsigned char *)sendbuff, DataNum);
  sendbuff[sendsize - 2] = crc16 >> 8;
  sendbuff[sendsize - 1] = crc16;
  if (BL_Write_Info(NodeAddr, AddrOffset, sendsize, 100) != CAN_SUCCESS) {
    return CAN_BL_ERR_SEND;
  }

  for (int i = 0; i < package_num; i++) {
    if (BL_Write_Data(NodeAddr, i, sendbuff + i * 7, 7) == CAN_BL_ERR_SEND)
      return CAN_BL_ERR_SEND;
  }
  if (BL_Write_Data(NodeAddr, package_num, sendbuff + package_num * 7,
                    end_num) == CAN_BL_ERR_SEND)
    return CAN_BL_ERR_SEND;

  uint32_t wait_id1 = NodeAddr | (LOCAL_ID << 8) | (CmdSuccess << 16);
  uint32_t wait_id2 = NodeAddr | (LOCAL_ID << 8) | (CmdFaild << 16);

  if (WaitMsg(wait_id1, wait_id2, CanGetMsg, TimeOut) == false) {
    return CAN_BL_ERR_TIME_OUT;
  }
  uint8_t cmd = (CanGetMsg.ID >> 16) & 0xff;
  if (cmd == CmdSuccess)
    return CAN_SUCCESS;
  if (cmd == CmdFaild) {
    std::cerr << "Write data crc error " << std::endl;
  }

  return CAN_ERR_CMD_FAIL;
}

/**
 * @brief 执行跳转app or bootloader
 *
 * 通过CAN总线向指定设备发送执行指令。
 *
 * @param DevHandle 设备句柄
 * @param CANIndex CAN总线索引
 * @param NodeAddr 目标节点地址
 * @param Type app or bootloader
 *
 * @return 执行结果
 * - CAN_SUCCESS: 执行成功
 * - CAN_BL_ERR_SEND: 发送消息失败
 */
int Protocol::BL_Excute(unsigned short NodeAddr, unsigned int Type) {
  CAN_MSG CanGetMsg, CanSendMsg;

  unsigned short MsgNodeAddr, MsgTargAddr;
  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (Excute << 16);
  CanSendMsg.DataLen = 4;
  CanSendMsg.RemoteFlag = 0;
  CanSendMsg.ExternFlag = 1;
  CanSendMsg.Data[0] = (Type >> 24) & 0xff;
  CanSendMsg.Data[1] = (Type >> 16) & 0xff;
  CanSendMsg.Data[2] = (Type >> 8) & 0xff;
  CanSendMsg.Data[3] = (Type >> 0) & 0xff;
  if (SendMsg(&CanSendMsg, 10) == false)
    return CAN_BL_ERR_SEND;

  return CAN_SUCCESS;
}

int Protocol::BL_SetNewBaudRate(unsigned short NodeAddr,
                                PCAN_INIT_CONFIG pInitConfig,
                                unsigned int NewBaudRate,
                                unsigned int TimeOut) {
  return 1;
}

/**
 * @brief 发送写操作完成消息
 *
 * 该函数用于发送一个写操作完成的消息，并等待目标设备的响应。
 *
 * @param DevHandle 设备句柄
 * @param CANIndex CAN通道索引
 * @param NodeAddr 目标设备节点地址
 * @param crc_16 CRC校验值
 * @param sw 软件版本号
 * @param TimeOut 超时时间（毫秒）
 *
 * @return 返回操作结果
 *         - CAN_SUCCESS：操作成功
 *         - CAN_BL_ERR_SEND：发送消息失败
 *         - CAN_BL_ERR_TIME_OUT：等待响应超时
 *         - CAN_ERR_CMD_FAIL：命令执行失败
 */
int Protocol::BL_WriteFinish(unsigned short NodeAddr, uint16_t crc_16,
                             uint32_t sw, unsigned int TimeOut) {
  CAN_MSG CanGetMsg, CanSendMsg;

  unsigned short MsgNodeAddr, MsgTargAddr;
  CanSendMsg.ID = NodeAddr << 8 | LOCAL_ID | (WriteFinish << 16);
  CanSendMsg.DataLen = 5;
  CanSendMsg.RemoteFlag = 0;
  CanSendMsg.ExternFlag = 1;
  CanSendMsg.Data[0] = (crc_16) & 0xff;
  CanSendMsg.Data[1] = (crc_16 >> 8) & 0xff;
  CanSendMsg.Data[2] = (sw) & 0xff;
  CanSendMsg.Data[3] = (sw >> 8) & 0xff;
  CanSendMsg.Data[4] = (sw >> 16) & 0xff;
  if (SendMsg(&CanSendMsg, 10) == false)
    return CAN_BL_ERR_SEND;

  uint32_t wait_id1 = NodeAddr | (LOCAL_ID << 8) | (CmdSuccess << 16);
  uint32_t wait_id2 = NodeAddr | (LOCAL_ID << 8) | (CmdFaild << 16);

  if (WaitMsg(wait_id1, wait_id2, CanGetMsg, TimeOut) == false) {
    return CAN_BL_ERR_TIME_OUT;
  }

  uint8_t cmd = (CanGetMsg.ID >> 16) & 0xff;
  if (cmd == CmdSuccess)
    return CAN_SUCCESS;
  if (cmd == CmdFaild) {
    std::cerr << "Write finish error " << std::endl;
    if (CanGetMsg.Data[0] == BOOT_ERROR_NOT_WRITEINFO) {
      std::cerr << "BOOT_ERROR_NOT_WRITEINFO" << std::endl;
    }
    if (CanGetMsg.Data[0] == BOOT_ERROR_CRC16_BACKUP) {
      std::cerr << "BOOT_ERROR_CRC16_BACKUP" << std::endl;
    }
    if (CanGetMsg.Data[0] == BOOT_ERROR_WRITEINFO) {
      std::cerr << "BOOT_ERROR_WRITEINFO" << std::endl;
    }
    if (CanGetMsg.Data[0] == BOOT_ERROR_COPY_TO_APP) {
      std::cerr << "BOOT_ERROR_COPY_TO_APP" << std::endl;
    }
  }

  return CAN_ERR_CMD_FAIL;
}
