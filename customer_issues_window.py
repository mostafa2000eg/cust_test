import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from customer_issues_database import enhanced_db
from customer_issues_file_manager import FileManager

class EnhancedMainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة مشاكل العملاء - النسخة المحسنة")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')

        # إعداد الخطوط
        self.setup_fonts()

        # المتغيرات
        self.file_manager = FileManager()
        self.current_case_id = None
        self.cases_data = []
        self.filtered_cases = []
        self.basic_data_widgets = {}
        self.scrollable_frame = None

        # ربط وظائف النظام
        try:
            from customer_issues_functions import EnhancedFunctions
            self.functions = EnhancedFunctions(self)
        except Exception as e:
            self.functions = None

        # إنشاء الواجهة
        self.create_main_layout()

        # تحميل البيانات الأولية بعد إنشاء كل عناصر الواجهة (لضمان وجود scrollable_frame)
        self.after_main_layout()

        # ربط أحداث الإغلاق
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def after_main_layout(self):
        """تحميل البيانات الأولية بعد إنشاء كل عناصر الواجهة"""
        if hasattr(self, 'functions') and self.functions:
            self.functions.load_initial_data()
        else:
            self.load_initial_data()
    
    def setup_fonts(self):
        """إعداد الخطوط"""
        self.fonts = {
            'header': ('Arial', 16, 'bold'),
            'subheader': ('Arial', 12, 'bold'),
            'normal': ('Arial', 10),
            'small': ('Arial', 9),
            'button': ('Arial', 10, 'bold')
        }
    
    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # اللوحة الجانبية (يمين)
        self.create_sidebar(main_frame)
        
        # فاصل
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side='right', fill='y', padx=5)
        
        # منطقة العرض الرئيسية (يسار)
        self.create_main_display(main_frame)
    
    def create_sidebar(self, parent):
        """إنشاء اللوحة الجانبية"""
        sidebar_frame = tk.Frame(parent, bg='#ffffff', width=400, relief='raised', bd=1)
        sidebar_frame.pack(side='right', fill='y', padx=(0, 5))
        sidebar_frame.pack_propagate(False)
        # عنوان اللوحة الجانبية
        header_frame = tk.Frame(sidebar_frame, bg='#2c3e50', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        header_label = tk.Label(header_frame, text="قائمة الحالات", 
                               font=self.fonts['header'], fg='white', bg='#2c3e50')
        header_label.pack(expand=True)
        # زر العودة للشاشة الرئيسية
        back_btn = tk.Button(sidebar_frame, text="⬅️ العودة للشاشة الرئيسية", font=self.fonts['small'], command=self.show_dashboard, bg='#f1c40f')
        back_btn.pack(fill='x', padx=10, pady=(5, 0))
        # أزرار الإجراءات
        self.create_action_buttons(sidebar_frame)
        # أدوات البحث والفلترة
        self.create_search_filters(sidebar_frame)
        # زر عرض جميع الحالات
        show_all_btn = tk.Button(sidebar_frame, text="👁️ عرض جميع الحالات", font=self.fonts['small'], command=self.show_all_cases_window)
        show_all_btn.pack(fill='x', padx=10, pady=(5, 0))
        # قائمة الحالات
        self.create_cases_list(sidebar_frame)

    def create_action_buttons(self, parent):
        """إنشاء أزرار الإجراءات"""
        buttons_frame = tk.Frame(parent, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        # زر إضافة حالة جديدة
        add_case_btn = tk.Button(buttons_frame, text="+ إضافة حالة جديدة",
                                command=self.add_new_case,
                                font=self.fonts['button'], bg='#27ae60', fg='white',
                                relief='flat', padx=20, pady=10)
        add_case_btn.pack(fill='x', pady=(0, 5))
        
        # زر حذف الحالة
        del_case_btn = tk.Button(buttons_frame, text="🗑️ حذف الحالة",
                                command=self.delete_case,
                                font=self.fonts['button'], bg='#e74c3c', fg='white',
                                relief='flat', padx=20, pady=10)
        del_case_btn.pack(fill='x', pady=(0, 5))
        
        # زر إدارة الموظفين
        manage_emp_btn = tk.Button(buttons_frame, text="👥 إدارة الموظفين",
                                  command=self.manage_employees,
                                  font=self.fonts['button'], bg='#3498db', fg='white',
                                  relief='flat', padx=20, pady=10)
        manage_emp_btn.pack(fill='x')
    
    def create_search_filters(self, parent):
        """إنشاء أدوات البحث والفلترة"""
        filters_frame = tk.Frame(parent, bg='#ffffff')
        filters_frame.pack(fill='x', padx=10, pady=10)
        
        # فلترة السنة
        year_frame = tk.Frame(filters_frame, bg='#ffffff')
        year_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(year_frame, text="السنة:", font=self.fonts['normal'], bg='#ffffff').pack(side='right')
        
        self.year_var = tk.StringVar(value="الكل")
        self.year_combo = ttk.Combobox(year_frame, textvariable=self.year_var, 
                                      state='readonly', width=15)
        self.year_combo.pack(side='right', padx=(5, 0))
        self.year_combo.bind('<<ComboboxSelected>>', self.filter_by_year)
        
        # البحث المتقدم
        search_frame = tk.Frame(filters_frame, bg='#ffffff')
        search_frame.pack(fill='x')
        
        tk.Label(search_frame, text="البحث:", font=self.fonts['normal'], bg='#ffffff').pack(anchor='e')
        
        # نوع البحث
        search_type_frame = tk.Frame(search_frame, bg='#ffffff')
        search_type_frame.pack(fill='x', pady=(5, 0))
        
        self.search_type_var = tk.StringVar(value="شامل")
        self.search_type_combo = ttk.Combobox(search_type_frame, textvariable=self.search_type_var,
                                             state='readonly', width=18)
        self.search_type_combo['values'] = [
            "شامل", "اسم العميل", "رقم المشترك", "العنوان", 
            "تصنيف المشكلة", "حالة المشكلة", "اسم الموظف"
        ]
        self.search_type_combo.pack(fill='x')
        self.search_type_combo.bind('<<ComboboxSelected>>', self.on_search_type_change)
        
        # حقل البحث
        search_input_frame = tk.Frame(search_frame, bg='#ffffff')
        search_input_frame.pack(fill='x', pady=(5, 0))
        
        self.search_value_var = tk.StringVar()
        self.search_entry = tk.Entry(search_input_frame, textvariable=self.search_value_var,
                                    font=self.fonts['normal'])
        self.search_entry.pack(fill='x')
        self.search_entry.bind('<KeyRelease>', self.perform_search)
        
        # سيتم إنشاء الكومبو بوكس ديناميكياً حسب نوع البحث
        self.search_combo = None
        
        # إضافة قائمة ترتيب
        sort_frame = tk.Frame(parent, bg='#ffffff')
        sort_frame.pack(fill='x', padx=10, pady=(0, 10))
        tk.Label(sort_frame, text="ترتيب حسب:", font=self.fonts['normal'], bg='#ffffff').pack(side='right')
        self.sort_var = tk.StringVar(value="السنة (تنازلي)")
        sort_options = ["السنة (تنازلي)", "السنة (تصاعدي)", "اسم العميل (أ-ي)", "اسم العميل (ي-أ)"]
        self.sort_combo = ttk.Combobox(sort_frame, textvariable=self.sort_var, values=sort_options, state='readonly', width=18)
        self.sort_combo.pack(side='right', padx=(5, 0))
        self.sort_combo.bind('<<ComboboxSelected>>', self.apply_sorting)
    
    def create_cases_list(self, parent):
        """
        إنشاء قائمة الحالات مع دعم Scrollbar وتمرير بالماوس ولوحة المفاتيح
        وجعل الـ Scrollbar ظاهر دائمًا
        """
        list_frame = tk.Frame(parent, bg='#ffffff')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        list_canvas = tk.Canvas(list_frame, bg='#ffffff', highlightthickness=0)
        # استخدم ttk.Style لجعل الـ Scrollbar دائم الظهور
        style = ttk.Style()
        style.layout('AlwaysOn.TScrollbar',
            [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})]
        )
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview, style='AlwaysOn.TScrollbar')
        self.scrollable_frame = tk.Frame(list_canvas, bg='#ffffff')
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.cases_canvas = list_canvas
        self.cases_scrollbar = scrollbar
        # دعم تمرير بالماوس
        def _on_mousewheel(event):
            list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        list_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # دعم تمرير بالأسهم
        list_canvas.bind_all("<Up>", self._on_case_list_up)
        list_canvas.bind_all("<Down>", self._on_case_list_down)
        self.selected_case_index = 0
        self.case_card_widgets = []
    
    def create_main_display(self, parent):
        """إنشاء منطقة العرض الرئيسية"""
        # الإطار الرئيسي للعرض
        display_frame = tk.Frame(parent, bg='#ffffff', relief='raised', bd=1)
        display_frame.pack(side='left', fill='both', expand=True)
        
        # رأس العرض
        self.create_display_header(display_frame)
        
        # أزرار العمليات
        self.create_display_buttons(display_frame)
        
        # نظام التبويبات
        self.create_tabs(display_frame)
    
    def create_display_header(self, parent):
        """إنشاء رأس العرض"""
        header_frame = tk.Frame(parent, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # اسم العميل
        self.customer_name_label = tk.Label(header_frame, text="اختر حالة من القائمة",
                                           font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        self.customer_name_label.pack(expand=True, pady=(10, 0))
        
        # الموظف المسؤول عن الحل
        self.solved_by_label = tk.Label(header_frame, text="",
                                       font=self.fonts['normal'], fg='#bdc3c7', bg='#34495e')
        self.solved_by_label.pack(pady=(0, 10))
    
    def create_display_buttons(self, parent):
        """إنشاء أزرار العمليات"""
        buttons_frame = tk.Frame(parent, bg='#ecf0f1', height=60)
        buttons_frame.pack(fill='x')
        buttons_frame.pack_propagate(False)
        
        # زر حفظ التغييرات
        self.save_btn = tk.Button(buttons_frame, text="💾 حفظ التغييرات",
                                 command=self.save_changes,
                                 font=self.fonts['button'], bg='#27ae60', fg='white',
                                 relief='flat', padx=20, pady=8, state='disabled')
        self.save_btn.pack(side='right', padx=10, pady=10)
        
        # زر طباعة
        self.print_btn = tk.Button(buttons_frame, text="🖨️ طباعة",
                                  command=self.print_case,
                                  font=self.fonts['button'], bg='#3498db', fg='white',
                                  relief='flat', padx=20, pady=8, state='disabled')
        self.print_btn.pack(side='right', padx=(0, 10), pady=10)
    
    def create_tabs(self, parent):
        """إنشاء نظام التبويبات"""
        # إطار التبويبات
        tabs_frame = tk.Frame(parent, bg='#ffffff')
        tabs_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # نوت بوك التبويبات
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # التبويبات
        self.create_basic_data_tab()
        self.create_attachments_tab()
        self.create_correspondences_tab()
        self.create_audit_log_tab()
    
    def create_basic_data_tab(self):
        """إنشاء تبويب البيانات الأساسية"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="البيانات الأساسية")
        
        # إطار للمحتوى مع سكرول
        canvas = tk.Canvas(basic_frame, bg='#ffffff')
        style = ttk.Style()
        style.layout('AlwaysOn.TScrollbar',
            [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})]
        )
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview, style='AlwaysOn.TScrollbar')
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # الحقول
        fields_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # بيانات العميل
        customer_section = tk.LabelFrame(fields_frame, text="بيانات العميل", 
                                        font=self.fonts['subheader'], bg='#ffffff')
        customer_section.pack(fill='x', pady=(0, 20))
        
        # اسم العميل
        self.create_field(customer_section, "اسم العميل:", "customer_name", row=0)
        
        # رقم المشترك
        self.create_field(customer_section, "رقم المشترك:", "subscriber_number", row=1)
        
        # رقم الهاتف
        self.create_field(customer_section, "رقم الهاتف:", "phone", row=2)
        
        # العنوان
        self.create_text_field(customer_section, "العنوان:", "address", row=3, height=3)
        
        # بيانات المشكلة
        problem_section = tk.LabelFrame(fields_frame, text="بيانات المشكلة", 
                                       font=self.fonts['subheader'], bg='#ffffff')
        problem_section.pack(fill='x', pady=(0, 20))
        
        # تصنيف المشكلة
        category_combo = self.create_combo_field(problem_section, "تصنيف المشكلة:", "category", row=0)
        categories = enhanced_db.get_categories() if hasattr(enhanced_db, 'get_categories') else []
        if not categories:
            # إضافة تصنيفات افتراضية إذا كانت قاعدة البيانات فارغة
            default_cats = ["مياه", "صرف صحي", "عداد", "فاتورة", "شكاوى أخرى"]
            # for cat in default_cats:
            #     if hasattr(enhanced_db, 'add_category'):
            #         enhanced_db.add_category(cat)
            categories = enhanced_db.get_categories() if hasattr(enhanced_db, 'get_categories') else []
        category_names = [cat[1] for cat in categories]
        category_combo['values'] = category_names
        if category_names:
            category_combo.set(category_names[0])
        
        # حالة المشكلة
        status_combo = self.create_combo_field(problem_section, "حالة المشكلة:", "status", row=1)
        status_options = enhanced_db.get_status_options() if hasattr(enhanced_db, 'get_status_options') else []
        if not status_options:
            status_options = [("جديدة", "#3498db"), ("قيد التنفيذ", "#f39c12"), ("تم حلها", "#27ae60"), ("مغلقة", "#95a5a6")]
        status_names = [s[0] for s in status_options]
        status_combo['values'] = status_names
        if status_names:
            status_combo.set(status_names[0])
        
        # وصف المشكلة
        self.create_text_field(problem_section, "وصف المشكلة:", "problem_description", row=2, height=4)
        
        # ما تم تنفيذه
        self.create_text_field(problem_section, "ما تم تنفيذه:", "actions_taken", row=3, height=4)
        
        # بيانات العداد والمديونية
        meter_section = tk.LabelFrame(fields_frame, text="بيانات العداد والمديونية", 
                                     font=self.fonts['subheader'], bg='#ffffff')
        meter_section.pack(fill='x')
        
        # آخر قراءة
        self.create_field(meter_section, "آخر قراءة للعداد:", "last_meter_reading", row=0)
        
        # تاريخ آخر قراءة
        self.create_field(meter_section, "تاريخ آخر قراءة:", "last_reading_date", row=1)
        
        # المديونية
        self.create_field(meter_section, "المديونية:", "debt_amount", row=2)
        
        # اختيار الموظف المسؤول عن الإضافة/التعديل
        employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
        self.employee_var = tk.StringVar()
        employee_names = [emp[1] for emp in employees]
        if employee_names:
            self.employee_var.set(employee_names[0])
        emp_frame = tk.Frame(fields_frame, bg='#ffffff')
        emp_frame.pack(fill='x', pady=(10, 0))
        tk.Label(emp_frame, text="الموظف المسؤول:", font=self.fonts['normal'], bg='#ffffff').pack(side='right')
        emp_combo = ttk.Combobox(emp_frame, textvariable=self.employee_var, values=employee_names, state='readonly', width=30)
        emp_combo.pack(side='right', padx=(5, 0))
        self.basic_data_widgets['employee_name'] = emp_combo
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # حفظ المراجع
        # self.basic_data_widgets = {}  # لا تعيد تعيين القاموس هنا حتى لا تفقد الحقول
    
    def create_field(self, parent, label_text, field_name, row, column=0, width=30):
        """إنشاء حقل إدخال عادي"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=column*2, sticky='e', padx=(10, 5), pady=5)
        
        entry = tk.Entry(parent, font=self.fonts['normal'], width=width)
        entry.grid(row=row, column=column*2+1, sticky='w', padx=(0, 10), pady=5)
        
        self.basic_data_widgets[field_name] = entry
        return entry
    
    def create_text_field(self, parent, label_text, field_name, row, height=3, width=40):
        """إنشاء حقل نص متعدد الأسطر"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=0, sticky='ne', padx=(10, 5), pady=5)
        
        text_frame = tk.Frame(parent, bg='#ffffff')
        text_frame.grid(row=row, column=1, sticky='w', padx=(0, 10), pady=5)
        
        text_widget = tk.Text(text_frame, font=self.fonts['normal'], width=width, height=height)
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        self.basic_data_widgets[field_name] = text_widget
        return text_widget
    
    def create_combo_field(self, parent, label_text, field_name, row, width=30):
        """إنشاء حقل قائمة منسدلة"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=0, sticky='e', padx=(10, 5), pady=5)
        combo = ttk.Combobox(parent, font=self.fonts['normal'], width=width-3, state='readonly')
        combo.grid(row=row, column=1, sticky='w', padx=(0, 10), pady=5)
        self.basic_data_widgets[field_name] = combo
        return combo
    
    def create_attachments_tab(self):
        """إنشاء تبويب المرفقات"""
        attachments_frame = ttk.Frame(self.notebook)
        self.notebook.add(attachments_frame, text="المرفقات")
        # أزرار المرفقات
        buttons_frame = tk.Frame(attachments_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        add_attachment_btn = tk.Button(buttons_frame, text="📎 إضافة مرفق",
                                      command=self.add_attachment,
                                      font=self.fonts['button'], bg='#3498db', fg='white',
                                      relief='flat', padx=15, pady=8)
        add_attachment_btn.pack(side='right')
        # جدول المرفقات (أضف عمود مسار الملف كعمود مخفي)
        columns = ('ID', 'نوع الملف', 'اسم الملف', 'الوصف', 'تاريخ الرفع', 'الموظف', 'مسار الملف')
        self.attachments_tree = ttk.Treeview(attachments_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.attachments_tree.heading(col, text=col)
            if col == 'ID':
                self.attachments_tree.column(col, width=50)
            elif col == 'نوع الملف':
                self.attachments_tree.column(col, width=80)
            elif col == 'مسار الملف':
                self.attachments_tree.column(col, width=0, stretch=False)  # إخفاء العمود
            else:
                self.attachments_tree.column(col, width=120)
        # سكرول بار للمرفقات
        attachments_scrollbar = ttk.Scrollbar(attachments_frame, orient='vertical', command=self.attachments_tree.yview)
        self.attachments_tree.configure(yscrollcommand=attachments_scrollbar.set)
        self.attachments_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        attachments_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        # ربط النقر المزدوج
        self.attachments_tree.bind('<Double-1>', self.open_attachment)
        self.attachments_tree.bind('<Button-3>', self.show_attachment_context_menu)
    
    def create_correspondences_tab(self):
        """إنشاء تبويب المراسلات"""
        correspondences_frame = ttk.Frame(self.notebook)
        self.notebook.add(correspondences_frame, text="المراسلات")
        # أزرار المراسلات
        buttons_frame = tk.Frame(correspondences_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        add_correspondence_btn = tk.Button(buttons_frame, text="✉️ إضافة مراسلة",
                                          command=self.add_correspondence,
                                          font=self.fonts['button'], bg='#e67e22', fg='white',
                                          relief='flat', padx=15, pady=8)
        add_correspondence_btn.pack(side='right')
        # زر حذف مراسلة
        del_correspondence_btn = tk.Button(buttons_frame, text="🗑️ حذف مراسلة",
                                           command=self.delete_correspondence,
                                           font=self.fonts['button'], bg='#e74c3c', fg='white',
                                           relief='flat', padx=15, pady=8)
        del_correspondence_btn.pack(side='right', padx=(0, 10))
        # جدول المراسلات
        columns = ('ID', 'رقم التسلسل', 'الرقم السنوي', 'المرسل', 'المحتوى', 'التاريخ', 'الموظف')
        self.correspondences_tree = ttk.Treeview(correspondences_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.correspondences_tree.heading(col, text=col)
            if col == 'ID':
                self.correspondences_tree.column(col, width=50)
            elif col in ['رقم التسلسل', 'الرقم السنوي']:
                self.correspondences_tree.column(col, width=80)
            else:
                self.correspondences_tree.column(col, width=120)
        # سكرول بار للمراسلات
        correspondences_scrollbar = ttk.Scrollbar(correspondences_frame, orient='vertical', command=self.correspondences_tree.yview)
        self.correspondences_tree.configure(yscrollcommand=correspondences_scrollbar.set)
        self.correspondences_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        correspondences_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        # ربط النقر المزدوج
        self.correspondences_tree.bind('<Double-1>', self.edit_correspondence)
    
    def create_audit_log_tab(self):
        """إنشاء تبويب سجل التعديلات"""
        audit_frame = ttk.Frame(self.notebook)
        self.notebook.add(audit_frame, text="سجل التعديلات")
        
        # جدول سجل التعديلات
        columns = ('التاريخ والوقت', 'الموظف', 'نوع الإجراء', 'وصف الإجراء')
        self.audit_tree = ttk.Treeview(audit_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.audit_tree.heading(col, text=col)
            if col == 'التاريخ والوقت':
                self.audit_tree.column(col, width=150)
            elif col == 'الموظف':
                self.audit_tree.column(col, width=120)
            else:
                self.audit_tree.column(col, width=200)
        
        # سكرول بار لسجل التعديلات
        audit_scrollbar = ttk.Scrollbar(audit_frame, orient='vertical', command=self.audit_tree.yview)
        self.audit_tree.configure(yscrollcommand=audit_scrollbar.set)
        
        self.audit_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        audit_scrollbar.pack(side='right', fill='y', pady=10)
    
    # سأكمل باقي الوظائف في الجزء التالي...
    
    def add_new_case(self):
        """تهيئة النموذج لإضافة حالة جديدة"""
        for widget in self.basic_data_widgets.values():
            if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
        self.current_case_id = None
        self.save_btn.config(state='normal')
        self.print_btn.config(state='disabled')
        self.customer_name_label.config(text="إدخال حالة جديدة")
        self.solved_by_label.config(text="")
        self.update_action_buttons_style()

    def manage_employees(self):
        employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
        win = tk.Toplevel(self.root)
        win.title("إدارة الموظفين")
        win.geometry("400x500")
        tk.Label(win, text="قائمة الموظفين:", font=self.fonts['header']).pack(pady=10)
        emp_listbox = tk.Listbox(win, font=self.fonts['normal'], height=12)
        emp_listbox.pack(fill='x', padx=20)
        for emp in employees:
            name = emp[1] if len(emp) > 1 else ''
            emp_listbox.insert('end', name)
        # إضافة موظف
        add_frame = tk.Frame(win)
        add_frame.pack(pady=10)
        new_emp_var = tk.StringVar()
        tk.Entry(add_frame, textvariable=new_emp_var, font=self.fonts['normal'], width=20).pack(side='left')
        def add_emp():
            name = new_emp_var.get().strip()
            if name:
                if hasattr(enhanced_db, 'add_employee'):
                    enhanced_db.add_employee(name)
                emp_listbox.insert('end', name)
                new_emp_var.set('')
        tk.Button(add_frame, text="إضافة", command=add_emp, font=self.fonts['button'], bg='#27ae60', fg='white').pack(side='left', padx=5)
        # حذف موظف
        def del_emp():
            sel = emp_listbox.curselection()
            if sel:
                idx = sel[0]
                name = emp_listbox.get(idx)
                # جلب id الموظف من قاعدة البيانات
                employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
                emp_id = None
                for emp in employees:
                    if emp[1] == name:
                        emp_id = emp[0]
                        break
                if emp_id and hasattr(enhanced_db, 'delete_employee'):
                    enhanced_db.delete_employee(emp_id)
                emp_listbox.delete(idx)
        tk.Button(win, text="حذف المحدد", command=del_emp, font=self.fonts['button'], bg='#e74c3c', fg='white').pack(pady=5)
        tk.Button(win, text="إغلاق", command=win.destroy).pack(pady=20)

    def filter_by_year(self, event=None):
        year = self.year_var.get()
        if year == "الكل":
            self.filtered_cases = self.cases_data.copy()
        else:
            self.filtered_cases = [case for case in self.cases_data if str(case.get('created_date', '')).startswith(year)]
        self.update_cases_list()

    def on_search_type_change(self, event=None):
        # إزالة أي كومبو بوكس سابق
        if self.search_combo:
            self.search_combo.destroy()
            self.search_combo = None
        search_type = self.search_type_var.get()
        parent = self.search_entry.master
        if search_type == "تصنيف المشكلة":
            categories = enhanced_db.get_categories() if hasattr(enhanced_db, 'get_categories') else []
            category_names = [cat[1] for cat in categories]
            self.search_value_var.set("")
            self.search_combo = ttk.Combobox(parent, values=category_names, textvariable=self.search_value_var, state='readonly')
            self.search_combo.pack(fill='x')
            self.search_combo.bind('<<ComboboxSelected>>', self.perform_search)
            self.search_entry.pack_forget()
        elif search_type == "حالة المشكلة":
            status_options = enhanced_db.get_status_options() if hasattr(enhanced_db, 'get_status_options') else []
            status_names = [s[0] for s in status_options]
            self.search_value_var.set("")
            self.search_combo = ttk.Combobox(parent, values=status_names, textvariable=self.search_value_var, state='readonly')
            self.search_combo.pack(fill='x')
            self.search_combo.bind('<<ComboboxSelected>>', self.perform_search)
            self.search_entry.pack_forget()
        else:
            if not self.search_entry.winfo_ismapped():
                self.search_entry.pack(fill='x')
            self.search_value_var.set("")
            if self.search_combo:
                self.search_combo.destroy()
                self.search_combo = None
        self.perform_search()

    def add_attachment(self):
        if not self.current_case_id:
            messagebox.showwarning("تنبيه", "يرجى اختيار أو حفظ حالة أولاً.")
            return
        win = tk.Toplevel(self.root)
        win.title("إضافة مرفق")
        win.geometry("400x260")
        tk.Label(win, text="اختر الملف:", font=self.fonts['normal']).pack(pady=(10, 0))
        file_path_var = tk.StringVar()
        def select_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                file_path_var.set(file_path)
        file_frame = tk.Frame(win)
        file_frame.pack(fill='x', padx=20)
        tk.Entry(file_frame, textvariable=file_path_var, font=self.fonts['normal'], state='readonly').pack(side='left', fill='x', expand=True)
        tk.Button(file_frame, text="استعراض...", command=select_file).pack(side='right', padx=(5, 0))
        tk.Label(win, text="الوصف:", font=self.fonts['normal']).pack(pady=(10, 0))
        desc_var = tk.StringVar()
        tk.Entry(win, textvariable=desc_var, font=self.fonts['normal']).pack(fill='x', padx=20)
        # اختيار الموظف
        tk.Label(win, text="الموظف المسؤول:", font=self.fonts['normal']).pack(pady=(10, 0))
        emp_names = [emp[1] for emp in enhanced_db.get_employees()]
        emp_var = tk.StringVar(value=emp_names[0] if emp_names else "")
        emp_combo = ttk.Combobox(win, values=emp_names, textvariable=emp_var, state='readonly')
        emp_combo.pack(fill='x', padx=20)
        def save_attachment():
            file_path = file_path_var.get()
            description = desc_var.get().strip()
            emp_name = emp_var.get()
            if not file_path:
                messagebox.showerror("خطأ", "يرجى اختيار ملف.")
                return
            # التصحيح هنا: استخدم copy_file_to_case_folder بدلاً من select_and_copy_file
            file_info = self.file_manager.copy_file_to_case_folder(file_path, self.current_case_id, description)
            print(f"[DEBUG] سيتم تخزين المرفق في المسار: {file_info['file_path'] if file_info else 'None'}")
            if file_info:
                file_info['case_id'] = self.current_case_id
                file_info['upload_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                emp_id = None
                employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
                for emp in employees:
                    if emp[1] == emp_name:
                        emp_id = emp[0]
                        break
                file_info['uploaded_by'] = emp_id if emp_id else 1
                file_info['file_type'] = self.file_manager.get_file_type(file_info['file_name'])
                file_info['description'] = description
                # تأكد من عدم وجود uploaded_by_name أو أي قيمة غير مطلوبة
                file_info = {k: v for k, v in file_info.items() if k in ['case_id', 'file_name', 'file_path', 'file_type', 'description', 'upload_date', 'uploaded_by']}
                print("[DEBUG] بيانات المرفق قبل الحفظ:", file_info)
                if hasattr(enhanced_db, 'add_attachment'):
                    enhanced_db.add_attachment(file_info)
                # تحقق من وجود الملف فعلياً بعد النسخ
                if not os.path.exists(file_info['file_path']):
                    messagebox.showerror("تحذير!", f"تم تسجيل المرفق لكن الملف غير موجود فعلياً في المسار:\n{file_info['file_path']}")
                # سجل التعديلات
                if hasattr(enhanced_db, 'log_action'):
                    desc = f"تم إضافة المرفق: {file_info['file_name']} بواسطة {emp_name}"
                    enhanced_db.log_action(self.current_case_id, "إضافة مرفق", desc, emp_id if emp_id else 1)
                self.load_attachments()
                messagebox.showinfo("تمت الإضافة", "تمت إضافة المرفق بنجاح.")
                win.destroy()
        btn_frame = tk.Frame(win)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="حفظ", command=save_attachment, width=12).pack(side='right', padx=10)
        tk.Button(btn_frame, text="إلغاء", command=win.destroy, width=12).pack(side='right')

    def open_attachment(self, event=None):
        selected = self.attachments_tree.selection()
        if not selected:
            return
        item = self.attachments_tree.item(selected[0])
        file_path = item['values'][-1]
        print(f"[DEBUG] محاولة فتح المرفق من المسار: {file_path}")
        # إذا كان المسار نسبي، حوله لمسار كامل من جذر المشروع
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(os.path.join(os.getcwd(), file_path))
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            def reattach_file():
                new_path = filedialog.askopenfilename(title="اختر الملف الأصلي للمرفق")
                if new_path:
                    # تحديث المسار في قاعدة البيانات
                    attachment_id = item['values'][0]
                    if hasattr(enhanced_db, 'execute_query'):
                        enhanced_db.execute_query("UPDATE attachments SET file_path = ? WHERE id = ?", (new_path, attachment_id))
                    # إعادة تحميل المرفقات
                    self.load_attachments()
                    messagebox.showinfo("تم التحديث", "تم تحديث مسار الملف بنجاح. يمكنك الآن فتح المرفق.")
            msg = f"الملف غير موجود في المسار التالي:\n{file_path}\n\nهل ترغب في إعادة ربط الملف؟"
            messagebox.showerror("ملف غير موجود", msg)
            if messagebox.askyesno("ملف غير موجود", msg):
                reattach_file()

    def show_attachment_context_menu(self, event=None):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="فتح", command=lambda: self.open_attachment())
        menu.add_command(label="حذف", command=self.delete_attachment)
        if event is not None:
            menu.tk_popup(event.x_root, event.y_root)

    def delete_attachment(self):
        selected = self.attachments_tree.selection()
        if not selected:
            return
        item = self.attachments_tree.item(selected[0])
        attachment_id = item['values'][0]
        file_name = item['values'][2]
        # تأكيد الحذف
        if not messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد أنك تريد حذف المرفق '{file_name}'؟"):
            return
        # حذف من قاعدة البيانات إذا كانت الدالة متوفرة
        if hasattr(enhanced_db, 'delete_attachment'):
            enhanced_db.delete_attachment(attachment_id)
        # سجل التعديلات
        emp_name = self.employee_var.get() if hasattr(self, 'employee_var') else ""
        emp_id = None
        employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
        for emp in employees:
            if emp[1] == emp_name:
                emp_id = emp[0]
                break
        if hasattr(enhanced_db, 'log_action'):
            desc = f"تم حذف المرفق: {file_name} بواسطة {emp_name}"
            enhanced_db.log_action(self.current_case_id, "حذف مرفق", desc, emp_id if emp_id else 1)
        self.load_attachments()
        messagebox.showinfo("تم الحذف", "تم حذف المرفق.")

    def add_correspondence(self):
        if not self.current_case_id:
            messagebox.showwarning("تنبيه", "يرجى اختيار أو حفظ حالة أولاً.")
            return
        win = tk.Toplevel(self.root)
        win.title("إضافة مراسلة")
        win.geometry("400x400")
        tk.Label(win, text="المرسل:", font=self.fonts['normal']).pack(pady=(10, 0))
        sender_var = tk.StringVar()
        tk.Entry(win, textvariable=sender_var, font=self.fonts['normal']).pack(fill='x', padx=20)
        # اختيار الموظف
        tk.Label(win, text="الموظف المسؤول:", font=self.fonts['normal']).pack(pady=(10, 0))
        emp_names = [emp[1] for emp in enhanced_db.get_employees()]
        emp_var = tk.StringVar(value=emp_names[0] if emp_names else "")
        emp_combo = ttk.Combobox(win, values=emp_names, textvariable=emp_var, state='readonly')
        emp_combo.pack(fill='x', padx=20)
        # توليد الرقمين تلقائياً
        seq_num, yearly_num = 1, 1
        if hasattr(enhanced_db, 'get_next_correspondence_numbers'):
            seq_num, yearly_num = enhanced_db.get_next_correspondence_numbers(self.current_case_id)
        tk.Label(win, text=f"رقم التسلسل: {seq_num}", font=self.fonts['normal']).pack(pady=(10, 0))
        tk.Label(win, text=f"الرقم السنوي: {yearly_num}", font=self.fonts['normal']).pack(pady=(0, 0))
        tk.Label(win, text="المحتوى:", font=self.fonts['normal']).pack(pady=10)
        content_var = tk.Text(win, height=6)
        content_var.pack(fill='x', padx=20)
        def save_corr():
            sender = sender_var.get().strip()
            content = content_var.get('1.0', tk.END).strip()
            emp_name = emp_var.get()
            emp_id = None
            employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
            for emp in employees:
                if emp[1] == emp_name:
                    emp_id = emp[0]
                    break
            if content and hasattr(enhanced_db, 'add_correspondence'):
                corr_data = {
                    'case_id': self.current_case_id,
                    'case_sequence_number': seq_num,
                    'yearly_sequence_number': yearly_num,
                    'sender': sender,
                    'message_content': content,
                    'created_by': emp_id if emp_id else 1,
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'sent_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                enhanced_db.add_correspondence(corr_data)
                # سجل التعديلات
                if hasattr(enhanced_db, 'log_action'):
                    desc = f"تم إضافة مراسلة رقم {seq_num} بواسطة {emp_name}"
                    enhanced_db.log_action(self.current_case_id, "إضافة مراسلة", desc, emp_id if emp_id else 1)
                self.load_correspondences()
                win.destroy()
                messagebox.showinfo("تمت الإضافة", "تمت إضافة المراسلة بنجاح.")
        tk.Button(win, text="حفظ", command=save_corr).pack(pady=10)
        tk.Button(win, text="إلغاء", command=win.destroy).pack()

    def edit_correspondence(self, event=None):
        selected = self.correspondences_tree.selection()
        if not selected:
            return
        item = self.correspondences_tree.item(selected[0])
        corr_id = item['values'][0]
        old_content = item['values'][4]
        win = tk.Toplevel(self.root)
        win.title("تعديل مراسلة")
        win.geometry("400x300")
        tk.Label(win, text="المحتوى:", font=self.fonts['normal']).pack(pady=10)
        content_var = tk.Text(win, height=6)
        content_var.insert('1.0', old_content)
        content_var.pack(fill='x', padx=20)
        def save_corr():
            content = content_var.get('1.0', tk.END).strip()
            # if content and hasattr(enhanced_db, 'update_correspondence'):
            #     enhanced_db.update_correspondence(corr_id, content)
            self.load_correspondences()
            win.destroy()
            messagebox.showinfo("تم التحديث", "تم تحديث المراسلة.")
        tk.Button(win, text="حفظ", command=save_corr).pack(pady=10)
        tk.Button(win, text="إلغاء", command=win.destroy).pack()

    def delete_correspondence(self):
        selected = self.correspondences_tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار مراسلة أولاً.")
            return
        item = self.correspondences_tree.item(selected[0])
        corr_id = item['values'][0]
        seq_num = item['values'][1]
        # تأكيد الحذف
        if not messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد أنك تريد حذف المراسلة رقم {seq_num}؟"):
            return
        try:
            print(f"[DEBUG] محاولة حذف مراسلة corr_id={corr_id}")
            if hasattr(enhanced_db, 'delete_correspondence'):
                enhanced_db.delete_correspondence(int(corr_id))
                print(f"[DEBUG] تم حذف المراسلة corr_id={corr_id}")
            else:
                print("[ERROR] دالة delete_correspondence غير موجودة في قاعدة البيانات!")
                messagebox.showerror("خطأ في الحذف", "دالة حذف المراسلة غير متوفرة في قاعدة البيانات.")
                return
            # سجل التعديلات
            emp_name = self.employee_var.get() if hasattr(self, 'employee_var') else ""
            emp_id = None
            employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
            for emp in employees:
                if emp[1] == emp_name:
                    emp_id = emp[0]
                    break
            if hasattr(enhanced_db, 'log_action'):
                desc = f"تم حذف مراسلة رقم {seq_num} بواسطة {emp_name}"
                enhanced_db.log_action(self.current_case_id, "حذف مراسلة", desc, emp_id if emp_id else 1)
            self.load_correspondences()
            messagebox.showinfo("تم الحذف", "تم حذف المراسلة.")
        except Exception as e:
            print(f"[ERROR] Exception أثناء حذف المراسلة: {e}")
            messagebox.showerror("خطأ في الحذف", f"حدث خطأ أثناء حذف المراسلة:\n{e}")

    def load_initial_data(self):
        self.cases_data = enhanced_db.get_all_cases() if hasattr(enhanced_db, 'get_all_cases') else []
        self.filtered_cases = self.cases_data.copy()
        self.update_cases_list()
        self.load_attachments()
        self.load_correspondences()
        self.load_audit_log()
        years = sorted({str(case.get('created_date', '')).split('-')[0] for case in self.cases_data if case.get('created_date')}, reverse=True)
        self.year_combo['values'] = ["الكل"] + years
        self.year_combo.set("الكل")

    def load_attachments(self):
        for i in self.attachments_tree.get_children():
            self.attachments_tree.delete(i)
        if not self.current_case_id or not hasattr(enhanced_db, 'get_attachments'):
            return
        attachments = enhanced_db.get_attachments(self.current_case_id)
        for att in attachments:
            self.attachments_tree.insert('', 'end', values=(
                att.get('id'),
                att.get('file_type'),
                att.get('file_name'),
                att.get('description'),
                att.get('upload_date'),
                att.get('uploaded_by_name'),
                att.get('file_path')  # عمود مسار الملف المخفي
            ))

    def load_correspondences(self):
        for i in self.correspondences_tree.get_children():
            self.correspondences_tree.delete(i)
        if not self.current_case_id or not hasattr(enhanced_db, 'get_correspondences'):
            return
        correspondences = enhanced_db.get_correspondences(self.current_case_id)
        for corr in correspondences:
            self.correspondences_tree.insert('', 'end', values=(
                corr.get('id'),
                corr.get('case_sequence_number'),
                corr.get('yearly_sequence_number'),
                corr.get('sender'),
                corr.get('message_content'),
                corr.get('sent_date'),
                corr.get('created_by_name')
            ))

    def load_audit_log(self):
        for i in self.audit_tree.get_children():
            self.audit_tree.delete(i)
        if not self.current_case_id or not hasattr(enhanced_db, 'get_case_audit_log'):
            return
        logs = enhanced_db.get_case_audit_log(self.current_case_id)
        for log in logs:
            # log: [id, case_id, action_type, action_description, performed_by, timestamp, old_values, new_values, performed_by_name]
            self.audit_tree.insert('', 'end', values=(log[5], log[8], log[2], log[3]))

    def print_case(self):
        if not self.current_case_id:
            messagebox.showwarning("تنبيه", "يرجى اختيار حالة أولاً.")
            return
        # دعم dict وtuple
        case = None
        for c in self.cases_data:
            try:
                if isinstance(c, dict):
                    cid = c.get('id')
                    if cid is None or not str(cid).isdigit():
                        continue
                    if int(cid) == int(self.current_case_id):
                        case = c
                        break
                elif isinstance(c, tuple):
                    cid = c[0]
                    if cid is None or not str(cid).isdigit():
                        continue
                    if int(cid) == int(self.current_case_id):
                        keys = ['id', 'customer_name', 'subscriber_number', 'status', 'category_name', 'color_code', 'modified_by_name', 'created_date', 'modified_date']
                        case = dict(zip(keys, c))
                        break
            except Exception:
                continue
        if not case:
            messagebox.showerror("خطأ", "تعذر العثور على بيانات الحالة.")
            return
        temp_path = os.path.join(os.getcwd(), f"case_{self.current_case_id}_print.txt")
        # تعريب الحقول
        field_map = {
            'id': 'رقم الحالة',
            'customer_name': 'اسم العميل',
            'subscriber_number': 'رقم المشترك',
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'category_name': 'تصنيف المشكلة',
            'status': 'حالة المشكلة',
            'problem_description': 'وصف المشكلة',
            'actions_taken': 'ما تم تنفيذه',
            'last_meter_reading': 'آخر قراءة للعداد',
            'last_reading_date': 'تاريخ آخر قراءة',
            'debt_amount': 'المديونية',
            'created_date': 'تاريخ الإضافة',
            'modified_date': 'تاريخ التعديل',
            'created_by_name': 'أضيف بواسطة',
            'modified_by_name': 'آخر معدل',
            'solved_by_name': 'تم الحل بواسطة',
        }
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write("========== تقرير حالة عميل ==========" + "\n\n")
            f.write("--- بيانات الحالة ---\n")
            for k, v in case.items():
                label = field_map.get(k, k)
                f.write(f"{label}: {v if v is not None else ''}\n")
            f.write("\n--- المرفقات ---\n")
            attachments = enhanced_db.get_attachments(self.current_case_id) if hasattr(enhanced_db, 'get_attachments') else []
            if attachments:
                for att in attachments:
                    f.write(f"ملف: {att.get('file_name', '')} | الوصف: {att.get('description', '')} | التاريخ: {att.get('upload_date', '')}\n")
            else:
                f.write("لا يوجد مرفقات\n")
            f.write("\n--- المراسلات ---\n")
            correspondences = enhanced_db.get_correspondences(self.current_case_id) if hasattr(enhanced_db, 'get_correspondences') else []
            if correspondences:
                for corr in correspondences:
                    f.write(f"مرسل: {corr.get('sender', '')} | التاريخ: {corr.get('created_date', '')}\nالمحتوى: {corr.get('message_content', '')}\n---\n")
            else:
                f.write("لا يوجد مراسلات\n")
            f.write("\n--- سجل التعديلات ---\n")
            audit_log = enhanced_db.get_case_audit_log(self.current_case_id) if hasattr(enhanced_db, 'get_case_audit_log') else []
            if audit_log:
                for log in audit_log:
                    if isinstance(log, dict):
                        f.write(f"{log.get('action_type', '')} | {log.get('action_description', '')} | {log.get('performed_by_name', '')} | {log.get('timestamp', '')}\n")
                    elif isinstance(log, tuple):
                        # ترتيب الأعمدة: [id, case_id, action_type, action_description, performed_by, timestamp, old_values, new_values, performed_by_name]
                        f.write(f"{log[2]} | {log[3]} | {log[8]} | {log[5]}\n")
            else:
                f.write("لا يوجد سجل تعديلات\n")
        try:
            os.startfile(temp_path, 'print')
            messagebox.showinfo("تمت الطباعة", "تم إرسال التقرير للطباعة بنجاح.")
        except Exception as e:
            messagebox.showerror("خطأ في الطباعة", f"حدث خطأ أثناء الطباعة:\n{e}")

    def update_cases_list(self):
        """
        تحديث عرض قائمة الحالات
        """
        if self.scrollable_frame is None:
            return
        # تنظيف القائمة الحالية
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.case_card_widgets = []
        # عرض الحالات المفلترة كبطاقات
        from customer_issues_functions import EnhancedFunctions
        ef = EnhancedFunctions(self)
        for i, case in enumerate(self.filtered_cases):
            card = ef.create_case_card(case, i, return_widget=True)
            self.case_card_widgets.append(card)
        # تحديث منطقة التمرير
        if hasattr(self, 'cases_canvas'):
            self.scrollable_frame.update_idletasks()
            self.cases_canvas.configure(scrollregion=self.cases_canvas.bbox("all"))
        # تمييز البطاقة المحددة
        self._highlight_selected_case_card()

    def save_changes(self):
        """حفظ أو تحديث بيانات الحالة في قاعدة البيانات"""
        if not messagebox.askyesno("تأكيد الحفظ", "هل أنت متأكد أنك تريد حفظ التغييرات؟"):
            return
        data = {}
        for key, widget in self.basic_data_widgets.items():
            if isinstance(widget, tk.Entry) or isinstance(widget, ttk.Combobox):
                data[key] = widget.get().strip()
            elif isinstance(widget, tk.Text):
                data[key] = widget.get('1.0', tk.END).strip()
        import logging
        logging.info(f"[DEBUG] القيم المجمعة من الواجهة: {data}")
        # معالجة الحقول المطلوبة
        required_fields = ['customer_name', 'subscriber_number']
        for field in required_fields:
            if not data.get(field):
                messagebox.showerror("خطأ في الإدخال", f"حقل '{field}' مطلوب.")
                return

        # تأكد من وجود جميع الحقول الخاصة بالمشكلة حتى لو كانت فارغة
        for field in ['problem_description', 'actions_taken', 'last_meter_reading', 'last_reading_date', 'debt_amount']:
            if field not in data:
                data[field] = ''

        # سجل محتوى البيانات قبل الحفظ للتشخيص
        import logging
        logging.info(f"[DEBUG] بيانات سيتم حفظها: {data}")
        # معالجة تصنيف المشكلة (category) وتحويله إلى category_id
        if 'category' in data:
            category_name = data['category']
            category_id = None
            for cat in enhanced_db.get_categories():
                if cat[1] == category_name:
                    category_id = cat[0]
                    break
            data['category_id'] = category_id
        # معالجة حالة المشكلة (status)
        if 'status' in data:
            data['status'] = data['status'] or 'جديدة'
        # إضافة تواريخ الإنشاء والتعديل
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emp_id = 1
        emp_name = data.get('employee_name')
        employees = enhanced_db.get_employees() if hasattr(enhanced_db, 'get_employees') else []
        for emp in employees:
            if emp[1] == emp_name:
                emp_id = emp[0]
                break
        if self.current_case_id is None:
            data['created_date'] = now
            data['modified_date'] = now
            data['created_by'] = emp_id
            data['modified_by'] = emp_id
            new_id = enhanced_db.add_case(data)
            self.current_case_id = new_id
            # سجل التعديلات
            if hasattr(enhanced_db, 'log_action'):
                enhanced_db.log_action(self.current_case_id, "إنشاء", "تم إنشاء الحالة", emp_id)
            messagebox.showinfo("تم الحفظ", "تمت إضافة الحالة بنجاح.")
        else:
            data['modified_date'] = now
            data['modified_by'] = emp_id
            enhanced_db.update_case(self.current_case_id, data)
            # سجل التعديلات
            if hasattr(enhanced_db, 'log_action'):
                enhanced_db.log_action(self.current_case_id, "تحديث", "تم تحديث بيانات الحالة", emp_id)
            messagebox.showinfo("تم الحفظ", "تم تحديث بيانات الحالة بنجاح.")
        self.save_btn.config(state='disabled')
        self.print_btn.config(state='normal')
        # إعادة تحميل المرفقات والمراسلات وسجل التعديلات للحالة الحالية
        if hasattr(self, 'functions') and self.functions is not None:
            if hasattr(self.functions, 'load_case_attachments'):
                self.functions.load_case_attachments(self.current_case_id)
            if hasattr(self.functions, 'load_case_correspondences'):
                self.functions.load_case_correspondences(self.current_case_id)
            if hasattr(self.functions, 'load_case_audit_log'):
                self.functions.load_case_audit_log(self.current_case_id)
        self.load_initial_data()

    def perform_search(self, event=None):
        """تنفيذ البحث وتحديث قائمة الحالات"""
        search_type = self.search_type_var.get()
        search_value = self.search_value_var.get().strip()
        year = self.year_var.get()
        # فلترة حسب السنة إذا تم اختيار سنة محددة
        if year and year != "الكل":
            cases = enhanced_db.get_cases_by_year(year)
        else:
            cases = enhanced_db.get_all_cases()
        # بحث متقدم إذا تم إدخال قيمة بحث
        if search_value:
            cases = enhanced_db.search_cases(search_type, search_value)
        self.filtered_cases = cases
        self.update_cases_list()

    def on_closing(self):
        """معالجة حدث إغلاق النافذة"""
        if messagebox.askokcancel("خروج", "هل تريد realmente الخروج؟"):
            self.root.destroy()
    
    def show_dashboard(self):
        self.clear_root()
        dash_frame = tk.Frame(self.root, bg='#f8f8f8')
        dash_frame.pack(fill='both', expand=True)
        tk.Label(dash_frame, text="لوحة عرض الحالات", font=('Arial', 22, 'bold'), bg='#f8f8f8').pack(pady=20)
        columns = ("اسم العميل", "رقم المشترك", "تصنيف المشكلة", "حالة المشكلة", "تاريخ الإضافة")
        tree = ttk.Treeview(dash_frame, columns=columns, show='headings', height=18)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        # Scrollbar رأسي
        scrollbar = ttk.Scrollbar(dash_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True, padx=30)
        scrollbar.pack(side='right', fill='y')
        # تحميل البيانات
        cases = enhanced_db.get_all_cases() if hasattr(enhanced_db, 'get_all_cases') else []
        for case in cases:
            tree.insert('', 'end', values=(
                case.get('customer_name', ''),
                case.get('subscriber_number', ''),
                case.get('category_name', ''),
                case.get('status', ''),
                case.get('created_date', '')
            ))
        tk.Button(dash_frame, text="دخول للنظام", font=('Arial', 16, 'bold'), bg='#3498db', fg='white', command=self.show_main_window).pack(pady=20)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_window(self):
        self.clear_root()
        self.create_main_layout()
        self.after_main_layout()

    def run(self):
        self.show_dashboard()
        self.root.mainloop()

    def load_case(self, case):
        """تحميل بيانات الحالة المختارة في النموذج"""
        # جلب بيانات الحالة كاملة من قاعدة البيانات (وليس فقط من القائمة)
        case_id = case.get('id')
        full_case = case
        if hasattr(enhanced_db, 'get_case_details'):
            db_result = enhanced_db.get_case_details(case_id)
            if isinstance(db_result, tuple):
                columns = [
                    'id', 'customer_name', 'subscriber_number', 'phone', 'address', 'category_id', 'status',
                    'problem_description', 'actions_taken', 'last_meter_reading', 'last_reading_date',
                    'debt_amount', 'created_date', 'created_by', 'modified_date', 'modified_by', 'solved_by',
                    'solved_date', 'category_name', 'color_code', 'created_by_name', 'modified_by_name', 'solved_by_name'
                ]
                full_case = dict(zip(columns, db_result))
            elif isinstance(db_result, dict):
                full_case = db_result
        self.current_case_id = case_id
        import logging
        logging.info(f"[DEBUG] تحميل بيانات الحالة: {full_case}")
        # تعبئة الحقول
        for key, widget in self.basic_data_widgets.items():
            value = full_case.get(key, '')
            # تصنيف المشكلة
            if key == 'category':
                # جلب اسم التصنيف من category_name أو تحويل category_id إلى اسم
                value = full_case.get('category_name', '')
                if (not value or value.isdigit() or value == full_case.get('category_id', '')):
                    cat_id = full_case.get('category_id')
                    categories = enhanced_db.get_categories() if hasattr(enhanced_db, 'get_categories') else []
                    for cat in categories:
                        if str(cat[0]) == str(cat_id):
                            value = cat[1]
                            break
                if isinstance(widget, ttk.Combobox):
                    options = list(widget['values'])
                    if value and value not in options:
                        widget['values'] = options + [value]
                    widget.set(value)
                    continue
            # حالة المشكلة
            if key == 'status':
                value = full_case.get('status', '')
                if isinstance(widget, ttk.Combobox):
                    options = list(widget['values'])
                    if value and value not in options:
                        widget['values'] = options + [value]
                    widget.set(value)
                    self.update_status_button_color(value)
                    continue
            # اسم الموظف
            if key == 'employee_name' and 'modified_by_name' in full_case:
                value = full_case.get('modified_by_name', '')
                if isinstance(widget, ttk.Combobox):
                    options = list(widget['values'])
                    if value and value not in options:
                        widget['values'] = options + [value]
                    widget.set(value)
                    continue
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, value if value is not None else '')
            elif isinstance(widget, ttk.Combobox):
                widget.set(value if value is not None else '')
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
                widget.insert('1.0', str(value) if value is not None else '')
        # تحديث العناوين
        self.customer_name_label.config(text=full_case.get('customer_name', ''))
        self.solved_by_label.config(text=full_case.get('modified_by_name', ''))
        self.save_btn.config(state='normal')
        self.print_btn.config(state='normal')
        self.load_attachments()
        self.load_correspondences()
        self.load_audit_log()
        # تعبئة التصنيف بالاسم فقط
        if 'category_name' in full_case and 'category' in self.basic_data_widgets:
            self.basic_data_widgets['category'].set(full_case.get('category_name', ''))
        # سنة الورود
        if 'created_date' in full_case and 'year_received' in self.basic_data_widgets:
            year = str(full_case.get('created_date', '')).split('-')[0] if full_case.get('created_date') else ''
            self.basic_data_widgets['year_received'].delete(0, 'end')
            self.basic_data_widgets['year_received'].insert(0, year)
        self.update_action_buttons_style()

    def delete_case(self):
        """حذف الحالة الحالية وكل بياناتها"""
        if not self.current_case_id:
            messagebox.showwarning("تنبيه", "يرجى اختيار حالة أولاً.")
            return
        if not messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذه الحالة وكل بياناتها؟ لا يمكن التراجع!"):
            return
        try:
            if hasattr(enhanced_db, 'delete_case'):
                enhanced_db.delete_case(self.current_case_id)
            # حذف ملفات المرفقات من النظام
            case_folder = os.path.join('files', f"case_{self.current_case_id}")
            if os.path.exists(case_folder):
                import shutil
                shutil.rmtree(case_folder)
            messagebox.showinfo("تم الحذف", "تم حذف الحالة وكل بياناتها بنجاح.")
            self.current_case_id = None
            self.load_initial_data()
            self.save_btn.config(state='disabled')
            self.print_btn.config(state='disabled')
            self.customer_name_label.config(text="اختر حالة من القائمة")
            self.solved_by_label.config(text="")
        except Exception as e:
            messagebox.showerror("خطأ في الحذف", f"حدث خطأ أثناء حذف الحالة:\n{e}")

    def show_all_cases_window(self):
        win = tk.Toplevel(self.root)
        win.title("جميع الحالات")
        win.geometry("900x500")
        columns = ("اسم العميل", "رقم المشترك", "تصنيف المشكلة", "حالة المشكلة", "تاريخ الإضافة")
        tree = ttk.Treeview(win, columns=columns, show='headings', height=20)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=170)
        tree.pack(fill='both', expand=True)
        # تعبئة البيانات
        for case in self.cases_data:
            if isinstance(case, dict):
                tree.insert('', 'end', values=(
                    case.get('customer_name', ''),
                    case.get('subscriber_number', ''),
                    case.get('category_name', ''),
                    case.get('status', ''),
                    case.get('created_date', '')
                ))
            elif isinstance(case, tuple):
                # ترتيب الأعمدة حسب get_all_cases
                # ['id', 'customer_name', 'subscriber_number', 'status', 'category_name', 'color_code', 'modified_by_name', 'created_date', 'modified_date']
                tree.insert('', 'end', values=(
                    case[1], case[2], case[4], case[3], case[7]
                ))
        tk.Button(win, text="إغلاق", command=win.destroy).pack(pady=10)

    def apply_sorting(self, event=None):
        def get_val(c, key, idx):
            if isinstance(c, dict):
                return c.get(key, '')
            elif isinstance(c, tuple):
                return c[idx] if len(c) > idx else ''
            return ''
        sort_type = self.sort_var.get()
        if sort_type == "السنة (تنازلي)":
            self.filtered_cases.sort(key=lambda c: get_val(c, 'created_date', 7), reverse=True)
        elif sort_type == "السنة (تصاعدي)":
            self.filtered_cases.sort(key=lambda c: get_val(c, 'created_date', 7))
        elif sort_type == "اسم العميل (أ-ي)":
            self.filtered_cases.sort(key=lambda c: get_val(c, 'customer_name', 1))
        elif sort_type == "اسم العميل (ي-أ)":
            self.filtered_cases.sort(key=lambda c: get_val(c, 'customer_name', 1), reverse=True)
        self.update_cases_list()

    def update_status_button_color(self, status_value):
        """تحديث لون زر أو شارة الحالة حسب القيمة (منطق الألوان فقط، بدون ربط مباشر بعناصر الواجهة)"""
        status_colors = {
            'جديدة': '#3498db',
            'قيد التنفيذ': '#f39c12',
            'تم حلها': '#27ae60',
            'مغلقة': '#95a5a6'
        }
        color = status_colors.get(status_value, '#95a5a6')
        # يمكن استخدام color عند رسم أي زر أو شارة حالة في أي مكان
        return color

    def update_action_buttons_style(self):
        """تحديث خصائص أزرار العمليات بعد أي تعديل"""
        for btn in [self.save_btn, self.print_btn]:
            btn.config(font=self.fonts['button'], relief='flat')
            if btn == self.save_btn:
                btn.config(bg='#27ae60', fg='white')
            elif btn == self.print_btn:
                btn.config(bg='#3498db', fg='white')

    def _on_case_list_up(self, event=None):
        if not self.case_card_widgets:
            return
        self.selected_case_index = max(0, self.selected_case_index - 1)
        self._highlight_selected_case_card()
        self._select_case_by_index()
    def _on_case_list_down(self, event=None):
        if not self.case_card_widgets:
            return
        self.selected_case_index = min(len(self.case_card_widgets) - 1, self.selected_case_index + 1)
        self._highlight_selected_case_card()
        self._select_case_by_index()
    def _highlight_selected_case_card(self):
        for idx, card in enumerate(self.case_card_widgets):
            if idx == self.selected_case_index:
                card.config(bg="#d1e7fd")
            else:
                card.config(bg="#ffffff")
    def _select_case_by_index(self):
        if 0 <= self.selected_case_index < len(self.filtered_cases):
            case = self.filtered_cases[self.selected_case_index]
            from customer_issues_functions import EnhancedFunctions
            ef = EnhancedFunctions(self)
            if isinstance(case, dict):
                ef.select_case(case.get('id'))
            elif isinstance(case, tuple):
                ef.select_case(case[0])