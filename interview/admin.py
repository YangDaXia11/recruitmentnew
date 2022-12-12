from django.contrib import admin
from django.http import HttpResponse

from interview.models import Candidate
import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
# Register your models here.
exportable_fields = (
    'username', 'phone', 'apply_position', 'gender', 'first_score', 'first_result', 'second_score', 'second_result',
    'hr_score', 'hr_result')


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
    #推送日志，谁导出了多少条数据
    logger.info("%s exported %s candidate records" % (request.user,len(queryset)))
    return response


export_model_as_csv.short_description = u'导出为csv文件'  #修改后后台显示新家功能的内容是导出为csv文件


class CandidateAdmin(admin.ModelAdmin):
    actions = (export_model_as_csv,)  # 添加新功能
    exclude = ('modified_date', 'userid')

    # fields = (
    #     'username', 'phone', 'apply_position', 'gender', 'first_score', 'first_result', 'second_score', 'second_result',
    #     'hr_score', 'hr_result')
    list_display = (
        'username', 'phone', 'apply_position', 'gender', 'first_score', 'first_result', 'second_score', 'second_result',
        'hr_score', 'hr_result')
    # def get_list_display(self, request):
    #     return ['username', 'phone', ]
    list_editable = ('apply_position',)  # 在列表显示页面直接编辑内容
    empty_value_display = 'unknown'  # 表单没有内容的在列表显示时，显示unknown
    # 当页面的东西太多时，就可以用fieldsets来进行分组，同时也可以一行显示多个字段，只需要将放一行的字段变成元组就好。
    list_display_links = ('username', 'phone')  # 可以通过姓名和电话进入详情页
    fieldsets = (
        (None, {
            'fields': (("username", "city", "phone",), ("email", "apply_position"), ("born_address", "gender",
                                                                                     "candidate_remark"),
                       ("bachelor_school", "master_school", "doctor_school"),
                       ("major", "degree", "test_score_of_general_ability", "paper_score"),),
        }),
        ('第一轮面试记录', {
            'fields': (("first_score", "first_learning_ability", "first_professional_competency"),
                       ("first_advantage", "first_disadvantage", "first_result"),
                       ("first_recommend_position", "first_interviewer_user", "first_remark"),
                       ),
        }),
        ('第二轮面试记录', {
            'fields': (("second_score", "second_learning_ability", "second_professional_competency"),
                       ("second_pursue_of_excellence", "second_communication_ability", "second_pressure_score"),
                       ("second_advantage", "second_disadvantage", "second_result"),
                       ("second_recommend_position", "second_interviewer_user", "second_remark"),
                       ),
        }),
        ('第三轮面试记录', {
            'fields': (
                ("hr_score", "hr_responsibility", "hr_communication_ability"), ("hr_logic_ability", "hr_potential",
                                                                                "hr_stability"),
                ("hr_advantage", "hr_disadvantage", "hr_result"),
                ("hr_interviewer_user", "hr_remark", "creator", "last_editor"),)
        }),
    )

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
