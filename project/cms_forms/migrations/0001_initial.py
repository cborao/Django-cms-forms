# Generated by Django 3.1.7 on 2021-05-04 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('Op', 'Opera'), ('Mu', 'Musical'), ('Te', 'Teatro'), ('Mo', 'Moderno'), ('Cl', 'Clasico')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64)),
                ('value', models.TextField()),
                ('topic', models.ManyToManyField(to='cms_forms.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('date', models.DateTimeField(verbose_name='published')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_forms.content')),
            ],
        ),
    ]
