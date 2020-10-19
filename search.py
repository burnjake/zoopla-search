import click
import requests
from pprint import pprint


PROPERTY_LISTINGS_URL = "http://api.zoopla.co.uk/api/v1/property_listings"


def construct_request_url(api_key, **kwargs):
    # Set response as json
    params = ".js?api_key={0}".format(api_key)

    for key, value in kwargs.items():
        if value is not None:
            params += "&{0}={1}".format(key, value)

    return PROPERTY_LISTINGS_URL + params


@click.command()
@click.option("--api-key", required=True, type=str)
@click.option("--area", required=True, type=str)
@click.option("--radius", required=False, default="0.25", type=str)
@click.option("--bathrooms", required=False, type=int)
@click.option("--bedrooms", required=False, type=str)
@click.option("--price", required=False, type=str)
def main(api_key, area, radius, bathrooms, bedrooms, price):
    url = construct_request_url(api_key,
                                area=area,
                                radius=radius,
                                listing_status="rent",
                                minimum_beds=bedrooms,
                                maximum_beds=bedrooms,
                                maximum_price=price
                                )
    print(url)
    resp = requests.get(url)
    print(resp.status_code)
    pprint(resp.json())
    pprint([x["details_url"] for x in resp.json()["listing"] if int(x["num_bathrooms"]) >= bathrooms])


if __name__ == "__main__":
    main()
