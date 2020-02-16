from app import db
from app.models import Address, District, City
from tests.test_client import FlaskClientTestCase


class ProductTestCase(FlaskClientTestCase):

    # Ensure product is inited
    def test_create(self):
        # address depend on district and city, create city first, following district.
        q1_dist_id = create_temp_district()

        address = Address(detail="Giang vo", district_id=q1_dist_id)
        self.assertTrue(address.detail, "Giang vo")

    # Ensure list product is showed
    def test_list_cate(self):
        with self.client:
            response = self.client.get('/address', follow_redirects=True)
            self.assertIn(b'Address Table', response.data)

    # Ensure product is created
    def test_create_address(self):
        with self.client:
            q1_dist_id = create_temp_district()

            response = self.client.post('/address/create', data={
                'address': "Giang Vo",
                'select-district': q1_dist_id,
            }, follow_redirects=True)

            self.assertIn(response.status, '200 OK')

    # Ensure api list address is working correctly

    def test_api_list_address(self):
        with self.client:
            response = self.client.get(
                '/address?page=1', follow_redirects=True)
            self.assertIn(response.status, '200 OK')


def create_temp_district():
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

    return q1_dist.id
