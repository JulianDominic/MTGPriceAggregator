# MTG Price Aggregator

## Table of Contents
- [MTG Price Aggregator](#mtg-price-aggregator)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
    - [Script](#script)
    - [Full Web Application](#full-web-application)
      - [Docker](#docker)
      - [Manual](#manual)
        - [Backend](#backend)
        - [Frontend](#frontend)
  - [Things to Take Note Of](#things-to-take-note-of)
  - [Future Updates](#future-updates)

Most recently, I have been learning fullstack development, and I decided to make this into a full web application.

This repository is split into two main sections:

1. Backend
2. Frontend

The backend contains `lgs.py` which is a script that sufficient to start searching for the cheapest card.

On the other hand, `app.py` is my [FastAPI](https://fastapi.tiangolo.com/) server.

The frontend uses [React](https://react.dev/?uwu=true) and [MUI](https://mui.com/).

The frontend doesn't just search for the cheapest card, it shows all the cards available, and you are able to sort by price instead.

## Usage

### Script

1. Make sure you have [Python](https://www.python.org/) installed and added to `PATH`.
2. Dowload/Clone the repository or just `lgs.py` and `requirements_script.txt` found in the backend.
3. Download the dependencies `pip install -r requirements_script.txt`.
4. Run the script.

``` bash
python lgs.py
```

### Full Web Application

For a start, download/clone the repository.

#### Docker

1. Make sure you have [Docker](https://www.docker.com/) installed.
2. Replace all instances of `YOUR_IP` in `docker-compose.yml` with the IP of the host machine/server you plan on running the web app on.
3. Similarly, replace `localhost` in `frontend/src/App.jsx`'s POST request with the IP used in step 2.
4. Simply run `docker compose up -d`.
5. The frontend will be accessible via `http://YOUR_IP:10015/`.

#### Manual

##### Backend

1. Make sure you have [Python](https://www.python.org/) installed.
2. Set your working directory to the backend `cd /path/to/backend`.
3. Download the dependencies `pip install -r requirements_app.txt`.
4. Run the backend `uvicorn app:app --reload`.

##### Frontend

1. Make sure you have [`npm`](https://www.npmjs.com/) installed.
2. Set your working directory to the frontend `cd /path/to/frontend`.
3. Download the node modules `npm install`.
4. Run the frontend `npm run dev`.

## Things to Take Note Of

> Tip: Agora has some really slow processing. Remove it to speed things up!

Do note that card name needs to have the correct spelling, and spelt exactly the same as the card. The script and web app are not case-sensitive.

For example, to find `Chandra's Ignition`, it cannot be `Chandras Ignition` -- the apostrophe is important.

## Future Updates

I intend to add the following functionality:

1. ~~Make the cards in the frontend clickable so that it redirects to the query page (not the specific card).~~ ✔️
2. Add a button to export a `csv` based on the cards chosen. It should contain (card name, store, price, link to query).
3. ~~Add the query link to the script output if it doesn't look too ugly.~~ ✔️
