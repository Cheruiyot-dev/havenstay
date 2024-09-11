openapi: 3.0.0
info:
  title: HavenStay API
  description: API for room bookings, table reservations, event management, and reviews for HavenStay.
  version: "1.0.0"

servers:
  - url: https://api.havenstay.com/v1
    description: Production Server
  - url: http://localhost:8000
    description: Development Server

paths:
  /auth/login:
    post:
      summary: Log in staff/admin users
      description: Authenticate staff or admin users using their credentials.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
              required:
                - username
                - password
      responses:
        200:
          description: Successful login
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token:
                    type: string
                  token_type:
                    type: string
        401:
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /auth/logout:
    post:
      summary: Log out staff/admin users
      description: Invalidate the user's session token.
      security:
        - bearerAuth: []
      responses:
        204:
          description: Successful logout

  /auth/user:
    get:
      summary: Retrieve authenticated user information
      security:
        - bearerAuth: []
      responses:
        200:
          description: Return the currently authenticated user
          content:
            application/json:
              schema:
                type: object
                properties:
                  username:
                    type: string
                  role:
                    type: string
        401:
          description: Unauthorized access
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /rooms:
    get:
      summary: Get list of available rooms
      description: Retrieve all room types and their details.
      responses:
        200:
          description: A list of rooms
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Room'

  /rooms/{id}:
    get:
      summary: Get details of a specific room
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: The ID of the room
      responses:
        200:
          description: Room details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Room'
        404:
          description: Room not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /rooms/availability:
    get:
      summary: Check room availability for a specific date range
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
                type: object
                properties:
                  available:
                    type: boolean
        400:
          description: Invalid date format
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /bookings:
    post:
      summary: Create a new room booking
      description: Create a booking for a room, no authentication required.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        201:
          description: Booking created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        400:
          description: Invalid booking details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /bookings/{id}:
    get:
      summary: Get booking details by reference ID
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Booking reference ID
      responses:
        200:
          description: Booking details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        404:
          description: Booking not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

    put:
      summary: Modify a booking (admin only)
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BookingRequest'
      responses:
        200:
          description: Booking updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookingResponse'
        401:
          description: Unauthorized access
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

    delete:
      summary: Cancel a booking (admin or user)
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Booking reference ID
      responses:
        204:
          description: Booking successfully cancelled
        401:
          description: Unauthorized access
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /restaurants:
    get:
      summary: Get list of available tables
      description: Retrieve all table details.
      responses:
        200:
          description: A list of tables
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Table'

  /restaurants/{id}:
    get:
      summary: Get table details
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Table ID
      responses:
        200:
          description: Table details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Table'
        404:
          description: Table not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /restaurants/{id}/availability:
    get:
      summary: Check table availability for a specific date and time
      parameters:
        - in: path
          name: id
          schema:
            type: integer
          required: true
          description: Table ID
        - in: query
          name: date_time
          schema:
            type: string
            format: date-time
          required: true
          description: Reservation date and time
      responses:
        200:
          description: Table availability
          content:
            application/json:
              schema:
                type: object
                properties:
                  available:
                    type: boolean
        404:
          description: Table not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

  /reservations:
    post:
      summary: Create a table reservation
      description: Reserve a table for a specified time.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReservationRequest'
      responses:
        201:
          description: Reservation created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReservationResponse'

  /events:
    get:
      summary: Get list of all events
      description: Retrieve all past and upcoming events.
      responses:
        200:
          description: A list of events
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Event'

  /reviews:
    get:
      summary: Get list of all reviews
      description: Retrieve reviews and testimonials submitted by users.
      responses:
        200:
          description: A list of reviews
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/ReviewResponse'

  /reviews:
    post:
      summary: Submit a new review
      description: Public users can submit reviews or testimonials.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReviewRequest'
      responses:
        201:
          description: Review submitted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ReviewResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:

    Room:
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
        available:
          type: boolean

    BookingRequest:
      type: object
      properties:
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
      required:
        - room_id
        - check_in
        - check_out
        - user_info

    BookingResponse:
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

    Table:
      type: object
      properties:
        id:
          type: integer
        description:
          type: string
        capacity:
          type: integer

    ReservationRequest:
      type: object
      properties:
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
      required:
        - table_id
        - reservation_time
        - user_info

    ReservationResponse:
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

    Venue:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        capacity:
          type: integer

    VenueBookingRequest:
      type: object
      properties:
        venue_id:
          type: integer
        event_name:
          type: string
        event_date:
          type: string
          format: date
        user_info:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
      required:
        - venue_id
        - event_name
        - event_date
        - user_info

    VenueBookingResponse:
      type: object
      properties:
        id:
          type: integer
        venue_id:
          type: integer
        event_name:
          type: string
        event_date:
          type: string
          format: date
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

    EventRequest:
      type: object
      properties:
        name:
          type: string
        description:
          type: string
        date:
          type: string
          format: date
      required:
        - name
        - date

    EventResponse:
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

    ReviewRequest:
      type: object
      properties:
        content:
          type: string
        user_info:
          type: object
          properties:
            name:
              type: string
            email:
              type: string
      required:
        - content
        - user_info

    ReviewResponse:
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

    ErrorResponse:
      type: object
      properties:
        detail:
          type: string
