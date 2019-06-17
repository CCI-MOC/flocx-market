# flocx marketplace
Just a simple pecan app

# Instructions

1. clone the repo

2. cd flocx-market and run cmd:
```
pip install -r requirements.txt
```
3. migrate the database:
```
cd flocx_market/db/sqlalchemy
```
```
alembic upgrade head
```

# List available offers
1. First create a offer record in the marketplace database, offer table (from MySQL cmd line)
```
INSERT INTO offer VALUES (1,'b711b1ca-a77e-4392-a9b5-dc84c4f469ac','b9752cc0-9bed-4f1c-8917-12ade7a6fdbe','Alice1992','2016-07-16T19:20:30','available','Dell380','2016-07-16T19:20:30','2016-08-16T19:20:30',164,' {
    "new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.",
    "cpu_type": "Intel Xeon",
    "cores": 16,
    "ram_gb": 512,
    "storage_type": "samsung SSD",
    "storage_size_gb": 204
  }',11);
```
2. Run the pecan app:
```
PYTHONPATH=. python flocx_market/cmd/api.py
```
3. List the offers by type the url in broswer:
```
http://localhost:8080/v1/offers
```


