[![Coverage Status](https://coveralls.io/repos/github/UB-ES-2020-A/Grup-ES/badge.svg?branch=main)](https://coveralls.io/github/UB-ES-2020-A/Grup-ES?branch=main)
[![Build Status](https://travis-ci.com/UB-ES-2020-A/Grup-ES.svg?branch=main)](https://travis-ci.com/UB-ES-2020-A/Grup-ES)
![GitHub release](https://img.shields.io/github/v/release/UB-ES-2020-A/Grup-ES)

<br />
<p align="center">
  <a href="https://github.com/UB-ES-2020-A/Grup-ES/">
    <img src="frontend/src/assets/bookshelter_icon1.png" alt="Logo" width="252" height="108">
  </a>

  <h3 align="center">Grup ES : Bookshelter</h3>

  <p align="center">
    An awesome web application to book and manage your favourite books.
    <br />
    <a href="https://grup-es.herokuapp.com/">View Demo</a>
    ·
    <a href="https://github.com/UB-ES-2020-A/Grup-ES/issues">Report Bug</a>
    .
    <a href="https://github.com/UB-ES-2020-A/Grup-ES/issues">Request Feature</a>
    .
    <a href="https://app.swaggerhub.com/apis-docs/grup-es/bookshelter/1.0.0">API Documentation</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is the project that has been done for the Software Engineering subject of the Computer Engineering degree at the University of Barcelona. This project has been developed following the different methodologies seen in class.


This website is based on the sale of books online in which users can search among a large number of books and can buy those they like the most. We also want this page to allow users to manage the books in the most comfortable way possible. For this, each user has their own library where the purchased books are added. In addition, they can also add books to their wish list to be able to acquire them in the near future.

We also want anyone responsible for maintaining the page to work in the best possible way. For that we want the administrator to have all the information about how the book sale is going on this page. The admin can also add the new titles available on the market, edit the information of an already added book, remove a book from the user's view, etc.

The page will also be the place where users can comment on the books and rate them so that it can be useful to other users in the community.

### Built With

Bookshelter web is divided in two parts: Frontend and Backend.

In the Backend part, the programming language used is [Python 3.6](https://www.python.org/). We have designed an API to manage all requests and data. So we used a popular light framework called [Flask](https://flask.palletsprojects.com/en/1.1.x/).

In the Frontend part, we have used web-oriented programming languages like [HTML](https://www.w3.org/html/) and [Javascript](https://www.javascript.com/). To make it easier, we've used [Vue.js](https://vuejs.org/) to design the user interface.
If we talk about Bookshelter's web design and appeareance, we have used [Bootstrap](https://getbootstrap.com) along with [BootstrapVue](https://bootstrap-vue.org/).



<!-- GETTING STARTED -->
## Getting Started

This project is build using PyCharm and Atom but these are not an actual requirement for running the project. You can just execute this project on localhost. In order to do that you will have to meet all the requirements described in this section and follow the instructions described in usage. 

### Prerequisites

- [python 3.6](https://www.python.org/) 
- [node.js](https://nodejs.org/)

### Installation

Once you have an enviroment of python 3.6 running with pip installed. You can simply run the following command to install all the dependencies:

`pip install -r deploy/requirements.txt`

If you want to be able to test and avaluate metrics like coverage you will need to install also the requirements for testing. Run the following command:

`pip install -r requirements_test.txt`

Once you have node.js running you can use npm to install all the dependencies. Just run the following command:

`npm run install` 

<!-- USAGE EXAMPLES -->
## Usage

As previously explained, the project is oriented to sell books where both users and administrators will mainly use the application through a web interface. However, there is a public API that would allow any user to create programs to interact with the database.

We will briefly explain how to use some of the features the product has.

First, on entering the main website locally or through our [main demo](https://grup-es.herokuapp.com/), we are welcomed with:

![portada](https://drive.google.com/uc?export=view&id=1pAkIN9BbcbIS8SXuUZprPaqpZPyK4CdA)

On clicking on any book, we can see more details about it.

![libro](https://drive.google.com/uc?export=view&id=1ynxVoRO1ExGkOTwmJoeEqKDWcDnLnjZb)

We can also search a specific book, through a basic search or click the three dots near the search button, to do an advance search.

![search](https://drive.google.com/uc?export=view&id=12htH2ouHhAkL_lmKhG7IuiFyXAvyDTU7)

Furthermore, when logged in, you can access at any point your library through clicking your profile name on the top left and selecting the option Biblioteca.

![biblioteca](https://drive.google.com/uc?export=view&id=1F-szYnHVsOXmimjjxxmyK2Jumw6JO1tD)

In case you logged in an admin account, you should be able to access the webpage of stock, through a similar procedure as before, but selecting the option Stock.

![stock](https://drive.google.com/uc?export=view&id=1jRpgz1fCDWqPBfke0xnVV6f4uTNMJzzK)

For the usage of the public API, please refer to the [API Documentation](https://app.swaggerhub.com/apis-docs/grup-es/bookshelter/1.0.0).

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/UB-ES-2020-A/Grup-ES/issues) for a list of proposed features (and known issues).


<!-- CONTACT -->
## Contact

- [Aarón Peruga Ortiga](https://github.com/aaronPeruga)
- [Francina Pons Llabrés](https://github.com/francinaPons)
- [Pau Bernabe Constans](https://github.com/paubernabe)
- [Guillem Molina Galera](https://github.com/gmolinga)
- [Ferran Sanchez Llado](https://github.com/ferranSanchezUB)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Postgres](https://www.postgresql.org/)
* [Sqlite](https://www.sqlite.org/index.html)
* [Pycharm](https://www.jetbrains.com/pycharm/)
* [Vue.js](https://vuejs.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
