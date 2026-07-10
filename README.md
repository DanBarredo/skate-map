# skate-map


View skate spots, create new spots or add to favourites, navigate to them. The app uses VueJS with Maplibre on the frontend, and FastAPI on the backend.


## Frontend Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## Backend Setup
Install 'uv' Python package manager and run the following.
1. Initialize the project tracking environment (creates uv.lock)
```sh
uv lock
```

2. Sync and install all requirements into a local .venv folder instantly
```sh
uv sync
```

3. Run Docker compose to create postgres DB container.
```sh
docker compose up -d
```

4. Boot up your FastAPI development server using uv's fast execution layer
```sh
uv run uvicorn app.main:app --reload
```