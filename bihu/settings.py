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
    'django_comments'
]

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
]

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
        "TEST":{
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
