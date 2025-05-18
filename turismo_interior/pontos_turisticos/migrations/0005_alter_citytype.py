from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pontos_turisticos', '0004_citytype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citytype',
            name='city',
        ),
        migrations.RemoveField(
            model_name='citytype',
            name='type',
        ),
        migrations.AddField(
            model_name='citytype',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='touristspot',
            name='city',
        ),
        migrations.AddField(
            model_name='touristspot',
            name='city',
            field=models.ForeignKey(default=1, on_delete=models.CASCADE, to='pontos_turisticos.city'),
            preserve_default=False,
        ),
    ] 