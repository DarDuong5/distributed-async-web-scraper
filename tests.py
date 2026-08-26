from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from unittest.mock import patch

from handlers import parse_html
from app import app
from database import get_session, Base

def test_extract_and_parse():
    html = """
    <article class="product_pod">
        <h3><a title="Computer Science Book" href="#">Computer Science Book</a></h3>
        <p class="price_color">£10000.00</p>
    </article>
    <article class="product_pod">
        <h3><a title="Math Book" href="#">Math Book</a></h3>
        <p class="price_color">£7500.00</p>
    </article>
    <article class="product_pod">
        <h3><a title="Physics Book" href="#">Physics Book</a></h3>
        <p class="price_color">£5000.00</p>
    </article>
    """

    results = parse_html(html)
    assert results == {'Computer Science Book': '£10000.00',
                       'Math Book': '£7500.00',
                       'Physics Book': '£5000.00'}

def test_empty_extract_and_parse():
    html = ''

    results = parse_html(html)
    assert results == {}

def test_malformed_extract_and_parse():
    html = """
    <bad class="product_pod">
        <h3><invalid title="Computer Science Book" foo bar ref="#">Computer Science Book</a></h3>
        <p foooooo class="price_color">£10000.00</p>
    </article>
    <bad class="product_pod">
        <h3><invalid title="Math Book" foo bar ref="#">Math Book</b></h3>
        <p foooooo class="price_color">£7500.00</p>
    </article>
    <bad class="product_pod">
        <h3><invalid title="Physics Book" foo bar ref="#">Physics Book</c></h3>
        <p foooooo class="price_color">£5000.00</p>
    </article>
    """

    results = parse_html(html)
    assert results == {}

test_engine = create_engine('sqlite:///:memory:',
                            connect_args={'check_same_thread': False},
                            poolclass=StaticPool)

Base.metadata.create_all(bind=test_engine)

def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

@patch('app.fetch')
def test_post_app(mock_fetch):
    response = client.post('/jobs', json=['http://example.com/1', 'http://example.com/2'])
    assert response.status_code == 200
    jobs = response.json()
    assert len(jobs) == 2
    assert jobs[0]['id'] == 1
    assert jobs[0]['status'] == 'pending'
    assert jobs[0]['url'] == 'http://example.com/1'
    assert jobs[1]['id'] == 2
    assert jobs[1]['status'] == 'pending'
    assert jobs[1]['url'] == 'http://example.com/2'



