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
https://garnbarn.example/api/v1/assignment/
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

### Get Assignment

This API return the specific Assignment Object related to the Assignment ID passed in the request body.

#### Permission

- User must have permission to view the requested Assignment </br> (By being the **owner of the assignment** or the **subscriber of the Tag** that the Assignment has been assigned).

#### HTTP Request

`GET /api/v1/assignment/{assignmentId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       | Description           |
| :-------------------------: | :--------------- | :-------------------- |
| ![Required][required_badge] | **assignmentId** | The ID of assignment. |

Example request:

```bash
curl -v -X GET {PREFIX}/api/v1/assignment/{assignmentId}/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response

Return status code `200` and [Assignment Object](#assignment-object)

Example response:

```JSON
{
    "id": 1,
    "name": "Example Assignment",
    "author": "0000000000000000000000000000",
    "description": "This is example",
    "dueDate": 1634745493,
    "tag": {
        "id": 1,
        "name": "ISP",
        "color": "#4285F4"
    },
    "reminderTime": [
        1,
        2,
        3
    ]
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

---

### Get All Assignments

This API return the specific Assignment Object related to the Assignment ID passed in the request body.

#### Permission

- User must have permission to view the requested Assignment </br> (By being the **owner of the assignment** or the **subscriber of the Tag** that the Assignment has been assigned).

#### HTTP Request

`GET /api/v1/assignment/`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**URL parameters**

|                             | Parameters      |  type   | Description                                                                           |
| :-------------------------: | :-------------- | :-----: | :------------------------------------------------------------------------------------ |
| ![Optional][optional_badge] | **fromPresent** | str     | If 'true', The API will return only the assignment that dueDate >= today (Focus on Day) |

Example request:

```bash
curl -v -X GET {PREFIX}/api/v1/assignment/{assignmentId}/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response

Return status code `200` and [Assignment Object](#assignment-object)

Example response:

```JSON
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "0000000000000000000000000000",
            "tag": null,
            "author": ,
            "name": "Test",
            "dueDate": null,
            "timestamp": 1635261404498,
            "description": "Example!",
            "reminderTime": [
                1,
                2,
                3
            ]
        }
    ]
}
```

---

### Create Assignment

This API will create the assignment in the Database.

#### Permission

- Anyone that have the account in GarnBarn system.

#### HTTP Request

`POST /api/v1/assignment/`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Request body**

|                             | Parameters      |  Type  | Description                                                   |
| :-------------------------: | :-------------- | :----: | :------------------------------------------------------------ |
| ![Required][required_badge] | **name**        | String | The name of the new assignment.                               |
| ![Required][required_badge] | **author** | String | The uid of the user that create assignment.                                |
| ![Optional][optional_badge] | **description** | String | The description of assignment.                                |
| ![Optional][optional_badge] | **dueDate**     | Number | The due date of the new assignment specifed as **Timestamp**. |
| ![Optional][optional_badge] | **tagId**       | Number | The tag id that this assignment will be assgiened to.         |
| ![Optional][optional_badge] | **reminderTime**| List   | The list of all reminder time.                                |

Example request:

```bash
curl -v -X POST {PREFIX}/api/v1/assignment/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "name": "Example",
    "dueDate": 1634745493,
    "tagId": "1234"
}'
```

#### Response

Return status code `201` and the new [Assignment Object](#assignment-object)

Example response:

```JSON
{
    "id": 1,
    "name": "Example",
    "author": "0000000000000000000000000000",
    "dueDate": 1634745493,
    "tag": {
        "id": 1,
        "name": "tag",
        "author": "0000000000000000000000000000",
        "color": "#TTTTTT",
        "reminderTime": [
            1,
            2,
            3
        ],
        "subscriber": [
            1,
            2,
            3
        ]
    },
    "reminderTime": [
        1,
        2,
        3
    ]
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

### Delete Assignment

This API will delete the specifed assignment from the Database.

#### Permission

- User must be the **owner** of the requested Assignment.
- (OR) User must be the **subscriber** of the Tag the requested Assignment has been assigned.

#### HTTP Request

`DELETE /api/v1/assignment/{assignmentId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       | Description                              |
| :-------------------------: | :--------------- | :--------------------------------------- |
| ![Required][required_badge] | **assignmentId** | The ID of assignment you want to remove. |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |

Example request:

```bash
curl -v -X DELETE {PREFIX}/api/v1/assignment/{assignmentId} \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response

Return status code `200` and empty json.

Example response:

```JSON
{}
```

#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Assignment not found"
}
```

---

### Update Assignment

This API will update the specifed assignment that user was the author with the new detail.

#### Permission

- User must be the **owner** of the requested Assignment.
- (OR) User must be the **subscriber** of the Tag the requested Assignment has been assigned.

#### HTTP Request

`PATCH /api/v1/assignment/{assignmentId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       |  Type  | Description                              |
| :-------------------------: | :--------------- | :----: | :--------------------------------------- |
| ![Required][required_badge] | **assignmentId** | String | The ID of assignment you want to update. |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |

**Request body**

|                             | Parameters      |  Type  | Description                                                   |
| :-------------------------: | :-------------- | :----: | :------------------------------------------------------------ |
| ![Optional][optional_badge] | **name**        | String | The name of the new assignment.                               |
| ![Optional][optional_badge] | **description** | String | The description of assignment.                                |
| ![Optional][optional_badge] | **dueDate**     | Number | The due date of the new assignment specifed as **Timestamp**. |
| ![Optional][optional_badge] | **tagId**       | String | The tag id that this assignment will be assgiened to.         |
| ![Optional][optional_badge] | **reminderTime**| List   | The list of all reminder time.                                |


Example request:

```bash
curl -v -X PATCH {PREFIX}/api/v1/assignment/{assignmentId} \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "name": "Renamed Assignment"
}'
```

#### Response

Return status code `200` and the [Assignment Object](#assignment-object) of the assignment after the update.

Example response:

```JSON
{
    "id": 1,
    "name": "Renamed Assignment",
    "author": "0000000000000000000000000000",
    "description": "This is example",
    "dueDate": 1634745493,
    "tag": {
        "id": 1,
        "name": "ISP",
        "author": "0000000000000000000000000000",
        "color": "#4285F4",
        "reminderTime": [
            1,
            2,
            3
        ],
        "subscriber": [
            1,
            2,
            3
        ]
    },
    "reminderTime": [
        1,
        2,
        3
    ]
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

---

## Tag API

### Get Tag

This API return the specific Tag Object related to the Tag ID passed in te request body.    

#### HTTP Request

`GET /api/v1/tag/{tagId}`    

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       | Description           |
| :-------------------------: | :--------------- | :-------------------- |
| ![Required][required_badge] | **tagId** | The ID of tag. |

Example request:

```bash
curl -v -X GET {PREFIX}/api/v1/tag/{tagId}/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response
Return status code `200` and [Tag Object](#tag-object)    
Example response:

```JSON
{
    "id": 1,
    "name": "tag",
    "author": "0000000000000000000000000000",
    "color": "#TTTTTT",
    "reminderTime": [
        1,
        2,
        3
    ],
    "subscriber": [
        1,
        2,
        3
    ]
}
```
#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

---

### Create Tag
This API will create the tag in Database.

#### HTTP Request

`POST /api/v1/tag/`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters      |  Type  | Description                                                   |
| :-------------------------: | :-------------- | :----: | :------------------------------------------------------------ |
| ![Required][required_badge] | **name**        | String | The name of the new tag.                               |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |
| ![Optional][optional_badge] | **color**     | String | The color of the tag. |
| ![Optional][optional_badge] | **reminderTime**       | List: Int | The tag reminder time list.         |
| ![Optional][optional_badge] | **subscriber**| List   | The list of all subscriber that subscribe the tag.       

Example request:

```bash
curl -v -X POST {PREFIX}/api/v1/tag/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response
Return status code `201` and [Tag Object](#tag-object)    
Example response:

```JSON
{
    "id": 1,
    "name": "tag",
    "author": "0000000000000000000000000000",
    "color": "#TTTTTT",
    "reminderTime": [
        1,
        2,
        3
    ],
    "subscriber": [
        1,
        2,
        3
    ]
}
```
#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

---
### Delete Tag

This API will delete the specifed tag that user was author from the Database.

#### HTTP Request

`DELETE /api/v1/tag/{tagId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |

**Path parameters**

|                             | Parameters       | Description           |
| :-------------------------: | :--------------- | :-------------------- |
| ![Required][required_badge] | **tagId** | The ID of tag user want to remove. |


Example request:

```bash
curl -v -X DELETE {PREFIX}/api/v1/tag/{tagId}/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
```

#### Response
Return status code `200` and [Tag Object](#tag-object)    
Example response:

```JSON
{}
```
#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

---
### Update Tag
This API will update the specifed tag that user was the author or was subscribe to that tag 
with the new detail.

#### HTTP Request

`PATCH /api/v1/tag/{tagId}`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |
| ![Required][required_badge] | **subscriber**| List   | User must be in subscribe list. | 

**Path parameters**

|                             | Parameters       |  Type  | Description                              |
| :-------------------------: | :--------------- | :----: | :--------------------------------------- |
| ![Required][required_badge] | **tagId** | String | The ID of tag you want to update. |

**Request body**

|                             | Parameters      |  Type  | Description                                                   |
| :-------------------------: | :-------------- | :----: | :------------------------------------------------------------ |
| ![Optional][optional_badge] | **name**        | String | The name of the new tag.                               |
| ![Optional][optional_badge] | **color** | String | The color of assignment.                                |
| ![Optional][optional_badge] | **reminderTime**     | List | The list of all reminder time. |
| ![Optional][optional_badge] | **subscriber**       | List | The list of all subscriber.         |


Example request:

```bash
curl -v -X PATCH {PREFIX}/api/v1/tag/{tagId} \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "name": "Renamed tag"
}'
```

#### Response
Return status code `200` and [Tag Object](#tag-object)    
Example response:

```JSON
{
    "id": 1,
    "name": "Renamed tag",
    "author": "0000000000000000000000000000",
    "color": "#TTTTTT",
    "reminderTime": [
        1,
        2,
        3
    ],
    "subscriber": [
        1,
        2,
        3
    ]
}
```
#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

### Subscribe Tag
This API will subscribe the specifed tag that user want to subscribe.

#### HTTP Request
`POST /api/v1/tag/{tagId}/subscribe`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       |  Type  | Description                              |
| :-------------------------: | :--------------- | :----: | :--------------------------------------- |
| ![Required][required_badge] | **tagId** | String | The ID of tag you want to subscribe. |
| ![Required][required_badge] | **TOTP** | String | The TOTP code of tag you want to subscribe. |

Example request:

```bash
curl -v -X POST {PREFIX}/api/v1/tag/{tagId}/subscribe \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "subscriber": "1111111111111111111111111111"
}'
```

#### Response
Return status code `200` and [Tag Object](#tag-object)    
Example response:

```JSON
{
    "id": 1,
    "name": "ISP",
    "author": "0000000000000000000000000000",
    "color": "#TTTTTT",
    "reminderTime": [
        1,
        2,
        3
    ],
    "subscriber": [
        11111111111111111111111111111
    ]
}
```

#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

### Unsubscribe Tag
This API will unsubscribe the specifed tag that user want to unsubscribe.

#### HTTP Request
`POST /api/v1/tag/{tagId}/unsubscribe`

**Request headers**

|                             | Parameters        | Value               |
| :-------------------------: | :---------------- | ------------------- |
| ![Required][required_badge] | **Content-Type**  | application/json    |
| ![Required][required_badge] | **Authorization** | Bearer `{ID Token}` |

**Path parameters**

|                             | Parameters       |  Type  | Description                              |
| :-------------------------: | :--------------- | :----: | :--------------------------------------- |
| ![Required][required_badge] | **tagId** | String | The ID of tag you want to subscribe. |

Example request:

```bash
curl -v -X POST {PREFIX}/api/v1/tag/{tagId}/subscribe \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer {ID Token}' \
-d '{
    "subscriber": []
}'
```

#### Response
Return status code `200` and [Tag Object](#tag-object)    
Example response:

```JSON
{
    "id": 1,
    "name": "ISP",
    "author": "0000000000000000000000000000",
    "color": "#TTTTTT",
    "reminderTime": [
        1,
        2,
        3
    ],
    "subscriber": [
    ]
}
```

#### Error

Returns a `40x` HTTP status code and an error response. For more information, see [Error responses in Common specifications](#error-responses-in-common-specifications).

Example error response:

```JSON
{
    "message": "Tag not found"
}
```

---

## Object Structure

### Assignment Object

|                             | Parameters      |           Type            | Value                                                              |
| :-------------------------: | :-------------- | :-----------------------: | :----------------------------------------------------------------- |
| ![Required][required_badge] | **id**          |          Number           | The ID of assignment.                                              |
| ![Required][required_badge] | **name**        |          String           | The name of assignment.                                            |
| ![Required][required_badge] | **author**      |          String           | The Firebase Auth UID of the assignment author.                    |
| ![Optional][optional_badge] | **description** |          String           | Assignment description.                                            |
| ![Optional][optional_badge] | **dueDate**     |          Number           | The due date of the current assignment presented as **Timestamp**. |
| ![Optional][optional_badge] | **tag**         | [Tag Object](#tag-object) | The tag object that this assignment has been assgiened to.         |

### Tag Object

|                             | Parameters |  Type  | Value                      |
| :-------------------------: | :--------- | :----: | :------------------------- |
| ![Required][required_badge] | **id**     | Number | The ID of the Tag.         |
| ![Required][required_badge] | **name**   | String | The name of the Tag.       |
| ![Required][required_badge] | **author** | String | The uid of the user that create tag.                                |
| ![Optional][optional_badge] | **color**  | String | Hex color code of the tag. |
| ![Optional][optional_badge] | **reminderTime**       | List: Int | The tag reminder time list.         |
| ![Optional][optional_badge] | **subscriber**| List   | The list of all subscriber that subscribe the tag.      |

## Error responses in Common specifications

_To be specified_

[required_badge]: https://img.shields.io/badge/-Required-ff6c5e?style=flat-square
[optional_badge]: https://img.shields.io/badge/-Optional-c9c9c9?style=flat-square
