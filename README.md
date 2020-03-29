# Brain Arts Site
Brain Arts Organization is a volunteer run 501(c)3 arts nonprofit for Greater Boston. Our mission is to create platforms for fringe artistic communities. Through our inclusive, participatory efforts, we aspire to uplift communities and fill cultural voids in our unique region of New England.

## Prerequisites
- Anaconda or Miniconda for environment management

## Environment Setup
- From the project directory run `conda env create -f environment.yml`
- Then `conda activate brain-arts`

## Test Server Usage
- To start a local test server run `flask run` from the project directory

## Dependencies
- Python 3
- Flask
- MySQL
- Pymysql
- python-dotenv
- markdown2
- flask-login
- python-slugify

## Host Server Setup
- Provision Ubuntu 18.04 Server from cloud provider
- Run automated initial server setup script
  - https://www.digitalocean.com/community/tutorials/automating-initial-server-setup-with-ubuntu-18-04
- Update system packages `sudo apt update && sudo apt upgrade -y`

### Apache
- Install apache `sudo apt install apache2`
- Adjust firewall to allow web traffic `sudo ufw allow in "Apache Full"`
- Check that apache is running `sudo systemctl status apache2`

### MySQL
- Install mysql server `sudo apt install mysql-server`
- Run interactive secure install script `sudo mysql_secure_installation`
- When prompted, remove anonymous users, the test database, disable remote login and load these new rules
- `CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';`
- `GRANT ALL PRIVILEGES ON * . * TO 'admin'@'localhost';`
- `FLUSH PRIVILEGES;`
- To switch the authentication method from auth_socket to mysql_native_password
	- `sudo mysql`
	- `ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';`
	- `FLUSH PRIVILEGES;`

### Deploy Flask
- Deploy flask app via apache:
	- https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/
	- https://modwsgi.readthedocs.io/en/develop/index.html

## Contact
**Jonathan Rodiger** - [jrodiger](https://github.com/jrodiger) - jon@brain-arts.org

## License
This project is licensed under the MIT license - see [LICENSE](LICENSE) for details
