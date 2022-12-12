from django.shortcuts import render
from django.http import Http404
# Create your views here.
from jobs.models import Job, JobTypes, Cities
from django.template import loader
from django.http import HttpResponse

# Django处理模板分为两个阶段
# Step1 加载：根据给定的标识找到模板然后预处理，通常会将它编译好放在内存中
#       loader.get_template(template_name)，返回一个Template对象
# Step2 渲染：使用Context数据对模板插值并返回生成的字符串
#       Template对象的render(RequestContext)方法，使用context渲染模板
# 加载渲染完整代码：
# from django.template import loader, RequestContext
# from django.http import HttpResponse
#
# def index(request):
#     tem = loader.get_template('temtest/index.html')
#     context = RequestContext(request, {})
#     return HttpResponse(tem.render(context))


def joblist(request):
    job_list = Job.objects.order_by('job_type')
    templates = loader.get_template('joblist.html')    #返回一个Template对象
    context = {'job_list': job_list}  # Template对象的render(RequestContext)方法，使用context渲染模板
    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]
    return HttpResponse(templates.render(context))
# return render(request, 'temtest/detail.html', context)

def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404('job not exist')
    return render(request, 'job.html', {'job': job})
