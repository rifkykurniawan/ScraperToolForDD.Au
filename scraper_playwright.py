import csv
import re
import json
import asyncio
from playwright.async_api import async_playwright

OUTPUT_FILE = "MELBOURNE_Café_and_Family Dining.csv"
#Fine_Dining
#Café_and_Family_Dining
#Informal_Dining_and_Takeaway
#Attractions_and_Activities
#Retail_and_Local_Services
#Travel_&_Leisure

REGIONS = [
    "melbourne",
]

CATEGORIES = [
    "cafe",
    #fine,cafe,takeaway,activity,services,travel
]

LIMIT = 30

# True = ambil 1 data saja
# False = scrape semua data
TEST_ONE_ONLY = False


async def get_offer_detail(page, uuid):

    detail_url = (
        "https://www.entertainment.com.au/"
        f"offer-details/{uuid}"
    )

    try:

        print(f"OPEN DETAIL: {uuid}")

        await page.goto(
            detail_url,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        await page.wait_for_timeout(3000)

        html = await page.content()

        # =========================
        # AMBIL JSON DARI HTML
        # =========================

        json_match = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            html,
            re.DOTALL
        )

        if not json_match:

            return {
                "editorial": "",
                "rules": []
            }

        raw_json = json_match.group(1)

        data = json.loads(raw_json)

        # =========================
        # CARI OFFER DATA RECURSIVE
        # =========================

        def find_offer_data(obj):

            if isinstance(obj, dict):

                # jika ada merchant + rules
                if (
                    "merchant" in obj
                    and "rules" in obj
                ):
                    return obj

                for value in obj.values():

                    result = find_offer_data(value)

                    if result:
                        return result

            elif isinstance(obj, list):

                for item in obj:

                    result = find_offer_data(item)

                    if result:
                        return result

            return None

        offer_data = find_offer_data(data)

        if not offer_data:

            return {
                "editorial": "",
                "rules": []
            }

        # =========================
        # MERCHANT EDITORIAL
        # =========================

        merchant = offer_data.get(
            "merchant",
            {}
        )

        editorial = merchant.get(
            "editorial",
            ""
        )

        if editorial:

            editorial = editorial.strip()

        # =========================
        # RULES OF USE
        # =========================

        rules_raw = offer_data.get(
            "rules",
            []
        )

        rules = []

        for rule in rules_raw:

            if not rule:
                continue

            clean_rule = str(rule).strip()

            if clean_rule:

                rules.append(
                    f"• {clean_rule}"
                )

        return {
            "editorial": editorial,
            "rules": rules
        }

    except Exception as e:

        print(
            f"DETAIL ERROR {uuid}: {e}"
        )

        return {
            "editorial": "",
            "rules": []
        }


async def scrape():

    all_results = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        page = await browser.new_page()

        stop_scraping = False

        for region in REGIONS:

            if stop_scraping:
                break

            for category in CATEGORIES:

                if stop_scraping:
                    break

                print(
                    f"\nSCRAPING {region} - {category}"
                )

                url = (
                    "https://www.entertainment.com.au/"
                    f"offers-list/all?"
                    f"sort=curatedOffers"
                    f"&region={region}"
                    f"&offerCategory={category}"
                    f"&id=all"
                )

                await page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=60000,
                )

                start = 0

                while True:

                    api_url = (
                        "https://www.entertainment.com.au/"
                        "api/dynamicoffers?"
                        f"offerSubCategories={category}"
                        f"&offerCategory={category}"
                        f"&latitude=-33.8688"
                        f"&longitude=151.2093"
                        f"&start={start}"
                        f"&limit={LIMIT}"
                        f"&search="
                        f"&redeemable=display"
                        f"&sort=curatedOffers"
                        f"&region={region}"
                    )

                    response = await page.request.get(
                        api_url,
                        headers={
                            "accept": "application/json"
                        }
                    )

                    print(
                        f"PAGE start={start} "
                        f"STATUS={response.status}"
                    )

                    if response.status != 200:
                        break

                    data = await response.json()

                    offers = data.get(
                        "results",
                        []
                    )

                    print(
                        f"Offers: {len(offers)}"
                    )

                    if not offers:
                        break

                    for offer in offers:

                        if (
                            TEST_ONE_ONLY
                            and all_results
                        ):
                            stop_scraping = True
                            break

                        uuid = offer.get("uuid")

                        print(
                            f"DETAIL -> {uuid}"
                        )

                        # =========================
                        # DETAIL DATA
                        # =========================

                        detail = await get_offer_detail(
                            page,
                            uuid
                        )

                        # =========================
                        # BASIC DATA
                        # =========================

                        merchant = offer.get(
                            "merchant",
                            {}
                        )

                        location = offer.get(
                            "nearestLocation",
                            {}
                        )

                        # =========================
                        # CATEGORY
                        # =========================

                        category_data = offer.get(
                            "offerCategory",
                            {}
                        )

                        category_display = (
                            category_data.get(
                                "displayValue",
                                ""
                            )
                        )

                        # =========================
                        # SUB CATEGORY
                        # =========================

                        subcategories = offer.get(
                            "offerSubCategories",
                            []
                        )

                        subcategory_display = ", ".join([

                            sub.get(
                                "displayValue",
                                ""
                            )

                            for sub in subcategories

                            if sub.get(
                                "displayValue"
                            )

                        ])

                        all_results.append({

                            "uuid": uuid,

                            "category":
                                category_display,

                            "sub_category":
                                subcategory_display,

                            "name": offer.get(
                                "name"
                            ),

                            "title": offer.get(
                                "title"
                            ),

                            "subtitle": offer.get(
                                "subtitle"
                            ),

                            "summary": offer.get(
                                "summary"
                            ),

                            "website": merchant.get(
                                "website"
                            ),

                            "merchant_editorial":
                                detail.get(
                                    "editorial"
                                ),

                            "rules":
                                "\n".join(
                                    detail.get(
                                        "rules",
                                        []
                                    )
                                ),

                            "address":
                                location.get(
                                    "formattedAddress"
                                ),

                            "city":
                                location.get(
                                    "city"
                                ),

                            "state":
                                location.get(
                                    "state"
                                ),

                            "phone":
                                location.get(
                                    "phone"
                                ),

                            "latitude":
                                location.get(
                                    "latitude"
                                ),

                            "longitude":
                                location.get(
                                    "longitude"
                                ),

                            "detail_url": (
                                "https://www.entertainment.com.au/"
                                f"offer-details/{uuid}"
                            )
                        })

                        await asyncio.sleep(1)

                    if stop_scraping:
                        break

                    # next page
                    start += LIMIT

                    await asyncio.sleep(1)

        await browser.close()

    # =========================
    # REMOVE DUPLICATE
    # =========================

    unique = {
        item["uuid"]: item
        for item in all_results
    }

    final_results = list(unique.values())

    if not final_results:

        print("NO DATA FOUND")
        return

    # =========================
    # SAVE CSV
    # =========================

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=final_results[0].keys()
        )

        writer.writeheader()

        writer.writerows(
            final_results
        )

    print(
        f"\nDONE -> {OUTPUT_FILE}"
    )

    print(
        f"Total unique offers: "
        f"{len(final_results)}"
    )


asyncio.run(scrape())