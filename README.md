# Background Removal API

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-005CED?style=flat&logo=onnx&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=white)

A small, focused REST API: upload an image, get back a PNG with the background removed. Runs a local segmentation model — no external AI provider, no API key, no usage quota. Built as a standalone backend service — no frontend, no database.

## Endpoint

### `POST /api/remove-background`

**Headers**
- `X-API-Key` — required only if `API_ACCESS_KEY` is set on the server

**Body** — `multipart/form-data`
- `image` — the source image, `.png`, `.jpg`/`.jpeg`, or `.webp`

**Response**

A `image/png` binary — the same image with the background removed (transparent).

**Errors**
- `422` — unsupported file type or an empty/corrupt image
- `401` — missing or invalid `X-API-Key` (only if access control is enabled)

### `GET /api/health`

Returns `{"status": "ok"}`. Useful for uptime checks.

### `GET /docs`

Interactive Swagger UI — try the API directly from your browser.

## Example

```bash
curl -X POST https://your-deployment.onrender.com/api/remove-background \
  -H "X-API-Key: your-key-if-set" \
  -F "image=@photo.jpg" \
  -o cutout.png
```

## Tech stack

FastAPI, [rembg](https://github.com/danielgatis/rembg) (U2-Net segmentation model via ONNX Runtime), Pillow. No LLM, no third-party API key required — the model runs locally in the process.

## Running locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8100
```

The first request downloads the segmentation model (~4 MB, cached afterward). Then open `http://localhost:8100/docs` to try it interactively.

## Deploying

**Render:**
- New Web Service, root directory: repo root (no subfolder)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables: `API_ACCESS_KEY` (optional), `CORS_ORIGINS`

No frontend, no database, no LLM key — this is a pure backend API, deployable on its own.

## Status

This is an MVP built for portfolio purposes. `API_ACCESS_KEY` is optional; leave it empty for an open demo, or set it to require callers to authenticate. Uses the lightweight `u2netp` model for fast inference on free-tier hardware — image quality on complex edges (hair, fur, glass) is good but not pixel-perfect.
