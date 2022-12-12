from django.contrib import admin

# Register your models here.
from django.contrib import admin
from jobs.models import Job


# Register your models here.

class JobAdmin(admin.ModelAdmin):  # 在<应用app>/admin.py里定义模型管理器类
    list_display = ('job_type', 'job_name', 'job_city', 'creator', 'created_date', 'modified_date')  # 控制列表页面上显示哪些字段/

    exclude = ('created_date', 'modified_date', 'creator')  # 控制列表页面上隐藏哪些字段,   值得注意的是如果隐藏了这些字段，那么在新建数据得时候也不显示，所以需要重写save_model方法，这个方法在保存之前先做一些操作。

    def save_model(self, request, obj, form, change):
        # 重写Django自带的save_model方法。比如在文章创建时我们希望在后台自动添加作者，而不是允许用户自己选择作者是谁，我们可以选择在创建文章的表单里把作者隐藏，而在后台添加作者
        obj.create = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)  # 绑定注册模型类和注册管理器模型

# 将app的模型注册到admin里，
#
# 原因见：https://blog.csdn.net/peishuai1987/article/details/89882657?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522166366501016782414968750%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=166366501016782414968750&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-2-89882657-null-null.142^v47^new_blog_pos_by_title,201^v3^control_1&utm_term=admin.site.register&spm=1018.2226.3001.4187
