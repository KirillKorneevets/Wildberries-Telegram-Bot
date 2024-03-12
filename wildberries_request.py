import aiohttp


async def get_info(article_number):
    """
    Асинхронная функция для получения информации о товаре по его артикулу из API Wildberries.
    """
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article_number}"
    total_qty = 0

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                product_info = await response.json()
                if "data" in product_info and "products" in product_info["data"]:
                    products = product_info["data"]["products"]

                    if products:  
                        for product in products:
                            sizes = product.get("sizes", [])
                            for size in sizes:
                                stocks = size.get("stocks", [])
                                for stock in stocks:
                                    total_qty += stock.get("qty", 0)

                        name = products[0].get("name")
                        product_id = products[0].get("id")
                        sale_price = str(products[0].get("salePriceU"))
                        supplier_rating = products[0].get("supplierRating")
                        
                        sale_price = sale_price[:-2]

                        return {
                            "name": name,
                            "id": product_id,
                            "salePriceU": sale_price,
                            "total_qty": total_qty,
                            "rating": supplier_rating
                        }
                    else:
                        return None  
                else:
                    return None
            else:
                return None
            
            