# Customer Issues Management System
## نظام إدارة مشاكل العملاء

![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

A comprehensive customer issues management system specifically designed for gas companies, featuring an enhanced Arabic and English interface with advanced tracking capabilities.

نظام شامل لإدارة مشاكل العملاء مصمم خصيصاً لشركات الغاز، يتميز بواجهة محسنة باللغتين العربية والإنجليزية مع إمكانيات تتبع متقدمة.

## ✨ Key Features | المميزات الرئيسية

### 🎨 Enhanced User Interface | واجهة محسنة
- **Split Layout Design** | تخطيط مقسم حديث
- **Dynamic Case List** | قائمة ديناميكية للحالات
- **Color-coded Status Badges** | شارات ملونة للحالات
- **Arabic/English Support** | دعم العربية والإنجليزية

### 🔍 Advanced Search | بحث متقدم
- **7 Search Types** | 7 أنواع بحث مختلفة
- **Dynamic Fields** | حقول ديناميكية
- **Real-time Filtering** | فلترة فورية
- **Smart Suggestions** | اقتراحات ذكية

### 📨 Correspondence Management | إدارة المراسلات
- **Dual Numbering System** | نظام ترقيم مزدوج
- **Case Number + Annual Number** | رقم الحالة + رقم سنوي
- **Automatic Tracking** | تتبع تلقائي
- **Document Attachment** | رفع المرفقات

### 📊 Issue Categories | تصنيفات المشاكل
1. **قراءة العداد** | Meter Reading
2. **تحصيل الفواتير** | Bill Collection  
3. **تعديل البيانات** | Data Modification
4. **شكاوى الفواتير** | Bill Complaints
5. **طلبات الربط** | Connection Requests
6. **قطع الخدمة** | Service Disconnection
7. **صيانة العدادات** | Meter Maintenance
8. **تسريب الغاز** | Gas Leakage
9. **شكاوى الخدمة** | Service Complaints
10. **مشاكل تقنية** | Technical Issues
11. **أخرى** | Other

### � Staff Management | إدارة الموظفين
- **Employee Registration** | تسجيل الموظفين
- **Role Assignment** | تحديد الأدوار
- **Activity Tracking** | تتبع النشاطات
- **Change History** | سجل التعديلات

### 🔄 Auto Backup System | نظام النسخ الاحتياطية
- **Smart Backup** | نسخ احتياطية ذكية
- **Scheduled Backups** | نسخ مجدولة
- **Version Control** | تحكم في الإصدارات
- **Data Recovery** | استرداد البيانات

## 🚀 Quick Start | البداية السريعة

### System Requirements | متطلبات النظام
- **Python 3.7+** (for source version | للنسخة المصدرية)
- **Windows 7+** / **Linux** / **macOS**
- **100MB** free disk space | مساحة فارغة

### Installation | التثبيت

#### Option 1: Portable Package | الحزمة المحمولة
```bash
# Download and extract the portable package
# حمل واستخرج الحزمة المحمولة

# Windows
run.bat

# Linux/Mac
./run.sh
```

#### Option 2: From Source | من المصدر
```bash
# Clone the repository
git clone https://github.com/yourusername/customer-issues-management.git
cd customer-issues-management

# Run the system
python customer_issues_main.py

# Or use the run scripts
./run_system.sh    # Linux/Mac
run_system.bat     # Windows
```

## � Usage | الاستخدام

### First Run | التشغيل الأول
1. **Launch the application** | تشغيل التطبيق
2. **System initializes automatically** | النظام يتهيأ تلقائياً
3. **Create your first case** | إنشاء أول حالة
4. **Start managing customer issues** | بدء إدارة مشاكل العملاء

### Main Interface | الواجهة الرئيسية
- **Right Panel**: Case list with search and filters | القائمة الجانبية: قائمة الحالات مع البحث والفلاتر
- **Left Panel**: Case details with tabs | اللوحة الرئيسية: تفاصيل الحالة مع التبويبات
  - **Basic Data** | البيانات الأساسية
  - **Attachments** | المرفقات  
  - **Correspondence** | المراسلات
  - **Change Log** | سجل التعديلات

### Search Types | أنواع البحث
1. **Customer Number** | رقم المشترك
2. **Customer Name** | اسم العميل
3. **Phone Number** | رقم الهاتف
4. **Issue Category** | تصنيف المشكلة
5. **Status** | الحالة
6. **Date Range** | فترة زمنية
7. **Staff Member** | الموظف المسؤول

## 🗂️ File Structure | هيكل الملفات

```
customer-issues-management/
├── customer_issues_main.py          # Main application | التطبيق الرئيسي
├── customer_issues_database.py      # Database manager | مدير قاعدة البيانات
├── customer_issues_window.py        # Main window | النافذة الرئيسية
├── customer_issues_functions.py     # Core functions | الوظائف الأساسية
├── customer_issues_file_manager.py  # File management | إدارة الملفات
├── test_customer_issues.py          # System tests | اختبارات النظام
├── requirements.txt                 # Dependencies | المتطلبات
├── run_system.sh                    # Linux/Mac runner | مشغل لينكس/ماك
├── run_system.bat                   # Windows runner | مشغل ويندوز
├── test_system.bat                  # Test runner | مشغل الاختبار
├── setup.py                         # Setup script | سكريبت الإعداد
├── build_installer.py               # Build script | سكريبت البناء
├── create_portable_package.sh       # Package creator | منشئ الحزمة
├── README.md                        # This file | هذا الملف
├── LICENSE.txt                      # License | الترخيص
├── files/                           # Attachments folder | مجلد المرفقات
├── reports/                         # Generated reports | التقارير المولدة
├── backups/                         # Database backups | النسخ الاحتياطية
└── logs/                           # System logs | سجلات النظام
```

## 🛠️ Development | التطوير

### Building from Source | البناء من المصدر
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
python build_installer.py

# Create portable package
./create_portable_package.sh
```

### Testing | الاختبار
```bash
# Run system tests
python test_customer_issues.py

# Or use the test runner
./test_system.bat    # Windows
```

### Contributing | المساهمة
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📚 Documentation | الوثائق

### Available Documentation | الوثائق المتوفرة
- **User Guide** | دليل المستخدم: Complete usage instructions
- **Technical Documentation** | الوثائق التقنية: System architecture and APIs
- **Installation Guide** | دليل التثبيت: Detailed setup instructions
- **Troubleshooting** | حل المشاكل: Common issues and solutions

### Language Support | دعم اللغات
- **Arabic (العربية)**: Full interface and documentation
- **English**: Full interface and documentation
- **Mixed Mode**: Arabic/English interface switching

## 🔧 Configuration | الإعدادات

### Database | قاعدة البيانات
- **SQLite**: Embedded database (default)
- **Automatic backups**: Every 24 hours
- **Backup retention**: 10 versions

### File Storage | تخزين الملفات
- **Default path**: `./files/`
- **Supported formats**: PDF, DOC, DOCX, XLS, XLSX, images
- **Max file size**: 10MB per file

### Logging | السجلات
- **Log level**: INFO (configurable)
- **Log rotation**: Daily
- **Log retention**: 30 days

## 🚨 Troubleshooting | حل المشاكل

### Common Issues | المشاكل الشائعة

#### Python Not Found | Python غير موجود
```bash
# Install Python 3.7+ from python.org
# Download and run the installer
# Add Python to PATH during installation
```

#### Permission Errors | أخطاء الصلاحيات
```bash
# Run as administrator/sudo
sudo ./run_system.sh    # Linux/Mac
# Right-click -> Run as administrator (Windows)
```

#### Database Errors | أخطاء قاعدة البيانات
```bash
# Check logs folder for detailed error information
# Restore from backup if needed
# Contact support if issues persist
```

## � Support | الدعم

### Getting Help | الحصول على المساعدة
- **Documentation**: Check the included guides
- **Logs**: Review log files in the `logs/` folder
- **Issues**: Create an issue on GitHub
- **Email**: Contact the development team

### Reporting Bugs | الإبلاغ عن الأخطاء
1. Check existing issues
2. Provide detailed description
3. Include log files
4. Specify system information
5. Steps to reproduce

## 📄 License | الترخيص

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE.txt](LICENSE.txt) للتفاصيل.

## 🏆 Credits | الشكر والتقدير

### Development Team | فريق التطوير
- **AI Assistant**: Lead Developer | المطور الرئيسي
- **Community Contributors**: Bug reports and suggestions | المساهمات والاقتراحات

### Special Thanks | شكر خاص
- Gas companies for requirements and feedback
- Beta testers for thorough testing
- Arabic language community for localization support

---

## � Star History | تاريخ النجوم

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/customer-issues-management&type=Date)](https://star-history.com/#yourusername/customer-issues-management&Date)

---

**Made with ❤️ for gas companies worldwide**  
**صُنع بـ ❤️ لشركات الغاز حول العالم**

For more information, visit our [GitHub repository](https://github.com/yourusername/customer-issues-management).  
لمزيد من المعلومات، قم بزيارة [مستودع GitHub](https://github.com/yourusername/customer-issues-management).