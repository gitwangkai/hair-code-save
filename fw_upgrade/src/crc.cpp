#include "crc.h"
// crc16校验
unsigned short crc16_check(const unsigned char *buf, unsigned int len) {
  unsigned int counter;
  unsigned short crc = 0;
  for (counter = 0; counter < len; counter++) {
    crc = (crc << 8) ^
          crc16tab[((crc >> 8) ^ *(const unsigned char *)buf++) & 0x00FF];
  }
  return crc;
}

unsigned short crc16_check_vector(std::vector<unsigned char> &buf) {
  unsigned int counter;
  unsigned short crc = 0;
  for (counter = 0; counter < buf.size(); counter++) {
    crc = (crc << 8) ^ crc16tab[((crc >> 8) ^ buf[counter]) & 0x00FF];
  }
  return crc;
}