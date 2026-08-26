from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(max_length=254),
        ),
    ]