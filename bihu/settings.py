"""
Django settings for bihu project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

from .config import *
from .dbconfig import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9xg7iqn85&m479j8bx)jj+qv2=2x^z#w^gvzt((hrc4#6@k-^g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bihu.xiaoma0121.cn', "127.0.0.1"]

# django all-auth验证所需配置
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'users.adapters.SocialAccountAdapter'

# django-allauth注册发送邮件的配置
EMAIL_BACKEND = DJANGO_EMAIL_BACKEND
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = DJANGO_EMAIL_HOST
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_USE_SSL = DJANGO_EMAIL_USE_SSL
EMAIL_PORT = DJANGO_EMAIL_PORT
EMAIL_HOST_USER = DJANGO_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = DJANGO_EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = DJANGO_DEFAULT_FROM_EMAIL

# Application definition

# 使得INSTALLED_APPS扫描到apps文件夹下面的app应用
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# 重载django的user表
AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # app应用
    'users',
    'news',
    'articles',
    'qa',
    'messager',
    'notifications',
    'taskapp.celery.CeleryAppConfig',

    # 第三方应用所需包
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'sorl.thumbnail',
    'compressor',
    'allauth.socialaccount.providers.github',
    'taggit',
    'markdownx',
    'django_comments',
    'channels',  # 用于websocke协议的连接
    'debug_toolbar',
    'djcelery_email',
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [redis_host, ]  # channels缓存通道使用Redis 3
        },
    }
}
ASGI_APPLICATION = 'bihu.routing.application'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
CRISPY_TEMPLATE_PACK = 'bootstrap3'
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', ]
ROOT_URLCONF = 'bihu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'bihu.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,  # 数据库名字
        'USER': db_user,  # 账号
        'PASSWORD': db_password,  # 密码
        'HOST': db_host,  # IP
        'PORT': db_port,  # 端口
        'CONN_MAX_AGE': 9,
        "TEST": {
            'NAME': "test_for_bihu",
            'CHARSET': "utf8",
            'COLLATION': 'utf8_general_ci'
        },
        # 这里引擎用innodb（默认myisam）
        # 因为后面第三方登录时，要求引擎为INNODB
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},  # 这样设置会报错，改为
        # "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True

# 将系统改为中文
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Markdown相关设置 https://neutronx.github.io/django-markdownx/customization/#settings
MARKDOWNX_UPLOAD_MAX_SIZE = 5 * 1024 * 1024  # 允许上传的最大图片大小为5MB
MARKDOWNX_IMAGE_MAX_SIZE = {'size': (1000, 1000), 'quality': 100}  # 图片最大为1000*1000, 不压缩

# django-compressor
# ------------------------------------------------------------------------------
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_ENABLED
COMPRESS_ENABLED = True
# https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_URL
COMPRESS_URL = STATIC_URL

# Celery
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ['zanhu.taskapp.celery.CeleryAppConfig']
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = "redis://localhost:6379/1"  # 使用Redis 1作为消息代理
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = "redis://localhost:6379/2"  # 把任务结果存在Redis 2
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json', 'msgpack']  # 指定接受的内容类型
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'msgpack'  # 任务序列化和反序列化使用msgpack，msgpack是一个二进制的json序列化方案，比json数据结构更小，更快
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的json
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60  # 单个任务的最大运行时间5分钟
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60  # 任务的软时间限制，超时候SoftTimeLimitExceeded异常将会被抛出
