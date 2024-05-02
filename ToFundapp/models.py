from django.db import models, migrations
import secrets
from .paystack import Paystack

class accounts(models.Model):
    email = models.EmailField()
    password = models.CharField( max_length= 100)

class Fund(models.Model):
    fund_name = models.CharField(max_length=100)
    duration_from = models.DateField()
    duration_to = models.DateField()
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField()
    Reason_for_fund = models.CharField(max_length=1000)

class donation(models.Model):
    email = models.EmailField(max_length=254)
    ref = models.CharField(max_length=50)
    amount = models.IntegerField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, default=None)  # Provide a default value here

    class Meta:
        ordering = ("date_created",)

    def __str__(self):
        return f"Amount: {self.amount}, Fund: {self.fund}"

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = secrets.token_urlsafe(50)
        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100

    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        return self.verified

    @classmethod
    def create_donation(cls, email, ref, amount, fund_id):
        fund = Fund.objects.get(pk=fund_id)  # Correct variable name
        donation_instance = cls(email=email, ref=ref, amount=amount, fund=fund)  # Correct field name
        donation_instance.save()
        return donation_instance

        





 
