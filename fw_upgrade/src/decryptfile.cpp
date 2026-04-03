#include "decryptfile.h"
#include <fstream>
#include <sstream>
#include <string>

#include <archive.h>
#include <archive_entry.h>
#include <openssl/evp.h>
#include <openssl/md5.h>
#include <openssl/rand.h>
#include <regex>
#include <cstring>
// 解密函数
bool DecryptFile::DecryptAES(const std::string &encrypted_file,
                             std::string password,
                             std::vector<unsigned char> &decrypted_data) {
  std::cout << "Decryptfile:" << encrypted_file << " password:" << password
            << std::endl;

  // 打开输入的加密文件
  std::ifstream infile(encrypted_file, std::ios::binary);
  if (!infile) {
    std::cerr << "无法打开加密文件。" << std::endl;
    return false;
  }

  // 读取并验证盐前缀
  const int salt_prefix_len = 8;
  const std::string salt_prefix = "Salted__";
  char prefix[salt_prefix_len];
  infile.read(prefix, salt_prefix_len);
  if (std::string(prefix, salt_prefix_len) != salt_prefix) {
    std::cerr << "无效的盐前缀，文件格式可能不正确。" << std::endl;
    return false;
  }

  // 读取实际的盐
  unsigned char salt[8];
  infile.read(reinterpret_cast<char *>(salt), sizeof(salt));

  // 从密码和盐生成密钥和 IV
  unsigned char key[32], iv[16];
  if (!EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha256(), salt,
                      reinterpret_cast<const unsigned char *>(password.data()),
                      password.size(), 1, key, iv)) {
    std::cerr << "生成密钥和 IV 失败。" << std::endl;
    return false;
  }

  // 初始化解密上下文
  EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
  if (!ctx) {
    std::cerr << "创建加密上下文失败。" << std::endl;
    return false;
  }
  if (EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv) != 1) {
    EVP_CIPHER_CTX_free(ctx);
    std::cerr << "解密初始化失败。" << std::endl;
    return false;
  }

  // 解密并存储数据
  std::vector<unsigned char> inbuf(4096),
      outbuf(4096 + EVP_CIPHER_block_size(EVP_aes_256_cbc()));
  int outlen;

  while (infile.read(reinterpret_cast<char *>(inbuf.data()), inbuf.size()) ||
         infile.gcount() > 0) {
    if (EVP_DecryptUpdate(ctx, outbuf.data(), &outlen, inbuf.data(),
                          infile.gcount()) != 1) {
      std::cerr << "解密过程失败。" << std::endl;
      EVP_CIPHER_CTX_free(ctx);
      return false;
    }
    decrypted_data.insert(decrypted_data.end(), outbuf.begin(),
                          outbuf.begin() + outlen);
  }

  // 解密的最终化处理
  if (EVP_DecryptFinal_ex(ctx, outbuf.data(), &outlen) != 1) {
    std::cerr << "解密的最终化失败。" << std::endl;
    EVP_CIPHER_CTX_free(ctx);
    return false;
  }
  decrypted_data.insert(decrypted_data.end(), outbuf.begin(),
                        outbuf.begin() + outlen);

  EVP_CIPHER_CTX_free(ctx);
  return true;
}

// 解压并将文件内容存储在内存中
bool DecryptFile::ExtractTar(
    const std::vector<unsigned char> &data,
    std::unordered_map<std::string, std::vector<unsigned char>>
        &file_contents) {
  struct archive *a = archive_read_new();
  struct archive_entry *entry;
  archive_read_support_format_tar(a);

  if (archive_read_open_memory(a, data.data(), data.size()) != ARCHIVE_OK) {
    std::cerr << "无法读取 tar 数据。" << std::endl;
    archive_read_free(a);
    return false;
  }

  while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
    const char *filename = archive_entry_pathname(entry);
    std::vector<unsigned char> content;

    const void *buff;
    size_t size;
    int64_t offset;
    while (archive_read_data_block(a, &buff, &size, &offset) == ARCHIVE_OK) {
      content.insert(content.end(), static_cast<const unsigned char *>(buff),
                     static_cast<const unsigned char *>(buff) + size);
    }

    file_contents[filename] = std::move(content);
  }

  archive_read_free(a);
  return true;
}
// 从 info.txt 中提取文件信息
bool extract_info(const std::string &info_content, std::string &filename,
                  std::string &expected_md5, int &can_id, uint8_t sv[3],
                  uint8_t hv[3]) {
  // Updated regex pattern to match the multi-line structure of info.txt
  std::regex info_regex(
      R"(Filename:\s+(\S+)\s+Can_id:\s+(\d+)\s+SV:\s+v(\d+)\.(\d+)\.(\d+)\s+HV:\s+v(\d+)\.(\d+)\.(\d+)\s+Size:\s+\d+\s+([a-fA-F0-9]{32})\s+\S+)");

  std::smatch match;
  if (std::regex_search(info_content, match, info_regex)) {
    filename = match[1];          // Extract Filename
    can_id = std::stoi(match[2]); // Extract and convert Can_id
    expected_md5 = match[9];      // Extract MD5 checksum

    // Extract and store SV and HV version numbers in uint8_t arrays
    sv[0] = static_cast<uint8_t>(std::stoi(match[3])); // SV major version
    sv[1] = static_cast<uint8_t>(std::stoi(match[4])); // SV minor version
    sv[2] = static_cast<uint8_t>(std::stoi(match[5])); // SV patch version

    hv[0] = static_cast<uint8_t>(std::stoi(match[6])); // HV major version
    hv[1] = static_cast<uint8_t>(std::stoi(match[7])); // HV minor version
    hv[2] = static_cast<uint8_t>(std::stoi(match[8])); // HV patch version

    return true;
  }
  return false;
}
// 计算文件的 MD5 校验值
std::string CalculateMd5(const std::vector<unsigned char> &data) {
  unsigned char md5_digest[MD5_DIGEST_LENGTH];
  MD5(data.data(), data.size(), md5_digest);

  // 将 MD5 转为字符串
  char md5_string[MD5_DIGEST_LENGTH * 2 + 1];
  for (int i = 0; i < MD5_DIGEST_LENGTH; ++i) {
    sprintf(&md5_string[i * 2], "%02x", md5_digest[i]);
  }
  return std::string(md5_string);
}

DecryptFile::DecryptFile() {}

bool DecryptFile::StartDecryptFile(std::string encrypted_file,
                                   std::string password) {
  //    std::string encrypted_file =
  //    "/home/dongfang/code/VCU/cube_vcu/app/build/Debug/cube_vcu_app.tar.enc";
  //    std::string password = "sator@2048!";

  if (DecryptAES(encrypted_file, password, decrypted_data)) {
    std::cout << "解密成功，开始解包 tar 文件..." << std::endl;
    if (ExtractTar(decrypted_data, file_contents)) {
      std::cout << "tar 文件提取成功。" << std::endl;

      // 查找并读取 info.txt
      if (file_contents.count("info.txt")) {
        std::string info_content(
            reinterpret_cast<const char *>(file_contents["info.txt"].data()),
            file_contents["info.txt"].size());
        std::string expected_md5;

        // 从 info.txt 中提取文件名和 MD5 校验值
        if (extract_info(info_content, filename, expected_md5, can_id, sv_,
                         hv_)) {
          std::cout << "从 info.txt 提取的文件名: " << filename
                    << ", MD5: " << expected_md5 << std::endl;

          // 查找并验证目标文件
          if (file_contents.count(filename)) {
            std::string calculated_md5 = CalculateMd5(file_contents[filename]);
            std::cout << "计算的 MD5: " << calculated_md5 << std::endl;

            // 比较 MD5 校验值
            if (expected_md5 == calculated_md5) {
              std::cout << "MD5 校验通过，文件完整。" << std::endl;
              return true;
            } else {
              std::cerr << "MD5 校验失败，文件可能已损坏。" << std::endl;
            }
          } else {
            std::cerr << "tar 文件中未找到指定的二进制文件: " << filename
                      << std::endl;
          }
        } else {
          std::cerr << "未能从 info.txt 提取文件信息。" << std::endl;
        }
      } else {
        std::cerr << "找不到 info.txt 文件。" << std::endl;
      }
    } else {
      std::cerr << "tar 文件提取失败。" << std::endl;
    }
  } else {
    std::cerr << "解密失败。" << std::endl;
  }
  return false;
}
int DecryptFile::GetCanId() { return can_id; }

bool DecryptFile::GetBinFile(const std::string out_filename) {
  // 检查文件是否存在于 file_contents 中
  if (file_contents.count(filename) == 0) {
    std::cerr << "文件内容未找到: " << filename << std::endl;
    return false;
  }

  // 打开文件以写入
  std::ofstream firmwareFile(out_filename, std::ios::binary);
  if (!firmwareFile.is_open()) {
    std::cerr << "无法打开文件以写入: " << out_filename << std::endl;
    return false;
  }

  // 获取数据并写入文件
  const std::vector<unsigned char> &bin_data = file_contents[filename];
  firmwareFile.write(reinterpret_cast<const char *>(bin_data.data()),
                     bin_data.size());

  // 关闭文件
  firmwareFile.close();
  return true;
}
void DecryptFile::GetBinSv(uint8_t *sv) { memcpy(sv, sv_, 3); }

void DecryptFile::GetBinHv(uint8_t *hv) { memcpy(hv, hv_, 3); }

bool DecryptFile::GetBinData(std::vector<unsigned char> &data) {
  if (file_contents.count(filename) == 0) {
    std::cerr << "文件内容未找到: " << filename << std::endl;
    return false;
  }
  const std::vector<unsigned char> &bin_data = file_contents[filename];
  std::cout << "bin data size: " << bin_data.size() << std::endl;
  data = bin_data;
  return true;
}