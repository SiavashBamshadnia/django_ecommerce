# Django Ecommerce

This is an ecommerce application built with Django. It provides a set of APIs that allow users to manage products,
categories, and users with custom fields such as Iranian phone number, name, sex, and birthdate. Some APIs require
authentication using Simple JWT. Additionally, this application uses MySQL as its database.

## APIs

This application provides APIs for managing products, categories, and users. The user APIs are secured with Simple JWT
authentication. The APIs are listed below:

### User APIs

The following user APIs are secured with Simple JWT authentication:

- `POST /api/token/`: Get a new access token by providing valid phone number and password in the request body
- `POST /api/token/refresh/`: Get a new access token by providing valid refresh token in the request body
- `POST /api/token/verify/`: Verify the validity of an access token by providing the token in the request body
- `POST /api/token/blacklist/`: Logout user by blacklisting the access and refresh token
- `POST /api/register/`: Register a new user by providing required user details in the request body. Required fields are
  phone number and password.

### Product APIs

- `GET /api/products/`: Get a list of all products
- `POST /api/products/`: Create a new product (needs authentication)

### Category APIs

- `GET /api/categories/`: Get a list of all categories
- `POST /api/categories/`: Create a new category (needs authentication)

## TODO

- Add UI.
- Add other API functions for the product and category model.
