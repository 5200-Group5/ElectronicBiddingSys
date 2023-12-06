from django.db import models

# Create your models here.


class ReportedIssue(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
    def __str__(self):
        return f'ReportedIssue {self.id}'

class transaction(models.Model):
    transaction_type = models.TextField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.TextField()   
    class Meta:
        db_table = 'bidding_transaction'
    def __str__(self):
        return f'transaction {self.id}'
