from mezzanine.conf import settings
from mezzanine.core.translation import TranslatedDisplayable, TranslatedRichText
from modeltranslation.translator import TranslationOptions, translator

from cartridge.shop.models import (
    Category,
    Product,
    ProductImage,
    ProductOption,
    ProductVariation,
)


class TranslatedProduct(TranslatedDisplayable, TranslatedRichText):
    fields = ()


class TranslatedProductImage(TranslationOptions):
    fields = ("description",)


class TranslatedProductOption(TranslationOptions):
    fields = ("name",)


class TranslatedProductVariation(TranslationOptions):
    fields = tuple("option%s" % opt[0] for opt in settings.SHOP_OPTION_TYPE_CHOICES)


class TranslatedCategory(TranslatedRichText):
    fields = ()


translator.register(Product, TranslatedProduct)
translator.register(ProductImage, TranslatedProductImage)
translator.register(ProductOption, TranslatedProductOption)
translator.register(ProductVariation, TranslatedProductVariation)
translator.register(Category, TranslatedCategory)
