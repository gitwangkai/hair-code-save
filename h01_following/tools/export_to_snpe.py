#!/usr/bin/env python3
"""
tools/export_to_snpe.py
YOLOv8-pose 模型导出脚本：PyTorch → ONNX → SNPE DLC
支持 QCS8550 DSP 加速推理
"""

import argparse
import sys
from pathlib import Path

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    print("警告: ultralytics 未安装，无法导出 YOLOv8 模型")
    print("安装: pip install ultralytics")

try:
    import onnx
    from onnxsim import simplify as onnx_simplify
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    print("警告: onnx/onnxsim 未安装，无法进行 ONNX 简化")


def export_yolov8_to_onnx(
    model_name: str = "yolov8n-pose",
    output_dir: str = "models",
    imgsz: int = 640,
    simplify: bool = True
) -> Path:
    """
    导出 YOLOv8-pose 为 ONNX 格式
    
    Args:
        model_name: YOLOv8 模型名称 (yolov8n-pose/yolov8s-pose/yolov8m-pose)
        output_dir: 输出目录
        imgsz: 输入图像尺寸
        simplify: 是否简化 ONNX 模型
    
    Returns:
        导出的 ONNX 文件路径
    """
    if not ULTRALYTICS_AVAILABLE:
        raise RuntimeError("ultralytics 未安装")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"加载模型: {model_name}")
    model = YOLO(model_name)
    
    # 导出 ONNX
    onnx_file = output_path / f"{model_name}.onnx"
    
    print(f"导出 ONNX: {onnx_file}")
    model.export(
        format="onnx",
        imgsz=imgsz,
        simplify=simplify,
        opset=12,
        device="cpu"
    )
    
    # ultralytics 导出后会自动命名
    exported = Path(f"{model_name}.onnx")
    if exported.exists() and exported != onnx_file:
        exported.rename(onnx_file)
    
    print(f"ONNX 导出完成: {onnx_file}")
    
    # 额外简化（如果 ultralytics 的 simplify 不够）
    if simplify and ONNX_AVAILABLE:
        print("进一步简化 ONNX 模型...")
        onnx_model = onnx.load(onnx_file)
        onnx_model, check = onnx_simplify(onnx_model)
        if check:
            onnx.save(onnx_model, onnx_file)
            print("ONNX 简化完成")
        else:
            print("ONNX 简化失败，使用原始模型")
    
    return onnx_file


def convert_onnx_to_dlc(
    onnx_path: Path,
    output_dir: str = "models",
    quantize: bool = False,
    input_list: str = None
) -> Path:
    """
    使用 SNPE SDK 将 ONNX 转换为 DLC 格式
    
    Args:
        onnx_path: ONNX 模型路径
        output_dir: 输出目录
        quantize: 是否进行 INT8 量化
        input_list: 量化校准数据列表文件
    
    Returns:
        导出的 DLC 文件路径
    """
    import subprocess
    import shutil
    
    # 检查 SNPE SDK
    snpe_root = Path.home() / "Qualcomm" / "SNPE" / "snpe-2.x.x"
    if not snpe_root.exists():
        # 尝试查找其他版本
        snpe_dirs = list((Path.home() / "Qualcomm" / "SNPE").glob("snpe-*"))
        if snpe_dirs:
            snpe_root = snpe_dirs[0]
    
    if not snpe_root.exists():
        raise RuntimeError(
            f"SNPE SDK 未找到，请安装到 {snpe_root}\n"
            "下载地址: https://developer.qualcomm.com/software/qualcomm-neural-processing-sdk"
        )
    
    snpe_onnx_to_dlc = snpe_root / "bin" / "x86_64-linux-clang" / "snpe-onnx-to-dlc"
    if not snpe_onnx_to_dlc.exists():
        raise RuntimeError(f"SNPE 工具未找到: {snpe_onnx_to_dlc}")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    dlc_file = output_path / onnx_path.stem.replace("-pose", "-pose_quantized" if quantize else "-pose") + ".dlc"
    
    # 转换命令
    cmd = [
        str(snpe_onnx_to_dlc),
        "--input_network", str(onnx_path),
        "--output_path", str(dlc_file)
    ]
    
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"转换失败:\n{result.stderr}")
        raise RuntimeError("ONNX 转 DLC 失败")
    
    print(f"DLC 导出完成: {dlc_file}")
    
    # 量化（如果需要）
    if quantize:
        if not input_list:
            print("警告: 未提供 input_list，跳过量化")
            return dlc_file
        
        snpe_dlc_quantize = snpe_root / "bin" / "x86_64-linux-clang" / "snpe-dlc-quantize"
        
        quantized_dlc = dlc_file.with_suffix(".quantized.dlc")
        cmd = [
            str(snpe_dlc_quantize),
            "--input_dlc", str(dlc_file),
            "--input_list", input_list,
            "--output_dlc", str(quantized_dlc)
        ]
        
        print(f"执行量化: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"量化失败:\n{result.stderr}")
            return dlc_file
        
        print(f"量化完成: {quantized_dlc}")
        return quantized_dlc
    
    return dlc_file


def generate_calibration_data(
    output_dir: str = "models",
    num_samples: int = 100,
    imgsz: int = 640
) -> str:
    """
    生成量化校准数据
    
    Args:
        output_dir: 输出目录
        num_samples: 校准样本数
        imgsz: 图像尺寸
    
    Returns:
        input_list 文件路径
    """
    import numpy as np
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    raw_dir = output_path / "calibration_data"
    raw_dir.mkdir(exist_ok=True)
    
    input_list_file = output_path / "input_list.txt"
    
    with open(input_list_file, "w") as f:
        for i in range(num_samples):
            # 生成随机图像数据
            data = np.random.randn(1, 3, imgsz, imgsz).astype(np.float32)
            raw_file = raw_dir / f"calib_{i:04d}.raw"
            data.tofile(raw_file)
            f.write(f"{raw_file}\n")
    
    print(f"生成 {num_samples} 个校准样本到 {raw_dir}")
    print(f"input_list: {input_list_file}")
    
    return str(input_list_file)


def main():
    parser = argparse.ArgumentParser(
        description="YOLOv8-pose 模型导出工具"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n-pose",
        choices=["yolov8n-pose", "yolov8s-pose", "yolov8m-pose", "yolov8l-pose"],
        help="YOLOv8 模型名称"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models",
        help="输出目录"
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="输入图像尺寸"
    )
    parser.add_argument(
        "--quantize",
        action="store_true",
        help="进行 INT8 量化（需要 SNPE SDK）"
    )
    parser.add_argument(
        "--skip-onnx",
        action="store_true",
        help="跳过 ONNX 导出（已有 ONNX 文件）"
    )
    parser.add_argument(
        "--onnx-path",
        type=str,
        help="现有 ONNX 文件路径（配合 --skip-onnx 使用）"
    )
    
    args = parser.parse_args()
    
    try:
        # 导出 ONNX
        if not args.skip_onnx:
            onnx_file = export_yolov8_to_onnx(
                model_name=args.model,
                output_dir=args.output,
                imgsz=args.imgsz,
                simplify=True
            )
        else:
            onnx_file = Path(args.onnx_path or f"{args.output}/{args.model}.onnx")
        
        # 转换为 DLC（如果需要量化）
        if args.quantize:
            input_list = generate_calibration_data(args.output)
            dlc_file = convert_onnx_to_dlc(
                onnx_path=onnx_file,
                output_dir=args.output,
                quantize=True,
                input_list=input_list
            )
            print(f"\n最终模型: {dlc_file}")
        else:
            print(f"\n最终模型: {onnx_file}")
        
        print("\n导出完成！")
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
