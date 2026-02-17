#!/usr/bin/env python3
# // coding: utf-8 
# 检查C++文件中的预处理指令是否配对

import os
import re
from pathlib import Path

def check_file(filepath):
    # 检查单个文件的预处理指令
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    stack = []
    issues = []
    
    for i, line in enumerate(lines, 1):
        # 提取预处理指令
        stripped = line.strip()
        
        # 处理 #ifdef, #ifndef, #if
        if re.match(r'^#if(def|ndef)?\s', stripped) and not stripped.startswith('#endif'):
            stack.append((stripped, i))
        
        # 处理 #else, #elif
        elif stripped.startswith('#elif') or stripped.startswith('#else'):
            if not stack:
                issues.append(f"Line {i}: {stripped} - 没有对应的 #ifdef/#ifndef")
        
        # 处理 #endif
        elif stripped.startswith('#endif'):
            if not stack:
                issues.append(f"Line {i}: #endif - 没有对应的 #ifdef/#ifndef")
            else:
                stack.pop()
    
    # 检查是否有未闭合的指令
    if stack:
        for directive, line_no in stack:
            issues.append(f"Line {line_no}: {directive} - 缺少 #endif")
    
    return issues

def main():
    """主程序"""
    core_dir = Path('core/src').resolve()
    
    print("=" * 70)
    print("检查所有 C++ 源代码文件中的预处理指令配对情况")
    print("=" * 70)
    
    total_issues = 0
    
    for cpp_file in core_dir.rglob('*.cpp'):
        issues = check_file(str(cpp_file))
        if issues:
            total_issues += len(issues)
            print(f"\n❌ {cpp_file.name}:")
            for issue in issues:
                print(f"   {issue}")
    
    for h_file in core_dir.rglob('*.h'):
        issues = check_file(str(h_file))
        if issues:
            total_issues += len(issues)
            print(f"\n❌ {h_file.name}:")
            for issue in issues:
                print(f"   {issue}")
    
    print("\n" + "=" * 70)
    if total_issues == 0:
        print("✅ 所有预处理指令都正确配对！")
    else:
        print(f"⚠️ 发现 {total_issues} 个问题")
    print("=" * 70)

if __name__ == '__main__':
    main()

