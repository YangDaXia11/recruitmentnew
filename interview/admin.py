from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from interview.models import Candidate
import csv
from datetime import datetime
import logging
from interview.candidate_fieldset import fieldsets, default_list_first, default_list_second
from django.db.models import Q
from interview import dingtalk
from jobs.models import Resume

logger = logging.getLogger(__name__)
# Register your models here.
exportable_fields = (
    'username', 'phone', 'apply_position', 'gender', 'first_score', 'first_result', 'second_score', 'second_result',
    'hr_score', 'hr_result')


# 新需求：将要应聘的人通知给对应的一面面试官
def notify_interviewer(modeladmin, request, queryset):
    candidates = ''
    interviewer = ''
    for obj in queryset:
        candidates = obj.username + ';' + candidates
        interviewer = obj.first_interviewer_user.username + ';' + interviewer
        dingtalk.send('候选人%s进入面试环节，请面试官做好准备：%s' % (candidates, interviewer))
    messages.add_message(request, messages.INFO, '已经成功发送面试通知')

notify_interviewer.short_description = u'通知一面面试官'

# 将应聘者信息导入到新的csv表中(csv文件下载)
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text_csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),)
    # 写入表头
    writer = csv.writer(response)
    writer.writerow([queryset.model._meta.get_field(i).verbose_name.title() for i in field_list])

    for obj in queryset:
        # 将各个字段的值写入到csv文件
        csv_list_values = []
        for field in field_list:
            field_obj = queryset.model._meta.get_field(field)
            field_value = field_obj.value_from_object(obj)
            csv_list_values.append(field_value)
        writer.writerow(csv_list_values)
    # 推送日志，谁导出了多少条数据
    logger.info("%s exported %s candidate records" % (request.user, len(queryset)))
    return response


# 需求：要求普通一面二面面试官没有导出csv的权限
export_model_as_csv.short_description = u'导出为csv文件'  # 修改后后台显示新家功能的内容是导出为csv文件
export_model_as_csv.allowed_permissions = ('export',)  # 对这个导出功能设置权限


class CandidateAdmin(admin.ModelAdmin):
    actions = (export_model_as_csv,notify_interviewer,)  # 添加新功能
    exclude = ('modified_date', 'userid')
    list_display = (
        'username', 'phone','get_resume', 'gender', 'first_interviewer_user', 'first_score', 'first_result',
        'second_interviewer_user', 'second_score', 'second_result',
        'hr_score', 'hr_result')
    #新需求：当简历被hr通过传给应聘者列表时，希望面试官可以看到他的一些原始的数据，所以需要在列表页面自定义一个选项，跳转到相应详情列表
    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a' % (resumes[0].id, "查看简历"))#target="_blank"表示在新页面打开
        return ""

    get_resume.short_description = '查看简历'
    get_resume.allow_tags = True
    # def get_list_display(self, request):
    #     return ['username', 'phone', ]
    # 判断当前用户是否有csv导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    # fields = (
    #     'username', 'phone', 'apply_position', 'gender', 'first_score', 'first_result', 'second_score', 'second_result',
    #     'hr_score', 'hr_result')

    # 需求：不同面试官只能修改自己的面试官的选择，不能改变其他阶段的面试官的选择
    # 第一种方法：利用readonly_fields字段
    # readonly_fields = ('first_interviewer_user','second_interviewer_user','hr_interviewer_user')
    # 上诉的选择完以后谁都不能更改，但是要求是hr最后可以更改不同阶段面试官的人选
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interview' in group_names:
            logger.info("interviewer_user is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    # 新需求，要求一面面试官只能填写一面反馈，二面面试官只能填写二面反馈，
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interview' in group_names and obj.first_interviewer_user == request.user:
            return default_list_first
        if 'interview' in group_names and obj.second_interviewer_user == request.user:
            return default_list_second
        return fieldsets

    # list_editable = ('first_interviewer_user', 'second_interviewer_user')  # 在列表显示页面直接编辑内容
    # 要求只能hr才能指定一面二面的面试官，而不是所有人，所以要重写
    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    # 上述代码发现没有起到作用，因为django没有专门的方法，所以得重写其他方法，覆盖了list_editable方法的指定内容
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    # 新需求：进行数据的权限。要求一面只能看到一面的数据，二面只能看到二面的数据，hr和超级用户都能看到
    # 对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:
    def get_queryset(self, request):  # show data only owned by the user
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    empty_value_display = 'unknown'  # 表单没有内容的在列表显示时，显示unknown
    list_display_links = ('username', 'phone')  # 可以通过姓名和电话进入详情页
    list_max_show_all = 4
    list_per_page = 5  # 设置每页显示多少个项目
    # list_select_related = ('User','first_interviewer_user')
    prepopulated_fields = {"email": ("phone",)}  # 当输入phone的值时，email会自动填充phone的值
    preserve_filters = True  # 是否保存搜索记录

    # ordering = ['-paper_score']
    # 或重写get_ordering()方法
    def get_ordering(self, request):
        return ['-paper_score', ]

    # sortable_by = ['paper_score']#禁止对某些列进行排序，一个空的集合会禁用所有列的排序
    search_fields = ['username', 'userid', 'city', 'gender']  # 查询
    search_help_text = '对姓名、id、城市、性别进行查询'
    list_filter = ['apply_position', 'degree', 'first_result', 'second_result', 'hr_result']  # 筛选
    save_on_top = True  # 一般来说操作按钮都在最下面，true后操作在页面上下都有


admin.site.register(Candidate, CandidateAdmin)
