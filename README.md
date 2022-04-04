# thundermeter

## [NATIVE] How to run

install django and other required packages (python)

python3 manage.py runserver

to run the indexer

python3 main.py

currently the indexer does a benchmark every couple minutes so you can add a time.sleep() to make that longer

## [Docker] How to run

`$ make start`

Go to http://localhost:8000/

Cheers!

## TODO

### Data
- [ ] Latency measurments need to be done on a different server. If the site gets too much traffic, it'll interfere with the computation.
- [ ] Running this on a different server enables making the requests from different regions, and therefore more visibility into the project.

### Product

- [ ] Add chains other than polygon (i.e. top 10 on pokt.network)
- [ ] Consider using www.timescale.com with postgres
- [ ] Don't store each harcoded percentile in the DB. Store raw data and pre-compute the latencies we're interested in (i.e. see Datadog)

### Model
- [ ] Add a table for request type so we can select/deselect it on the graph

### Infra
- [ ] Deploy dockerized container

### Code
- [ ]