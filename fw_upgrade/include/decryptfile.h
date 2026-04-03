#ifndef DECRYPTFILE_H
#define DECRYPTFILE_H
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstdint>
class DecryptFile {
public:
  DecryptFile();
  bool StartDecryptFile(std::string encrypted_file, std::string password);
  int GetCanId();
  bool DecryptAES(const std::string &encryptedData, std::string password,
                  std::vector<unsigned char> &decryptedData);
  bool ExtractTar(const std::vector<unsigned char> &data,
                  std::unordered_map<std::string, std::vector<unsigned char>>
                      &file_contents);
  bool GetBinFile(const std::string filename);
  void GetBinSv(uint8_t *sv);
  void GetBinHv(uint8_t *hv);
  bool GetBinData(std::vector<unsigned char> &data);

protected:
  std::vector<unsigned char> decrypted_data;
  std::unordered_map<std::string, std::vector<unsigned char>> file_contents;
  std::string filename;
  int can_id;
  int size;
  uint8_t sv_[3];
  uint8_t hv_[3];
  std::string checksum;
};
int testDecrypt();

#endif // DECRYPTFILE_H
