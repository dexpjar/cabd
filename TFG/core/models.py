from django.conf import settings
from django.db import models
from django.utils.timezone import now


class CommonInfo(models.Model):
    created_date = models.DateTimeField('Created Date', default=now, blank=True)
    last_modified_date = models.DateTimeField('Last modified', default=now, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER,verbose_name="Created by", blank=True, null=True, related_name="%(app_label)s_%(class)s_created")
    
    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = now()
        self.last_modified_date = now()
        super(CommonInfo,self).save(*args, **kwargs)
        
    class Meta:
        abstract = True