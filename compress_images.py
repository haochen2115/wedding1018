#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片批量压缩脚本
将指定文件夹中的图片压缩到1M以内
"""

import os
from PIL import Image
import math

def compress_image(input_path, output_path, target_size_mb=1):
    """
    压缩图片到指定大小以内
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        target_size_mb: 目标文件大小（MB）
    """
    target_size_bytes = target_size_mb * 1024 * 1024
    
    # 打开图片
    with Image.open(input_path) as img:
        # 转换为RGB模式（如果需要）
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # 获取原始尺寸
        original_width, original_height = img.size
        
        # 计算压缩质量
        quality = 95
        
        # 首先尝试降低质量
        while quality > 10:
            # 保存到临时位置测试大小
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            
            # 检查文件大小
            file_size = os.path.getsize(output_path)
            
            if file_size <= target_size_bytes:
                print(f"✓ 压缩完成: {os.path.basename(input_path)} ({file_size / (1024*1024):.2f}MB)")
                return
            
            quality -= 5
        
        # 如果降低质量还是太大，尝试缩小尺寸
        scale_factor = math.sqrt(target_size_bytes / os.path.getsize(output_path))
        new_width = int(original_width * scale_factor * 0.9)  # 稍微保守一点
        new_height = int(original_height * scale_factor * 0.9)
        
        # 缩放图片
        resized_img = img.resize((new_width, new_height), Image.Lanczos)
        
        # 再次尝试不同质量
        quality = 85
        while quality > 10:
            resized_img.save(output_path, 'JPEG', quality=quality, optimize=True)
            file_size = os.path.getsize(output_path)
            
            if file_size <= target_size_bytes:
                print(f"✓ 压缩完成: {os.path.basename(input_path)} "
                      f"({file_size / (1024*1024):.2f}MB, {new_width}x{new_height})")
                return
            
            quality -= 5
        
        print(f"⚠ 警告: {os.path.basename(input_path)} 可能无法压缩到1MB以内")

def batch_compress_images(input_folder, output_folder=None):
    """
    批量压缩文件夹中的所有图片
    
    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径（如果为None，则覆盖原文件）
    """
    if output_folder is None:
        output_folder = input_folder
    
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 支持的图片格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    
    # 获取所有图片文件
    image_files = [f for f in os.listdir(input_folder) 
                   if f.lower().endswith(supported_formats)]
    
    if not image_files:
        print("❌ 在指定文件夹中没有找到支持的图片文件")
        return
    
    print(f"📁 找到 {len(image_files)} 个图片文件")
    print("🔄 开始压缩...")
    
    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        try:
            # 检查原文件大小
            original_size = os.path.getsize(input_path) / (1024 * 1024)
            print(f"\n📷 处理: {filename} (原始大小: {original_size:.2f}MB)")
            
            if original_size <= 1:
                print(f"✓ 跳过: {filename} 已经小于1MB")
                # 如果输出路径不同，复制文件
                if input_path != output_path:
                    import shutil
                    shutil.copy2(input_path, output_path)
                continue
            
            compress_image(input_path, output_path)
            
        except Exception as e:
            print(f"❌ 处理 {filename} 时出错: {str(e)}")
    
    print("\n🎉 批量压缩完成！")

if __name__ == "__main__":
    # 输入文件夹路径
    input_folder = "/Users/ch/Desktop/MyFile/photo/邀请函链接_压缩"
    
    print("🖼️  图片批量压缩工具")
    print(f"📂 输入文件夹: {input_folder}")
    print("🎯 目标大小: 1MB以内")
    print("=" * 50)
    
    if not os.path.exists(input_folder):
        print(f"❌ 错误: 文件夹不存在 - {input_folder}")
        exit(1)
    
    # 开始批量压缩（直接覆盖原文件）
    batch_compress_images(input_folder) 