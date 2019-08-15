YADS REST-API documentation
===========================

Current prefix for api: `/api/v1.0/`
##### User data:
1. `/<uid>/: [GET]         ` - Get full profile data
1. `/<uid>/age : [GET]    ` - User's age
1. `/<uid>/gender : [GET]` - Users' gender
1. `/<uid>/sex_pref : [GET]` - User's sex preference
1. `/<uid>/biography : [GET]` - User's biography
1. `/<uid>/tags : [GET]` - Get user's tags
1. `/<uid>/geo: [GET]` - Get user's geo
1. `/<uid>/photos : [GET]` - get a list of links to all profile photos
1. `/<uid>/rating : [GET]` - get user's rating
1. `/<uid>/online : [GET]` - get user's online status

#### User action
1. `/like/<uid> : [GET, PUT, DELETE]`
    + `GET` - return true if like exists
    + `PUT` - add like
    + `DELETE` - remove like
1. `/favorites/ : [GET]` - Get all likes
1. `/connected/ : [GET]` - Get all connected users
1. `/search/ : [POST]` - find users by criteria

    `{`
    
    `age-min: <int>`
    
    `age-max: <int>`
    
    `rating-min: <int>`
    
    `rating-max: <int>`
    
    `geo: <string>`
    
    `tags: [tags1, tags2, tags3]`
    
    `}`
    
1. `/login : POST`
1. `/signup: POST`

## Notice
Chat system work on WebSocket and not included to API