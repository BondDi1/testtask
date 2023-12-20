import graphene
from django.db.models import Min

from graphene_django.types import DjangoObjectType
from .models import Product, Store, Category


class StoreType(DjangoObjectType):
    class Meta:
        model = Store


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ProductType(DjangoObjectType):
    class Meta:
        model = Product

    store = graphene.Field(StoreType)
    categories = graphene.List(CategoryType)

    def resolve_store(self, info):
        return self.store

    def resolve_categories(self, info):
        return self.categories.all()


class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)

    # def resolve_all_products(self, info):
    #     # using distinct('field1', 'field2') works only on PostgreSQL
    #     return Product.objects.values('store', 'categories') \
    #         .annotate(min_price=Min('price')) \
    #         .order_by('store', 'categories', 'price') \
    #         .distinct('store', 'categories')

    def resolve_all_products(self, info):
        min_prices = Product.objects.values('store_id', 'categories')\
                                    .annotate(min_price=Min('price'))

        product_ids = []
        for min_price in min_prices:
            product = Product.objects.filter(
                store_id=min_price['store_id'],
                categories=min_price['categories'],
                price=min_price['min_price']
            ).first()
            if product:
                product_ids.append(product.id)

        return Product.objects.filter(id__in=product_ids)

schema = graphene.Schema(query=Query)
