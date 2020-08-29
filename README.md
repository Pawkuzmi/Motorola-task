# Motorola Radio system
A simple service for device handling in a Motorola radio system.
 
## Running a server
To start the server go to the location with `docker-compose.yml` file, open the terminal
 and run `docker-compose up` command. The server will be available at `localhost`.

## Testing scenarios
In order to test the server, go to the `request_body` folder, open the terminal and
perform the following curl commands.

### Scenario 1

- `curl -d @post_radio100.json -H "Content-Type: application/json" -i -L localhost/radios/100` - post radio of id 100 with parameters given in json file

- `curl -d @post_radio101.json -H "Content-Type: application/json" -i -L localhost/radios/101` - post radio of id 100 with parameters given in json file

- `curl -d @location_CPH1.json -H "Content-Type: application/json" -i -L localhost/radios/100/location` - set location of radio 100 to CPH-1

- `curl -d @location_CPH3.json -H "Content-Type: application/json" -i -L localhost/radios/101/location` - set location of radio 101 to CPH-3

- `curl -d @location_CPH3.json -H "Content-Type: application/json" -i -L localhost/radios/100/location` - try to set location of radio 100 to CPH-3

- `curl -i -L localhost/radios/101/location` - get location of radio of id 101

### Scenario 2
- `curl -d @post_radio102.json -H "Content-Type: application/json" -i -L localhost/radios/102` - post radio of id 100 with parameters given in json file

- `curl -i -L localhost/radios/102/location` -  get location of radio of id 101
