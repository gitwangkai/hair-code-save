"""
utils/logger.py
统一日志工厂，所有模块从这里获取 logger。
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

# 日志格式
LOG_FORMAT = "%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志级别映射
LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

# 全局日志配置
_log_dir: Path = Path("logs")
_log_level: int = logging.INFO
_log_to_file: bool = False
_initialized: bool = False


def setup_logging(
    level: str = "info",
    log_dir: str = "logs",
    log_to_file: bool = False,
    log_to_console: bool = True,
):
    """
    初始化日志系统（只需调用一次）。
    
    Args:
        level: 日志级别 (debug/info/warning/error/critical)
        log_dir: 日志文件保存目录
        log_to_file: 是否写入文件
        log_to_console: 是否输出到控制台
    """
    global _log_dir, _log_level, _log_to_file, _initialized
    
    _log_level = LEVEL_MAP.get(level.lower(), logging.INFO)
    _log_dir = Path(log_dir)
    _log_to_file = log_to_file
    _initialized = True
    
    # 创建日志目录
    if _log_to_file:
        _log_dir.mkdir(parents=True, exist_ok=True)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(_log_level)
    
    # 清除已有处理器
    root_logger.handlers.clear()
    
    # 控制台处理器
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(_log_level)
        console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
    
    # 文件处理器
    if _log_to_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = _log_dir / f"h01_following_{timestamp}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(_log_level)
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    root_logger.info(f"Logging initialized: level={level}, file={_log_to_file}")


def get_logger(name: str) -> logging.Logger:
    """
    获取命名日志器。
    
    Args:
        name: 模块名称，建议使用 __name__
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    if not _initialized:
        # 自动初始化（默认配置）
        setup_logging()
    
    return logging.getLogger(name)


# 便捷函数
def set_level(level: str):
    """动态修改日志级别"""
    global _log_level
    _log_level = LEVEL_MAP.get(level.lower(), logging.INFO)
    logging.getLogger().setLevel(_log_level)


def debug(msg: str, *args, **kwargs):
    """输出调试日志"""
    logging.debug(msg, *args, **kwargs)


def info(msg: str, *args, **kwargs):
    """输出信息日志"""
    logging.info(msg, *args, **kwargs)


def warning(msg: str, *args, **kwargs):
    """输出警告日志"""
    logging.warning(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs):
    """输出错误日志"""
    logging.error(msg, *args, **kwargs)


def critical(msg: str, *args, **kwargs):
    """输出严重错误日志"""
    logging.critical(msg, *args, **kwargs)
