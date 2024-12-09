use ntex::web;

mod api;
mod ipfs;
mod jwt;
mod types;

#[web::get("/")]
async fn index() -> impl web::Responder {
    "Hello, World!"
}

#[web::get("/{name}")]
async fn hello(name: web::types::Path<String>) -> impl web::Responder {
    format!("Hello {}!", &name)
}

#[ntex::main]
async fn main() -> std::io::Result<()> {
    web::HttpServer::new(|| {
        let json_config = web::types::JsonConfig::default().limit(4000000);
        web::App::new()
            .service(index)
            .service(hello)
            .service(
                web::resource("/cat/{hash}")
                    .state(json_config.clone())
                    .route(web::get().to(api::cat::cat)),
            )
            .service(
                web::resource("/create")
                    .state(json_config.clone())
                    .route(web::post().to(api::create::create)),
            )
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}
