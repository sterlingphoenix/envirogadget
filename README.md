# envirogadget
Gadget shoing temperature and humidity using Pimoroni Enviro.

Putting this here to make sure I have the new virtualenv-based method for installation. A lot more detail is available from my [EnviroPlus Prometheus Exporter](https://github.com/sterlingphoenix/enviroplus_exporter). 

**Note:** Assumes the raspberry pi is using the user `pi`. 

### Create virtual environment.

`python -m venv .virtualenvs/pimoroni`


### Install Pimoroni libraries.

Activate virtual environment:

`cd .virtualenvs/pimoroni`

`source /bin/activate`

Follow [Pimoroni's installation instructions](https://github.com/pimoroni/enviroplus-python/).

### Install script/service

* Install script in `/usr/local/bin`, make sure it is executable (i.e., `chmod 755`)
* Install service file in `/etc/systemd/system/`.
* Run `sudo systemctl enable envirogadget`
* Optional: sudo systemctl start envirogadget` to make sure it works.
* Optional: set system to read-only.
