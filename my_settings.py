SECRET_KEY = 'django-insecure-5pl--lw9ka7u1qt4n1ed-vn0y$2in$-8ptne17qv*mqw+dhih3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'delay_api', 
        'USER': 'djangouser',                    
        'PASSWORD': 'djangouser',        
        'HOST': 'localhost',          
        'PORT': '3306',
    }
}