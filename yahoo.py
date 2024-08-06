import requests
import json

YAHOO_APP_ID = "dj0zaiZpPTRNZk0wUTh6VE1zcCZzPWNvbnN1bWVyc2VjcmV0Jng9Mjk-"
YAHOO_AFFILIATE_TYPE = "vc"
YAHOO_AFFILIATE_ID = "http://ck.jp.ap.valuecommerce.com/servlet/referral?sid=3587512%26pid=887076517%26vc_url="
YAHOO_IMAGE_SIZE = 600
YAHOO_ITEM_SEARCH_API = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"

def save_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def yahoo_item_search(query_parameters):
    query = f"appid={YAHOO_APP_ID}&affiliate_type={YAHOO_AFFILIATE_TYPE}&affiliate_id={YAHOO_AFFILIATE_ID}&image_size={YAHOO_IMAGE_SIZE}&price_from=2000&"

    for key, value in query_parameters.items():
        if value == "" or value is None:
            continue
        else:
            query += key + "=" + value + "&"

    url = f"{YAHOO_ITEM_SEARCH_API}?{query}"

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    items = []

    if response.status_code == 200:
        response_json = response.json()

        save_to_json_file(response_json,'./output/yahoo-api-data.json')

        if response_json.get("hits"):
            for i in response_json["hits"]:
                item = {}
                discountedPrice = i["priceLabel"]["discountedPrice"]
                defaultPrice = i["priceLabel"]["defaultPrice"]

                if defaultPrice > 0:
                    discountPercentage = ((defaultPrice - discountedPrice) / defaultPrice) * 100
                else:
                    discountPercentage = 0

                item = {
                    "item_id": f"ya_{i['code']}",
                    "title": i["name"],
                    "description": i["description"],
                    "headline": i["headLine"],
                    "availability": i["inStock"],
                    "affiliate_rate": i["affiliateRate"],
                    "price": i["price"],
                    "currency": "JPY",
                    "shop_id": i["seller"]["sellerId"],
                    "shop_name": i["seller"]["name"],
                    "review_count": i["review"]["count"],
                    "review_average": i["review"]["rate"],
                    "genre_id": i["genreCategory"]["id"],
                    "brand": i.get("brand").get("name"),
                    "shop_url": i["seller"]["url"],
                    "item_url": i["url"],
                    "image_urls": [i["exImage"]["url"]],
                    "tags": None,
                    "shipping_overseas": None,
                    "condition": 0 if i["condition"] == "used" else 1,
                    "genre_name": i["genreCategory"]["name"],
                    "shop_review_count": i["seller"]["review"]["count"],
                    "shop_review_average": i["seller"]["review"]["rate"],
                    "tax_included": i["priceLabel"]["taxable"],
                    "point_multiplier": i["point"]["times"],
                    "best_seller": i["seller"]["isBestSeller"],
                    "sale_start_time": i["priceLabel"]["periodStart"],
                    "sale_end_time": i["priceLabel"]["periodEnd"],
                    "parent_genre_categories": i["parentGenreCategories"],
                    "platform": "yahoo",
                    "discountedPrice": discountedPrice,
                    "defaultPrice": defaultPrice,
                    "fixedPrice": i["priceLabel"]["fixedPrice"],
                    "discountRate": discountPercentage
                }
                items.append(item)

    return items

query_parameters = {"query": "nike", "is_discounted": "true"}

items = yahoo_item_search(query_parameters)
save_to_json_file(items, "./output/yahoo.json")
