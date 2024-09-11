openapi: 3.0.0
info:
  title: HavenStay API
  description: API for room bookings, table reservations, event management, and more.
  version: 1.0.0
servers:
  - url: 
    description: Production Server

tags:
  - name: Authentication
    description: Authentication for staff and admin.
  - name: Room Bookings
    description: Room booking and management endpoints.
  - name: Table Reservations
    description: Table reservation and management endpoints.
  - name: Venues
    description: Meeting and conference space management.
  - name: Events
    description: Event management.
  - name: Reviews
    description: Reviews and testimonials management.

paths:

  /api/auth/login:
    post:
      tags: 
        - Authentication
      summary: Authenticate staff or admin
      description: Authenticate a staff/admin with valid username and password.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  example: admin
                password:
                  type: string
                  example: password123
      responses:
        200:
          description: Successful authentication
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                    example: jwt_token_string
        401:
          description: Invalid credentials

  /api/auth/logout:
    post:
      tags:
        - Authentication
      summary: Log out staff or admin
      description: Invalidate the session token and log out the authenticated user.
      security:
        - bearerAuth: []
      responses:
        200:
          description: Logout successful
        401:
          description: Unauthorized

  /api/auth/user:
    get:
      tags:
        - Authentication
      summary: Get authenticated user details
      description: Retrieve the details of the logged-in staff/admin.
      security:
        - bearerAuth: []
      responses:
        200:
          description: User information retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  username:
                    type: string
                  role:
                    type: string
        401:
          description: Unauthorized

  /api/rooms:
    get:
      tags:
        - Room Bookings
      summary: Get list of all room types
      description: Retrieve the list of all available room types with their details.
      responses:
        200:
          description: List of room types
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    description:
                      type: string
                    price:
                      type: number
                      format: float

  /api/rooms/{id}:
    get:
      tags:
        - Room Bookings
      summary: Get room details by ID
      description: Retrieve detailed information of a specific room type by room ID.
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Room ID
      responses:
        200:
          description: Room details retrieved successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
                  price:
                    type: number
                    format: float
        404:
          description: Room not found

  /api/rooms/availability:
    get:
      tags:
        - Room Bookings
      summary: Check room availability
      description: Check room availability for specific check-in and check-out dates.
      parameters:
        - in: query
          name: check_in
          schema:
            type: string
            format: date
          required: true
          description: Check-in date
        - in: query
          name: check_out
          schema:
            type: string
            format: date
          required: true
          description: Check-out date
      responses:
        200:
          description: Room availability status
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    room_id:
                      type: integer
                    available:
                      type: boolean
                      example: true

  /api/bookings:
    post:
      tags:
        - Room Bookings
      summary: Create a new room booking
      description: Allows public users to create a new room booking.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                room_id:
                  type: integer
                user_info:
                  type: object
                  properties:
                    name:
                      type: string
                    email:
                      type: string
                check_in:
                  type: string
                  format: date
                check_out:
                  type: string
                  format: date
      responses:
        201:
          description: Booking created successfully
        400:
          description: Invalid request data

  /api/bookings/{id}:
    get:
      tags:
        - Room Bookings
      summary: Retrieve booking details by ID
      description: Retrieve details of a specific booking using the booking reference ID.
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Booking reference ID
      responses:
        200:
          description: Booking details retrieved
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  room_id:
                    type: integer
                  user_info:
                    type: object
                    properties:
                      name:
                        type: string
                      email:
                        type: string
                  check_in:
                    type: string
                    format: date
                  check_out:
                    type: string
                    format: date
        404:
          description: Booking not found

  /api/bookings/{id}:
    put:
      tags:
        - Room Bookings
      summary: Update a booking
      description: Modify an existing booking (admin only).
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Booking reference ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                check_in:
                  type: string
                  format: date
                check_out:
                  type: string
                  format: date
      responses:
        200:
          description: Booking updated successfully
        400:
          description: Invalid request data
        404:
          description: Booking not found
        403:
          description: Unauthorized to update booking

  /api/bookings/{id}:
    delete:
      tags:
        - Room Bookings
      summary: Cancel a booking
      description: Cancel a booking by reference ID or by admin privileges.
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Booking reference ID
      responses:
        200:
          description: Booking cancelled successfully
        404:
          description: Booking not found

# Additional paths for Table Reservations, Venues, Events, and Reviews should follow the same structure, using appropriate HTTP methods and parameters.

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Booking:
      type: object
      properties:
        id:
          type: integer
        room_id:
          type: integer
        check_in:
          type: string
          format: date
        check_out:
          type: string
          format: date
        user_info:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    Reservation:
      type: object
      properties:
        id:
          type: integer
        table_id:
          type: integer
        reservation_time:
          type: string
          format: date-time
        user_info:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
    Event:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        date:
          type: string
          format: date
    Review:
      type: object
      properties:
        id:
          type: integer
        content:
          type: string
        user_info:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
