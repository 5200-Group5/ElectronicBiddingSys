from django.db import models

# Create your models here.


class ReportedIssue(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
    def __str__(self):
        return f'ReportedIssue {self.id}'
