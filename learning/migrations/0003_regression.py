# Generated by Django 3.1.1 on 2020-10-15 17:39

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0002_auto_20201015_0134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regression',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickle', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
