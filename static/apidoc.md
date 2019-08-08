YADS REST-API documentation
===========================

Current prefix for api: `/api/v1.0/`
##### User data:
1. `/<uid>/: [GET]         ` - Get full profile data
1. `/<uid>/age : [GET, PUT]    ` - User's age
1. `/<uid>/gender : [GET, PUT]` - Users' gender
1. `/<uid>/sex_pref : [GET, PUT]` - User's sex preference
1. `/<uid>/biography : [GET, PUT]` - User's biography
1. `/<uid>/tags : [GET]` - Get user's tags
1. `/<uid>/tags/tag : [GET, PUT, DELETE]`
    + `GET` - return true if tag exists for this user
    + `PUT` - add new tag for user
    + `DELETE` - remove tag for user, if exist
1. `/<uid>/photos : [GET, PUT]`
    + `GET` - get a list of links to all profile photos
    + `PUT` - add a new photo
1. `/<uid>/photos/<phid> : [GET, DELETE]`
    + `GET` - get a photo
    + `DELETE` - delete a photo
1. `/<uid>/geo : [GET, PUT]`
    + `GET` - get user's geoposition
    + `PUT` - set new geoposition
1. `/<uid>/rating : [GET]`

#### User action
1. `/like/<uid> : [GET, PUT, DELETE]`
    + `GET` - return true if like exists
    + `PUT` - add like
    + `DELETE` - remove like
1. `/favorites/ : [GET]` - Get all likes
1. `/connected/ : [GET]` - Get all connected users

## Notice
Chat system work on WebSocket and not included to API