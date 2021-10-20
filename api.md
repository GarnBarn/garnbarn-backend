# GarnBarn API Documentation

This Document contain the API structure of GarnBarn API

### Endpoint Structure

```
{PREFIX}/api/v{API_VERSION}/{END_POINT}...
```

Definition:

- PREFIX: is the address where you host this API
- API_VERSION: is the version of the API (See the versions list in the doc below)
- END_POINT: See the detail in the doc below to see the available end point.

Example of the fully assembled API endpoint:

```
https://garnbarn.example/api/v1/assignments
```

_Note: https://garnbarn.example is an example PREFIX. Please don't send any request to this prefix_

### Available API Version List

| Version   | Availability |
| :-------- | :----------: |
| [v1](#v1) |      ✅      |

# v1

## Definitions

- `ID Token` : The user authortization token from GarnBarn Frontend. It is used to identify the user and authorize the request

## Assignment API

### Get Assignment API

This API return the specific Assignment Object related to the Assignment ID passed in the request body.

#### HTTP Request

`GET /api/v1/assignments/{assignmentId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       |  Type  | Description           |
| :-------------------------: | :--------------- | :----: | :-------------------- |
| ![Required][required_badge] | **assignmentId** | String | The ID of assignment. |

Example request:

```bash
curl -v -X GET {PREFIX}/api/v1/assignments/{assignmentId}/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response

Return status code `200` and [Assignment Object](#assignment-object)

Example response:

```JSON
{
    "assignmentId": "1",
    "name": "Example Assignment",
    "description": "This is example",
    "dueDate": 1634745493,
    "tagId": "1234",
}
```

#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Assignment not found"
}
```

### Create Assignment API

This API will create the assignment in the Database.

#### HTTP Request

`POST /api/v1/assignments/`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Request body**

|                             | Parameters  |  Type  | Description                                                   |
| :-------------------------: | :---------- | :----: | :------------------------------------------------------------ |
| ![Required][required_badge] | **name**    | String | The name of the new assignment.                               |
| ![Optional][optional_badge] | **dueDate** | Number | The due date of the new assignment specifed as **Timestamp**. |
| ![Optional][optional_badge] | **tagId**   | String | The tag id that this assignment will be assgiened to.         |

Example request:

```bash
curl -v -X POST {PREFIX}/api/v1/assignments/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "name": "Example",
    "dueDate": 1634745493,
    "tagId": "1234"
}'
```

#### Response

Return status code `200` and the new assignment id

Example response:

```JSON
{
    "assignmentId": "1",
}
```

#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Assignment not found"
}
```

## Object Structure

### Assignment Object

|                             | Parameters       |  Type  | Value                                                              |
| :-------------------------: | :--------------- | :----: | :----------------------------------------------------------------- |
| ![Required][required_badge] | **assignmentId** | String | The ID of assignment.                                              |
| ![Required][required_badge] | **name**         | String | The name of assignment.                                            |
| ![Optional][optional_badge] | **description**  | String | Assignment description.                                            |
| ![Optional][optional_badge] | **dueDate**      | Number | The due date of the current assignment presented as **Timestamp**. |
| ![Optional][optional_badge] | **tagId**        | String | The tag id that this assignment has been assgiened to.             |

## Error responses in Common specifications

_To be specified_

[required_badge]: https://img.shields.io/badge/-Required-ff6c5e?style=flat-square
[optional_badge]: https://img.shields.io/badge/-Optional-c9c9c9?style=flat-square
