from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pontos_turisticos', '0005_create_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='touristspot',
            name='city',
        ),
        migrations.AddField(
            model_name='touristspot',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pontos_turisticos.city'),
        ),
    ] 