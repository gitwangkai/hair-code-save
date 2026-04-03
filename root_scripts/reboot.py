import rclpy
import subprocess
from rclpy.node import Node
import time

class RebootService(Node):
    def __init__(self):
        super().__init__("reboot_service_node")
        self.get_logger().info("服务重启节点启动")
        self.count = 0
        self.timer = self.create_timer(120, self.reboot_callback)

    def reboot_callback(self):
        self.count += 1
        self.get_logger().info(f"准备重启服务 {self.count} 次")
        try:
            # 执行服务重启命令
            result = subprocess.run(
                ["sudo", "systemctl", "restart", "ros_launch.service"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=True
            )
            self.get_logger().info(f"服务重启完成 {self.count} 次")
            time.sleep(10)
            self.scan_message_echo()  # 检查话题

        except subprocess.CalledProcessError as e:
            self.get_logger().error(
                f"【执行失败】命令返回码：{e.returncode}\n错误信息：{e.stderr.strip()}"
            )
        except subprocess.TimeoutExpired:
            self.get_logger().error(f"【执行超时】命令执行超过10秒，已强制终止！")
        except Exception as e:
            self.get_logger().error(f"【未知异常】服务重启失败：{str(e)}")

    def scan_message_echo(self):
        """安全获取/scan话题消息"""
        proc = None
        try:
            # 启动ros2 topic echo命令
            proc = subprocess.Popen(
                ["ros2", "topic", "echo", "/scan"],  # 禁用守护进程避免残留
                text=True,
                shell=False,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            # 等待3秒获取输出
            stdout, stderr = proc.communicate(timeout=5)
            
            # 处理话题未发布的提示
            if "does not appear to be published yet" in stderr:
                self.get_logger().warn("/scan话题暂未发布（服务重启后可能还在初始化）")
            elif stdout:
                self.get_logger().info(f"/scan话题内容：{stdout[:500]}")  # 截断过长输出
            else:
                self.get_logger().warn("/scan话题无输出，但未检测到发布异常")
                
        except subprocess.TimeoutExpired:
            self.get_logger().warn("获取/scan话题超时（3秒），已终止")
            if proc:
                proc.terminate()  # 终止子进程
                proc.wait()       # 等待进程退出
        except Exception as e:
            self.get_logger().error(f"话题消息获取失败：{str(e)}")
        finally:
            # 安全清理子进程（核心修复点）
            if proc:
                # 检查进程是否还在运行
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=2)  # 等待2秒确保进程退出

    def destroy_node(self):
        """销毁节点时清理定时器"""
        self.timer.destroy()
        super().destroy_node()

def main():
    rclpy.init()
    node = RebootService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("节点被用户中断")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
