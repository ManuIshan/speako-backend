# Generated migration for adding payment_id field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='payment_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]