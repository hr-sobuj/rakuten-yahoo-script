import requests
import re
import json

RAKUTEN_AFFILIATE_ID = 1023148930846876394
BASE_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"


def save_to_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def rakuten_item_search(query_parameters):
    query = f"format=json&affiliateId={RAKUTEN_AFFILIATE_ID}&minPrice=2000&availability=1&applicationId={RAKUTEN_AFFILIATE_ID}&"

    keyword = ""
    for key, value in query_parameters.items():
        if key == "keyword":
            query += key + "=" + keyword + value + "&"
        else:
            query += key + "=" + value + "&"

    url = f"{BASE_URL}?{query}"

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    response = requests.request("GET", url, headers=headers)

    data = response.json()

    save_to_json_file(data, "rakuten-api-data.json")

    items = []

    if response.status_code == 200:
        response_json = response.json()

        for i in response_json.get("Items", []):
            item_name = i["Item"]["itemName"]

            discount_match = re.search(r"SALE／(\d+)%OFF", item_name, re.IGNORECASE)
            discount = discount_match.group(1) if discount_match else None

            if discount_match:
                item = {
                    "item_id": f"ra_{i['Item']['itemCode']}",
                    "title": item_name,
                    "description": i["Item"]["itemCaption"],
                    "headline": i["Item"]["catchcopy"],
                    "availability": True if i["Item"]["availability"] == 1 else False,
                    "affiliate_rate": i["Item"]["affiliateRate"],
                    "price": i["Item"]["itemPrice"],
                    "currency": "JPY",
                    "shop_id": i["Item"]["shopCode"],
                    "shop_name": i["Item"]["shopName"],
                    "review_count": i["Item"]["reviewCount"],
                    "review_average": i["Item"]["reviewAverage"],
                    "genre_id": i["Item"]["genreId"],
                    "brand": None,
                    "shop_url": i["Item"]["shopUrl"],
                    "item_url": i["Item"]["itemUrl"],
                    "tag_ids": i["Item"]["tagIds"],
                    "shipping_overseas": i["Item"]["shipOverseasArea"],
                    "condition": (
                        0
                        if "中古" in i["Item"]["itemName"] + i["Item"]["catchcopy"]
                        else 1
                    ),
                    "shop_review_count": None,
                    "shop_review_average": None,
                    "tax_included": True if i["Item"]["taxFlag"] == 0 else False,
                    "point_multiplier": i["Item"]["pointRate"],
                    "best_seller": (
                        True if i["Item"]["shopOfTheYearFlag"] == 1 else False
                    ),
                    "sale_start_time": i["Item"]["startTime"],
                    "sale_end_time": i["Item"]["endTime"],
                    "platform": "rakuten",
                    "discount": discount,
                }
                items.append(item)

    return items


query_parameters = {
    "keyword": "『臼田あさ美さん着用』『UR TECH』USAコットンロールスリーブTシャツ",
    "genreId": "303656",
    "model_cd": "KX4496",
}

items = rakuten_item_search(query_parameters)
save_to_json_file(items, "rakuten.json")
