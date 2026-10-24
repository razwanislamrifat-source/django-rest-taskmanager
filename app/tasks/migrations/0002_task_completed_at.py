# Generated manually for completed_at field
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
