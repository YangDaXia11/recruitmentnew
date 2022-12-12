"""
Django settings for recruitmentnew project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = r"/logs/"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0oltyg5$vpirtgtzws(zr!^=9@w-y76)z!$3gl!_c(x1cwr_ca'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobs',
    'interview',
    'debug_toolbar',
    'django_python3_ldap',

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'recruitmentnew.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'recruitmentnew.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
DEBUG_TOOLBAR_CONFIG = {
    # 访问本地jquery文件
    "JQUERY_URL": '',
    # 已存储请求的数量
    'RESULTS_STORE_SIZE': 100,
}

STATIC_URL = '/static/'

# 添加日志配置
LOGGING = {
    'version': 1,  # python里统一用法，只有一个版本
    'disable_existing_loggers': False,  # 是否禁用现在已有的其他logger，一般为false
    'formatters': {
        'simple': {  # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(lineno)d %(levelname)-8s %(message)s',
        },
    },

    # handlers这个类是确定logger中消息发生的引擎程序，描述特定的日志记录行为，譬如控制台打印、写入日志文件、通过网络进行发送等与logger一样，handler也具有日志级别，如果日志记录的日志级别未达到或超过handler的级别，则handler将忽略该消息。
    #  一个logger可以有多个handler，每个handler可以有不同的日志级别和记录方法
    'handlers': {
        'console': {  # 控制台输出
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },

        'mail_admins': {  # Add Handler for mail_admins for `warning` and above发邮件
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # 'file': {  # 将日志发送到指定的文件地址
        #     # 'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'simple',
        #     'filename': os.path.join(LOG_DIR, '../logs/recruitment.admin.log'),
        # },

        # 'performance': {
        #     # 'level': 'INFO',
        #     'class': 'logging.FileHandler',
        #     'formatter': 'simple',
        #     'filename': os.path.join(LOG_DIR, '../logs/recruitment.performance.log'),
        # },
    },

    # 'root': {
    #     'handlers': ['console', 'file'],     #设置同时在控制台和文件输出日志
    #     # 'handlers': ['console', ],
    #     'level': 'INFO',
    # },

    # 'loggers': {     #自定义的django_python3_ldap的日志
    #     "django_python3_ldap": {
    #         "handlers": ["console", "file"],
    #         "level": "DEBUG",      #DEBUG级别的才会记录下来
    #     },
    #
    #     "interview.performance": {
    #         "handlers": ["console", "performance"],
    #         "level": "INFO",
    #         "propagate": False,
    #     },
    # },
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# LDAP配置
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# LDAP_AUTH_URL = "ldap:/172.27.16.1:389/"
# LDAP_AUTH_URL = "ldap:/localhost:389/"
# LDAP_AUTH_USE_TLS = False
# LDAP_AUTH_SEARCH_BASE = 'dc=ihopeit,dc=com'
# LDAP_AUTH_OBJECT_CLASS = 'inetOrgPerson'  # 认证用户类型，哪些用户可以登录
# LDAP_AUTH_USER_LOOKUP_FIELDS = {
#     "username": "cn",
#     "fist_name": "givenNane",
#     "last_name": "sn",
#     "email": "mail",
# }
# LDAP_AUTH_USER_CONNECTION_FIELDS = ("username",)
#
# LDAP_AUTH_CLEAN_USER_DATA = 'django_python3_ldap.utils.clean_user_data'
# LDAO_AUTH_CONNECTION_USERNAME = None
# LDAP_AUTH_CONNECTION_PASSWORD = None
# AUTHENTICATION_BACKENDS = {'django_python3_ldap.auth.LDAPBackend', 'django.contrib.auth.backends.ModelBackend',}
