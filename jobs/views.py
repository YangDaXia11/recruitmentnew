from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from jobs.models import Job, JobTypes, Cities, Resume
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
    # templates = loader.get_template('templates/joblist.html')    #返回一个Template对象
    context = {'job_list': job_list}  # Template对象的render(RequestContext)方法，使用context渲染模板
    for job in job_list:
        job.city_name = Cities[job.job_city][1]
        job.type_name = JobTypes[job.job_type][1]
    # return HttpResponse(templates.render(context))
    return render(request, 'joblist.html', context)

def detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = Cities[job.job_city][1]
    except Job.DoesNotExist:
        raise Http404('job not exist')
    return render(request, 'job.html', {'job': job})

class ResumeCreateView(LoginRequiredMixin,CreateView):
    #简历职位页面
    template_name = 'resume_form.html'
    success_url = '/joblist/'
    model = Resume
    fields = ("username", "city", "phone",
            "email", "apply_position", "born_address", "gender", "picture", "attachment",
            "bachelor_school", "master_school", "major", "degree",
            "candidate_introduction", "work_experience", "project_experience",)

 # def post(self, request, *args, **kwargs):
 #        form = ResumeForm(request.POST, request.FILES)
 #        if form.is_valid():
 #            # <process form cleaned data>
 #            form.save()
 #            return HttpResponseRedirect(self.success_url)
 #
 #        return render(request, self.template_name, {'form': form})

    ### 从 URL 请求参数带入默认值"""Return the initial data to use for forms on this view."""
    def get_initial(self):
        initial = {}
        for x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class ResumeDetailView(DetailView):
    template_name = 'resume_detail.html'
    success_url = '/resume-detail/'
    model = Resume