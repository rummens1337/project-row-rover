# Socket and API documentation

## API

The API (application programming interface) can be accesed thru `http://<IP>:<PORT>/api`
all communication with the API must be acomplised using the *api_key*. The value of this key can be seen at `./settings.conf` *> [server] > api_key*. The API key must be send as a parameter named `key` with the key value as a string.

The API server returns all request in JSON format, consisting of:

* `status` HTTP status code
* `message` HTTP status message
* `description` HTTP status description
* `data` data requested, empty if no data is requested or available


### Requests

#### Get version
A get request can be performed at the root of the api endpoint to request the current version of the application.

* Endpoint: `/`
* Methode: GET
* Parameter: None
* Returns: current version as a string

Example:
```
➜  ~ curl <IP>:<PORT>/api -d "key=<KEY>" -X GET
{"description": "Request was successful.", "status": 200, "data": {"version": "0.0.1-Alderaan"}, "message": "OK"}
```

#### Get motor status
Get the current speed of both (left, right) motors

* Endpoint: `/motor`
* Methode: GET
* Parameter: None
* Returns: left and right motor speed.

Example:
```
➜  ~ curl <IP>:<PORT>/api/motor -d "key=<KEY>" -X GET
{"description": "Request was successful.", "status": 200, "data": {"motor": [{"side": "left", "speed": 0, "value": 0}, {"side": "right", "speed": 0, "value": 0}]}, "message": "OK"}

```

#### Set motor values
Set the speed of the motors.

* Endpoint: `/motor`
* Methode: Put
* Parameters: *left* (optional) and *right* (optional), both containing a uint8
* Returns: None

Example:
```
➜  ~ curl <IP>:<PORT>/api/motor -d "key=<KEY>" -d "right=-123" -d "left=10" -X PUT
{"description": "Request was successful.", "status": 200, "data": "", "message": "OK"}

```

### On failure
The api gives a 400 error if the request is not valid, and a 500 error if the server encounters an internal server error.


## Socket
The socket allows for an continuos connection between the server and the client. The interface is very simular of the API. A connection is made with the socket by connecting to `ws://<IP>:<PORT>`. All communication over the websocket is done with JSON.

**Request contains**:
* `key` *api_key* of the application, found at `./settings.conf` *> [server] > api_key*. 
* `request` type of request.
* `data` (optional) data to send to the server

**Response contains**
* `status` HTTP status code
* `message` HTTP status message
* `description` HTTP status description
* `data` data requested, empty if no data is requested or available

### Requests

#### Get current version
Get the version of the application

* Request: `status`
* Data: None
* Returns: current version as a string

Example:
```
> {"request": "status", "key": "<KEY>"}
< {"status": 200, "description": "Request was successful.", "data": {"version": "0.0.1-Alderaan"}, "message": "OK"} 
```

#### Get motor values 
Get the current speed of both (left, right) motors

* Request: `motor`
* Data: None
* Returns: left and right motor speed values.

Example:
```
> {"key": "<KEY>", "request": "motor"}
< {"description": "Request was successful.", "status": 200, "data": {"motor": [{"side": "left", "speed": 0, "value": -10}, {"side": "right", "speed": 0, "value": 123}]}, "message": "OK"}
```

#### Set motor values
Set the speed of the motors.

* Request: `motor`
* Data: `left`(optional) motor speed left, `right`(optional) motor speed right. Both in unit8
* Returns: none

Example:
```
> {"key": "<KEY>", "request": "motor", "data":{"left": 10, "right": 255}}
< {"description": "Request was successful.", "status": 200, "data": "", "message": "OK"}
```

#### Toggle flashlight
Set the flashlight on or off.

* Request: `lamp`
* Data: 1 (on), 0 (off)
* Returns: none

Example:
```
> {"key": "<KEY>", "request": "lamp", "data":1}
< {"description": "Request was successful.", "status": 200, "data": "", "message": "OK"}
```
#### Get flashlight status
see the pin that is connected to the flashlight and if its on.

* Request: `lamp`
* Data: None
* returns: status of the flashlight (1: on, 0: off) and the pin.

Example:
```
> {"request": "lamp", "key": "<KEY>"}
< {"status": 200, "description": "Request was successful.", "data": {"lamppin": 7, "lampmode": 0}, "message": "OK"}
```

#### Display message on display
Display a 16*2(32) set of characters on the display of the rover.

* Request: `displayMsg`
* Data: string of text (max 32 characters)
* Returns: none

Example:
```
> {"key": "<KEY>", "request": "displayMsg", "data":"hello, world!"}
< {"description": "Request was successful.", "status": 200, "data": "", "message": "OK"}
```

#### get battery status
Get the battery percentage of the rover (0-100)

* Request: `battery`
* Data: None
* Returns: int (0-100)

Example:
```
> {"key": "<KEY>", "request": "battery", "data":""}
< {"description": "Request was successful.", "status": 200, "data": "57", "message": "OK"}
```

## On failure
the socket closes the connection on a failed request (400) or on an internal server error (500). More detail about the failer can be read in the `data` section of the message.