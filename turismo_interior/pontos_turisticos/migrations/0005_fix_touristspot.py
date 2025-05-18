from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('pontos_turisticos', '0004_citytype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touristspot',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='rating',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='touristspot',
            name='place_id',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='touristspot',
            name='description',
            field=models.TextField(blank=True),
        ),
    ] 