xml_util_inputs = {
	"command_name": "RegisterUser",
	"command_display_name": "User Registration", 
	"fields": [
		{
			"name": "email",
			"type": "String", 
			"required": True
		},
		{
			"name": "password",
			"type": "String",
			"required": True
		},
		{
			"name": "confirmPassword", 
			"type": "String",
			"required": True
		},
		{
			"name": "acceptTerms",
			"type": "Boolean", 
			"required": True
		}
	],
	"api": "POST /users/register",
	"additional_requirements": "Add password strength indicator and terms of service link"
}