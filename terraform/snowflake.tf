resource "snowflake_database" "sensor_data" {
  name = "sensor_data"
}

resource "snowflake_schema" "public" {
  name      = "public"
  database  = snowflake_database.sensor_data.name
}

resource "snowflake_table" "sensors" {
  name    = "sensors"
  schema  = snowflake_schema.public.name
  database = snowflake_database.sensor_data.name
  column {
    name = "id"
    type = "STRING"
    primary_key = true
  }
  column {
    name = "timestamp"
    type = "TIMESTAMP"
  }
  column {
    name = "temperature"
    type = "FLOAT"
  }
  column {
    name = "pressure"
    type = "FLOAT"
  }
}
