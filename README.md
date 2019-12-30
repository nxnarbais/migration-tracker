# Customer health check

## Get started

If you want to use a container:
```
docker run -v $(PWD):/src -p 5000:5000 --rm --name ddhc -it python:3 /bin/bash
cd src/
```

Then setup the `.env` file properly, check `.env.example` for an example.

Install the dependencies and launch the app
```
pip install --upgrade -r requirements.txt
python app.py
```

Once launched, start to go on [localhost:5000](http://localhost:5000)

## In production

**To be reviewed**

Setup the `.env` file.

Build the container:
```
docker build -d dd-healthcheck .
```

Run the container
```
docker run -d -p 5000:5000 dd-healthcheck
```

## How it works?

### Storage

To go faster, the app is storing the results from the api calls into files that you can find in the `/data` folder. The data can then be out of date regularly.

### API Calls

Some API calls are extremely time consuming:

- The host list since there are multiple pages
- The dashboard details since it has to be query on all dashboards to get the widgets in use.
