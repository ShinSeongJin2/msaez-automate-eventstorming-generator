create_command_wire_frame_inputs = {
    "commandName": "CreateBook",
    "commandDisplayName": "Create Book",
    "fields": [
        {
            "name": "title",
            "type": "string",
            "required": True
        },
        {
            "name": "author",
            "type": "string",
            "required": True
        },
        {
            "name": "publishedDate",
            "type": "date",
            "required": True
        }
    ],
    "api": "POST /books",
    "additionalRequirements": "Make a ui for the CreateBook command"
}