<h1 align="center"> Public Notes </h1>

<p align="center">
  <a href="https://github.com/Yu-Leo/public-notes/blob/main/LICENSE" target="_blank"> <img alt="license" src="https://img.shields.io/github/license/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/releases/latest" target="_blank"> <img alt="last release" src="https://img.shields.io/github/v/release/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/commits/main" target="_blank"> <img alt="last commit" src="https://img.shields.io/github/last-commit/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/Yu-Leo/public-notes/graphs/contributors" target="_blank"> <img alt="commit activity" src="https://img.shields.io/github/commit-activity/m/Yu-Leo/public-notes?style=for-the-badge&labelColor=090909"></a>
</p>

## Navigation

* [Project description](#chapter-0)
* [Interface](#chapter-1)
* [Getting started](#chapter-2)
* [Source code](#chapter-3)
* [License](#chapter-5)

<a id="chapter-0"></a>

## :page_facing_up: Project description

The website where users can write public notes.

See full description in [technical documentation](./docs/README.md).

<a id="chapter-1"></a>

## :camera: Interface

- **Main** - the main page of the site where all notes are displayed
- **About** - project information page
- **Categories** - distribution of notes by category
- **Categories list** - displaying categories as a list with different levels of
  nesting
- **Authors** - list of authors who wrote notes on the site
- **Add note** - form for adding notes (only for authorized users)
- **Search** - search by note titles
- **\<username\>** - user profile (only for authorized users)

![main_page](./docs/img/main_page.jpg)

![profile_page](./docs/img/profile_page.jpg)

![category_page](./docs/img/category_page.jpg)

<a id="chapter-2"></a>

## :hammer: Getting started - [tutorial](./docs/getting_started.md)

<a id="chapter-3"></a>

## :computer: Source code

### :books: [Technical documentation](./docs/README.md)

### :wrench: Technologies

#### BackEnd:

- DBMS: **PostgreSQL**
- Programming language: **Python (3.10.4)**
- Frameworks and libraries:
    - **Django 3.1**

#### FrontEnd:

- Languages: **HTML**, **CSS**
- Frameworks and libraries:
    - **Bootstrap 5**

#### Tools:

- **Docker** and **Docker compose**

### :coffee: Tests

Run all tests:

```bash
./publicnotes/manage.py test wall.tests

```

Using `coverage`:

```bash
coverage run ./publicnotes/manage.py test wall.tests
```

With report page generation:

```bash
coverage run ./publicnotes/manage.py test wall.tests && coverage html
```

<a id="chapter-5"></a>

## :open_hands: License

Author: [Yu-Leo](https://github.com/Yu-Leo)

[GNU General Public License v3.0](./LICENSE)

If you use my code, please put a star ⭐️ on the repository