from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_productimage_file_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="publish_date",
            field=models.DateTimeField(
                help_text="With Published chosen, won't be shown until this time",
                null=True,
                verbose_name="Published from",
                db_index=True,
                blank=True,
            ),
        ),
    ]
