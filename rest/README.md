# Gatekeeper 

##### IPFS access management REST API
---

## Dependencies

- Docker
- Docker-compose
- Rust with cargo
---

## Starting the service
- ```bash 
  $ docker compose up
- ```bash
  $ cargo run
---

## API Calls

In Order to create a test JWT the test cases in src/jwt/mod.rs can be used.

#### Create Item
```bash
$ curl -X POST http://127.0.0.1:8080/create  -H "Content-Type: application/json" -d "{\"jwt\":\"eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJnYXRla2VlcGVyIiwiaXNzIjoicmVzY2FsZSIsImlhdCI6MTczMDc5NTU4MiwiZXhwIjoxNzMwODU1NTgyLCJ0Ym9tIjp7InRib20iOiJ0ZXN0In19.Yr9p2pL8GxDmbvJ6XyBIjmN2V4ES_faceBAynmWnCezjmA7kAV7J8dQoCyzOEq7R-1jrGAP0Mr9UipChXUbLtA\", \"public_key\":\"-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAElbf6R6Ha4Fqupjj5eMO/XLKnjqHoJjDthQUDV83uiUM7fovTzeeOoXWruFOzdHZfyAALVJAijh0FlRmr5vGP/w==\n-----END PUBLIC KEY-----\"}"
```

#### Get Item
```bash
curl -X POST http://127.0.0.1:8080/cat/QmSo1L92ZoCavjzwGXaANGB8HRRFi5yr9ehNBeeizofD24
```
