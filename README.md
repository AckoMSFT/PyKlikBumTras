# PyKlikBumTras

python main.py --type authentication --authentication-url http://127.0.0.1:5000 --jwt-secret AckoCar123 --roles-field roles --owner-role owner --customer-role customer --courier-role courier
python main.py --type level2 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
python main.py --type level2 --with-authentication --authentication-url http://localhost:5000 --owner-url http://localhost:5001 --customer-url http://localhost:5002 --courier-url http://localhost:5003


PS C:\Users\aleks\Downloads\tests (1)\Tests> python main.py --type all --owner-role owner --customer-role customer --courier-role courier --roles-field roles --jwt-secret AckoCar123 --with-authentication --authentication-url http://127.0.0.1:5000 --owner-url http://127.0.0.1:5001 --customer-url http://127.0.0.1:5002 --courier-url http://127.0.0.1:5003
RUNNING AUTHENTICATION TESTS
==============================
AUTHENTICATION = 100.00%
==============================
RUNNING LEVEL 0 TESTS
==============================
LEVEL 0 = 100.00%
==============================
RUNNING LEVEL 1 TESTS
==============================
SKIPPED 11
SKIPPED 12
SKIPPED 13
LEVEL 1 = 100.00%
==============================
RUNNING LEVEL 2 TESTS
==============================
SKIPPED 0
SKIPPED 1
SKIPPED 2
SKIPPED 3
SKIPPED 4
SKIPPED 5
SKIPPED 6
SKIPPED 7
SKIPPED 8
SKIPPED 9
SKIPPED 10
SKIPPED 19
SKIPPED 20
SKIPPED 21
SKIPPED 22
SKIPPED 31
SKIPPED 32
SKIPPED 36
SKIPPED 37
SKIPPED 38
SKIPPED 39
SKIPPED 40
SKIPPED 41
LEVEL 2 = 100.00%
==============================
RUNNING LEVEL 3 TESTS
==============================
SKIPPED 8
SKIPPED 17
SKIPPED 27
LEVEL 3 = 100.00%
==============================
SCORE = 100.00%


http://127.0.0.1:5004/?server=authentication_database&username=root&db=authentication&select=user
http://127.0.0.1:5005/?server=shop_database&username=root&db=shop&sql=DELETE%20FROM%20product_category%3B%0AALTER%20TABLE%20product_category%20AUTO_INCREMENT%20%3D%200%3B%0ADELETE%20FROM%20order_product%3B%0AALTER%20TABLE%20order_product%20AUTO_INCREMENT%20%3D%200%3B%0ADELETE%20FROM%20%60order%60%3B%0AALTER%20TABLE%20%60order%60%20AUTO_INCREMENT%20%3D%200%3B%0ADELETE%20FROM%20product%3B%0AALTER%20TABLE%20product%20AUTO_INCREMENT%20%3D%200%3B%0ADELETE%20FROM%20category%3B%0AALTER%20TABLE%20category%20AUTO_INCREMENT%20%3D%200%3B%0A

IEPMetaMask123