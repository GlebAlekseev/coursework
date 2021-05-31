import random
random.seed(444)
hats = {}
Links_storage = {'Wildberries': ['https://wbxsearch.wildberries.ru/exactmatch/v2/common?query=REQUEST&_app-type=sitemobile',
								 'https://wbxcatalog-ru.wildberries.ru/BUCKET/catalog?PRESET&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub&page=PAGE',
								 'https://wbxcatalog-ru.wildberries.ru/SHARD/catalog?SUBJECT&search=NAME&page=PAGE&appType=2&spp=0&regions=68,75,69,40,48,33,70,64,1,4,38,30,71,22,31,66&stores=119261,122252,122256,117673,122258,122259,121631,122466,122467,122495,122496,122498,122590,122591,122592,123816,123817,123818,123820,123821,123822,124093,124094,124095,124096,124097,124098,124099,124100,124101,120762,119400,116433,507,3158,120602,6158,117501,121709,2737,117986,1699,1733,686,117413,119070,118106,119781&pricemarginCoeff=1&pricemarginMin=0&pricemarginMax=0&reg=0&emp=0&lang=ru&locale=ru&version=3&curr=rub'],
				 'my-shop':		['http://my-shop.ru/cgi-bin/shop2.pl?q=search&sort=z&page=PAGE&f14_6=REQUEST',
					  	    	 'https://my-shop.ru/cgi-bin/shop2.pl?q=product&id=3143442'],
				 'eldorado':	['https://www.eldorado.ru/sem/v3/a408/products?rootRestrictedCategoryId=0&query=REQUEST&orderField=popular&limit=50&offset=PAGE&regionId=11324',
								 'https://api.retailrocket.net/api/1.0/partner/5ba1feda97a5252320437f20/items/?itemsIds=71112985&stock=&format=json'],
					  	    	 }
