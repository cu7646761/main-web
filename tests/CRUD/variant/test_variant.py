from app import db
from app.models import Product, Store, Color, Address, District, City, Category, Brand, ProductVariant
from tests.test_client import FlaskClientTestCase


class ProductVariantTestCase(FlaskClientTestCase):

    # Ensure product variant is inited
    def test_create(self):

        product_variant = ProductVariant(price=333)
        self.assertTrue(product_variant.price, 333)

    # Ensure list product  variant is showed
    def test_list_variant(self):
        with self.client:
            response = self.client.get('/variants', follow_redirects=True)
            self.assertIn(b'Product Variant Table', response.data)

    # Ensure product  variant is created
    def test_create_variant(self):
        with self.client:
            color_id = create_temp_color()
            store_id = create_temp_store()
            product_id = create_temp_product()

            response = self.client.post('/variants/api/create', data={
                'product_id': product_id,
                'store_id': store_id,
                'color_id': color_id,
                'product_variant_price': 333,
            }, follow_redirects=True)

            self.assertIn(response.status, '200 OK')

    # Ensure api list address is working correctly
    def test_api_list_address(self):
        with self.client:
            response = self.client.get(
                '/variants?page=1', follow_redirects=True)
            self.assertIn(response.status, '200 OK')

    # Ensure address is edit
    def test_edit_variant(self):
        with self.client:
            color_id = create_temp_color()
            store_id = create_temp_store()
            product_id = create_temp_product()

            product_variant = ProductVariant(
                color_id=color_id, store_id=store_id, product_id=product_id, price=333)
            db.session.add(product_variant)
            db.session.commit()

            response = self.client.post('/address/edit', data={
                'product_id': product_id,
                'store_id': store_id,
                'color_id': color_id,
                'price': 44,
                'id': 333,
            }, follow_redirects=True)
            self.assertIn(response.status, '200 OK')


def create_temp_store():
    try:
        hcm_city = City(name="Ho Chi Minh")
        db.session.add(hcm_city)
        db.session.commit()
    except:
        db.session.rollback()
        raise

    q1_dist = District(name="Quan 1", city_id=hcm_city.id)
    db.session.add(q1_dist)
    db.session.commit()

    address = Address(detail="Quan 1", district_id=q1_dist.id)
    db.session.add(address)
    db.session.commit()

    store = Store(store_name="Cua Hang A", address_id=address.id)
    db.session.add(store)
    db.session.commit()

    return store.id


def create_temp_color():
    color = Color(value="RED")

    return color.id


def create_temp_product():
    brand = Brand(name="samsung")
    db.session.add(brand)
    db.session.commit()

    category = Category(name="tivi", brand_id=brand.id)
    db.session.add(category)
    db.session.commit()

    product = Product(name="Tivi Sieu dep", category_id=category.id)
    db.session.add(product)
    db.session.commit()

    return product.id
