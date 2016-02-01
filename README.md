# Item catalog

Project #3 for Udacity's Full stack web developer nanodegree program by davcs86

## Usage

1. Clone the project source code

    ```bash
    $> git clone https://github.com/davcs86/fullstack-nanodegree-flask-item-catalog.git
    ```

1. Enter into the directory `fullstack-nanodegree-flask-item-catalog/vagrant`

    ```bash
    $> cd fullstack-nanodegree-flask-item-catalog/vagrant
    ```

1. Start the vagrant image ([Vagrant installation guide](https://www.vagrantup.com/docs/installation/)):

    ```bash
    $> vagrant up
    ```

1. Login to the vagrant instance via ssh

    ```bash
    $> vagrant ssh
    ```

1. Go to `/vagrant/catalog` directory

    ```bash
    $> cd /vagrant/catalog
    ```

1. Start the application with

    ```bash
    $> python ./application.py
    ```

1. Open [http://localhost:5000/](http://localhost:5000/) in your browser

## File structure

Base: `/vagrant/catalog`

`application.py` (File): Starts the flask application

`app` (Folder/Module): Has the app settings, utils classes and the app itself

`app/models` (Folder/Module): Has the model definitions for sqlalchemy

`app/routes` (Folder/Module): Has the controllers (business logic) for the app

`app/static` (Folder): Has the static content (css, js scripts and images) necessary for the views

`app/templates` (Folder): Has the jinja2 templates necessary for the views
