# Comparte Ride

=============

In Mexico D.F, the pollution was so high, that the government reduced by law the number of cars in circulation, based on their license plate. Faced with this situation, people began to share their ride. Let's say: if Tom has 3 seats in his car, he can take 3 more with him. People can also join to groups, in where others can share their rides. But you need to be invited by other one if you want to be in that group.

`Comparte Ride` is the app that models this situation, in order to scale to a city like Mexico D.F. It is composed by 3 main phases:

- Invitation: An user joins to a group through an -invitation-. Every user has a limited number of invitations inside each group.
- Ride: Inside a group a member (or user), can offer or join a trip. Just a defined number of users can join a trip. (Remember the example of Tom, he has just 3 seats)
- Rating: At the end of the trip, users rate the experience. Every user has a general reputation and is public in its groups (or circles).

## The entities of the bussines logic

This is a description of the main entities that compose the bussines logic of Comparte Ride.

### The user models

Base

- Email
- Username
- Phone number
- First name
- Last name

Perfil

- User(Pk)
- Biography(about me)
- Rides taken(total)
- Rides offered (total)

Membership

- User(Pk)/ Profile(PK)
- Circle (Pk)
- IsAdminCircle (BOOL)
- UsedInvitations (Int)
- RemainingInvitations(Int)
- InvitedBy
- Rides taken (Inside circle)
- Rides offered (Inside circle)

### The circle models

Circle

- Nombre
- Slug name
- About
- Picture
- Members
- Rides taken
- Rides offered
- IsOfficial (BOOL)
- IsPublic (BOOL)
- LimitMember(Int)
- HasLimit(BOOL)

Invitation

- Code
- Circle (PK)
- InvitedBy
- UsedBy
- DateUsed

### The ride models

Ride

- OfferedBy
- Where
- When
- Seats
- Comments
- Calification
- IsActive (BOOL)

Rating

- Ride (PK)
- Circle (PK)
- RatedBy
- Who rates
- Scoring (1-5)

## Logic features between entities

Users

- Sign up (email confirmation)
- Log in
- User Details
- DB actualization
    * Profile
    * Base

Circles

- List all circles (filter, and search)
- Create a circle
- Circle details
- Data actualization
(Yep it's a CRUD)

- List circle members
- Join circle (invitation required)
- Members details
- Delete member
- Get invitation code

Rides

- List rides (filter and search)
- Create a ride in a circle
- Join to ride
- Rating a ride
- Send reminder to users to rate

## The final app

The final app is an API-REST, that can express in URL format, all the info that could need a frontend part (mobile or web) of `Comparte Ride`. You can even play with the final product using a graphic interface like `Postman`, or a cli command like `httpie`.

## The development stage

### The structure

The application uses [cookiecuter-django-api](https://github.com/gianfrancolombardo/cookiecutter-django-api). This template bring a boilerplate with 4 docker services: Postgres, Django, Redis, and Celery. Celery is splitted in 3 docker images: celeryworker, celerybeat and flowers (a graphic interface for see the celery tasks in real time). The django container actualize the code on the fly when we running it locally: we write the base code, on our machine, and we can see the changes on the container when we save it (That's an amazing feature, by the way). We also have here, all the necesary configuration in order to deploy locally our app, and develop it. Just simply run:

- `sudo docker-compose -f local.yml build`
- `sudo docker-compose -f local.yml up`

And you will have everything to start to develop :)

### The tools

It is used django rest framework:

- Mixins view classes
- Serializers
- Permissions

### The apps

We define three apps:

- circles
- rides
- users

In each one, you will see models, views, serializers, and permissions. All the bussines logic, and how it is mapped to URL's, in order to conform the endpoint.

## Deployment

I will deploy it to heroku, very soon!
