import django.db.models.deletion
import mezzanine.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="_order",
            field=mezzanine.core.fields.OrderField(null=True, verbose_name="Order"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="productvariation",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.SET_NULL,
                verbose_name="Image",
                blank=True,
                to="shop.ProductImage",
                null=True,
            ),
            preserve_default=True,
        ),
    ]
