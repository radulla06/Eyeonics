use rocket::serde::{Deserialize, json::Json};
use rocket::{config, fs};

use pyo3::{prelude::*, types::{IntoPyDict, PyModule}};

#[derive(Deserialize)]
#[serde(crate = "rocket::serde")]
struct Input<'r> {
    date_time: &'r str,
    distance: u8,
    base64_image: &'r str,
}

#[rocket::post("/postVisuals", format = "image/png;base64", data = "<file>")]
async fn upload(mut file: fs::TempFile<'_>) -> std::io::Result<()> {
    file.persist_to("./image.png").await
}

#[rocket::post("/postData", format = "json", data = "<input>")]
fn visuals(input: Json<Input<'_>>) -> f64 {
    let mut distance: f64 = 0;

    Python::with_gil(|py| {
        let activators = PyModule::from_code(std::include_str!("./deepNeuralNetwork.py"))?;
        
        distance = activators.getattr("identify_objects")?.call1("./image.png")?.extract()?;
    });

    distance
}

#[rocket::main]
async fn main() -> Result<(), rocket::Error> {
    let figment = config::Config::figment();

    let _rocket = rocket::custom(figment)
        .mount("/", rocket::routes![upload, visuals])
        .launch()
        .await?;

    Ok(())
}
