# SlateBackend

This is the backend for the project Slate.

## Slate

![Logo](https://raw.githubusercontent.com/Waayway/slate-backend/main/logo.svg)

Slate is an note taking application that i am working on, it is mostly for me to learn so not very well commented.
I tried focussing on D&D note taking but haven't found a way yet to do this.

## DB

### Models for the DB

### Notes

- id: random char string
- name: Title or Name of the note
- type: describes what type it is, so SessionNote, City, Town etc
- content: content
- user: id of user.
- permission: a permission string, empty if none.
- createddate: date of creation
- updateddate: date of last update

### Parent

- id random string of ints
- name
- content
- childs

### User

- id: random char string
- username: username of string
- email: string of email of user
- password: string of the encrypted password of the user
- permissions: a array with the permissions of the user

## API

**GET Urls**

`/users/id/{id}` get user by id, of course no password

`/users/name/{name}` get user by name

`/parents/id/{id}` get parent by id

`/parents/name/{name}` get parent by name

`/notes` get all notes from your user

`/notes/id/{id}` get note by id

`/notes/name/{name}` get note by name

`/notes/parent/{id}` give id of note to get parent

**POST Urls**

`/login` Get a user and login so the server knows you're logged in. give a password and username

`/users` Create a user, give all arguments of userCreate from schemas in db

`/users/change` Change a user, only username and permissions

`/parents` Create a parent, parentCreate from schemas

`/parents/change` Change a parent, only name and content

`/parents/link` Link a Parent to a note, give arguments `parent: {id}, note: {id}`

`/notes` Create a note use createNote from db

`/notes/change` Change a Note only name, type, content. And updatedate will be updated automatically

`/notes/link` See `/parent/link`
