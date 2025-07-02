#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Issues Management System - Main Application
نظام إدارة مشاكل العملاء - التطبيق الرئيسي

Version: 3.0.0
Author: AI Assistant
Date: December 2024
"""

# Version information
VERSION = "3.0.0"

import sys
import os
import logging
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import shutil
import platform
import time

# إعداد المسارات
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# إعداد نظام السجلات
def setup_logging():
    """إعداد نظام السجلات"""
    log_dir = os.path.join(CURRENT_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'customer_issues_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def check_requirements():
    """فحص المتطلبات الأساسية"""
    logging.info("فحص متطلبات النظام...")
    
    # فحص إصدار Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        error_msg = f"يتطلب النظام Python 3.7 أو أحدث. الإصدار الحالي: {python_version.major}.{python_version.minor}"
        logging.error(error_msg)
        messagebox.showerror("خطأ في المتطلبات", error_msg)
        return False
    
    # فحص المكتبات المطلوبة
    required_modules = ['tkinter', 'sqlite3', 'datetime', 'shutil', 'platform']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = f"المكتبات التالية مفقودة: {', '.join(missing_modules)}"
        logging.error(error_msg)
        messagebox.showerror("خطأ في المتطلبات", error_msg)
        return False
    
    logging.info("✅ تم فحص جميع المتطلبات بنجاح")
    return True

def create_backup():
    """إنشاء نسخة احتياطية"""
    try:
        backup_dir = os.path.join(CURRENT_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        db_path = os.path.join(CURRENT_DIR, 'customer_issues_enhanced.db')
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f'customer_issues_backup_{timestamp}.db')
            shutil.copy2(db_path, backup_path)
            logging.info(f"تم إنشاء نسخة احتياطية: {backup_path}")
            
            # تنظيف النسخ القديمة (الاحتفاظ بـ 10 نسخ)
            backup_files = [f for f in os.listdir(backup_dir) if f.startswith('customer_issues_backup_')]
            if len(backup_files) > 10:
                backup_files.sort()
                for old_backup in backup_files[:-10]:
                    old_path = os.path.join(backup_dir, old_backup)
                    os.remove(old_path)
                    logging.info(f"تم حذف النسخة الاحتياطية القديمة: {old_backup}")
        
        return True
    except Exception as e:
        logging.error(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
        return False

def initialize_system():
    """تهيئة النظام"""
    logging.info("بدء تهيئة النظام...")
    
    # إنشاء المجلدات الأساسية
    dirs_to_create = ['files', 'backups', 'reports', 'logs']
    for dir_name in dirs_to_create:
        dir_path = os.path.join(CURRENT_DIR, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"تم إنشاء/فحص المجلد: {dir_path}")
    
    # إنشاء نسخة احتياطية
    create_backup()
    
    # تهيئة قاعدة البيانات
    try:
        from customer_issues_database import DatabaseManager
        db_manager = DatabaseManager()
        db_manager.init_database()
        logging.info("✅ تم تهيئة قاعدة البيانات بنجاح")
    except Exception as e:
        logging.error(f"خطأ في تهيئة قاعدة البيانات: {e}")
        messagebox.showerror("خطأ في قاعدة البيانات", f"فشل في تهيئة قاعدة البيانات:\n{e}")
        return False
    
    logging.info("✅ تم تهيئة النظام بنجاح")
    return True

def show_splash_screen():
    """عرض شاشة البداية"""
    splash = tk.Toplevel()
    splash.title("نظام إدارة مشاكل العملاء")
    splash.geometry("600x400")
    splash.resizable(False, False)
    
    # توسيط النافذة
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (600 // 2)
    y = (splash.winfo_screenheight() // 2) - (400 // 2)
    splash.geometry(f"600x400+{x}+{y}")
    
    # إزالة أزرار النافذة
    splash.overrideredirect(True)
    
    # الخلفية
    main_frame = tk.Frame(splash, bg='#2c3e50', padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # العنوان الرئيسي
    title_label = tk.Label(
        main_frame,
        text="نظام إدارة مشاكل العملاء",
        font=('Arial', 24, 'bold'),
        fg='white',
        bg='#2c3e50'
    )
    title_label.pack(pady=(40, 10))
    
    # العنوان الفرعي
    subtitle_label = tk.Label(
        main_frame,
        text="Customer Issues Management System",
        font=('Arial', 14),
        fg='#bdc3c7',
        bg='#2c3e50'
    )
    subtitle_label.pack(pady=(0, 30))
    
    # الإصدار
    version_label = tk.Label(
        main_frame,
        text="الإصدار 3.0.0 - النسخة المحسنة",
        font=('Arial', 12),
        fg='#3498db',
        bg='#2c3e50'
    )
    version_label.pack(pady=(0, 5))

    # اسم المطور تحت الإصدار
    dev_name_label = tk.Label(
        main_frame,
        text="مصطفى اسماعيل",
        font=('Arial', 12, 'bold'),
        fg='#e67e22',
        bg='#2c3e50'
    )
    dev_name_label.pack(pady=(0, 15))
    
    # معلومات النظام
    info_text = """
    نظام شامل لإدارة مشاكل وشكاوى عملاء شركات الغاز
    
    ✓ إدارة بيانات العملاء والمشاكل
    ✓ تتبع المراسلات مع الترقيم المزدوج
    ✓ رفع وإدارة المرفقات
    ✓ بحث متقدم وتقارير شاملة
    ✓ نسخ احتياطية تلقائية
    """
    
    info_label = tk.Label(
        main_frame,
        text=info_text,
        font=('Arial', 10),
        fg='#ecf0f1',
        bg='#2c3e50',
        justify='center'
    )
    info_label.pack(pady=20)
    
    # شريط التحميل
    progress_frame = tk.Frame(main_frame, bg='#2c3e50')
    progress_frame.pack(pady=(20, 10))
    
    progress_label = tk.Label(
        progress_frame,
        text="جاري تحميل النظام...",
        font=('Arial', 10),
        fg='#95a5a6',
        bg='#2c3e50'
    )
    progress_label.pack()
    
    # معلومات المطور
    dev_label = tk.Label(
        main_frame,
        text="تطوير: مساعد الذكي الاصطناعي - 2024",
        font=('Arial', 8),
        fg='#7f8c8d',
        bg='#2c3e50'
    )
    dev_label.pack(side='bottom', pady=(20, 0))
    
    # تحديث النافذة
    splash.update()
    
    return splash

def main():
    """الوظيفة الرئيسية"""
    # إعداد نظام السجلات
    setup_logging()
    
    logging.info("=" * 50)
    logging.info("بدء تشغيل نظام إدارة مشاكل العملاء v3.0.0")
    logging.info(f"نظام التشغيل: {platform.system()} {platform.release()}")
    logging.info(f"إصدار Python: {sys.version}")
    logging.info("=" * 50)
    
    # إنشاء نافذة root مخفية
    root = tk.Tk()
    root.withdraw()
    
    try:
        # عرض شاشة البداية
        splash = show_splash_screen()
        splash.update()
        
        # فحص المتطلبات
        if not check_requirements():
            splash.destroy()
            return 1
        
        # تهيئة النظام
        splash.update()
        if not initialize_system():
            splash.destroy()
            return 1
        
        # استيراد وتشغيل الواجهة الرئيسية
        splash.update()
        time.sleep(5)  # عرض splash screen لمدة 3 ثواني
        try:
            from customer_issues_window import EnhancedMainWindow
            
            # إغلاق شاشة البداية
            splash.destroy()
            
            # إظهار النافذة الرئيسية
            root.destroy()  # Destroy the hidden root window
            
            # تطبيق النافذة الرئيسية
            app = EnhancedMainWindow()
            
            logging.info("✅ تم تشغيل النظام بنجاح")
            
            # بدء حلقة الأحداث الرئيسية
            app.run()
            
        except ImportError as e:
            logging.error(f"خطأ في استيراد الواجهة الرئيسية: {e}")
            messagebox.showerror("خطأ في النظام", f"فشل في تحميل الواجهة الرئيسية:\n{e}")
            return 1
        
    except Exception as e:
        logging.error(f"خطأ عام في النظام: {e}")
        messagebox.showerror("خطأ في النظام", f"حدث خطأ غير متوقع:\n{e}")
        return 1
    
    finally:
        # إنشاء نسخة احتياطية عند الإغلاق
        create_backup()
        logging.info("تم إغلاق النظام")
        logging.info("=" * 50)

if __name__ == "__main__":
    sys.exit(main())