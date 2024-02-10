from django.db import models
from django.conf import settings
import random
import os


class Contractor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='contractor')
    
    def __str__(self) -> str:
        return f'{self.user.username}'




def user_directory_path(instance, filename): 
    rand_int = random.randint(1,10000)
    base_name, extension = os.path.splitext(filename)
    return '{0}_{1}{2}'.format(instance.contractor.user.username,rand_int, extension)

class ExcelFile(models.Model):
    contractor = models.ForeignKey(Contractor,
                                    on_delete=models.CASCADE,
                                    related_name='contractor_docs')
    file = models.FileField(upload_to=user_directory_path)



    def __str__(self) -> str:
        return f'Sheet for - {self.contractor.user.username}'