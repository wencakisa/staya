# Generated by Django 2.1.3 on 2018-11-02 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'amenities'},
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, default='', max_length=10000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='listings', to='listings.Location'),
            preserve_default=False,
        ),
    ]