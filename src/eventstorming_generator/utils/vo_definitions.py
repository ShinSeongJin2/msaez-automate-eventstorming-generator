VODefinitions = {
    "Money": [
        {
            "className": "Double",
            "isKey": False,
            "label": "- amount: Double",
            "name": "amount",
            "nameCamelCase": "amount",
            "namePascalCase": "Amount",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- currency: String",
            "name": "currency",
            "nameCamelCase": "currency",
            "namePascalCase": "Currency",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Email": [
        {
            "className": "String",
            "isKey": False,
            "label": "- email: String",
            "name": "email",
            "nameCamelCase": "email",
            "namePascalCase": "Email",
            "_type": "org.uengine.model.FieldDescriptor",
        }
    ],
    "Likes": [
        {
            "className": "Boolean",
            "isKey": False,
            "label": "- isLiked: Boolean",
            "name": "isLiked",
            "nameCamelCase": "isLiked",
            "namePascalCase": "IsLiked",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "File": [
        {
            "className": "String",
            "isKey": False,
            "label": "- fileName: String",
            "name": "fileName",
            "nameCamelCase": "fileName",
            "namePascalCase": "FileName",
            "_type": "org.uengine.model.FieldDescriptor",
            "isLob": True,
            "isVO": False,
            "isList": False,
            "isName": False,
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- file: String",
            "name": "file",
            "nameCamelCase": "file",
            "namePascalCase": "File",
            "_type": "org.uengine.model.FieldDescriptor",
            "isLob": True,
            "isVO": False,
            "isList": False,
            "isName": False,
        },
    ],
    "Payment": [
        {
            "className": "String",
            "isKey": False,
            "label": "- paymentType: String",
            "name": "paymentType",
            "nameCamelCase": "paymentType",
            "namePascalCase": "PaymentType",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "Double",
            "isKey": False,
            "label": "- amount: Double",
            "name": "amount",
            "nameCamelCase": "amount",
            "namePascalCase": "Amount",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Photo": [
        {
            "className": "String",
            "isKey": False,
            "label": "- imgName: String",
            "name": "imgName",
            "nameCamelCase": "imgName",
            "namePascalCase": "ImgName",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- imgFile: String",
            "name": "imgFile",
            "nameCamelCase": "imgFile",
            "namePascalCase": "ImgFile",
            "_type": "org.uengine.model.FieldDescriptor",
            "isLob": True,
        },
    ],
    "Tags": [
        {
            "className": "List<String>",
            "isKey": False,
            "label": "- tag: List<String>",
            "name": "tag",
            "nameCamelCase": "tag",
            "namePascalCase": "Tag",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "User": [
        {
            "className": "String",
            "isKey": False,
            "label": "- userId: String",
            "name": "userId",
            "nameCamelCase": "userId",
            "namePascalCase": "UserId",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- password: String",
            "name": "password",
            "nameCamelCase": "password",
            "namePascalCase": "Password",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- name: String",
            "name": "name",
            "nameCamelCase": "name",
            "namePascalCase": "Name",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- email: String",
            "name": "email",
            "nameCamelCase": "email",
            "namePascalCase": "Email",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- address: String",
            "name": "address",
            "nameCamelCase": "address",
            "namePascalCase": "Address",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- phone: String",
            "name": "phone",
            "nameCamelCase": "phone",
            "namePascalCase": "Phone",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Weather": [
        {
            "className": "Double",
            "isKey": False,
            "label": "- degree: Double",
            "name": "degree",
            "nameCamelCase": "degree",
            "namePascalCase": "Degree",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "Double",
            "isKey": False,
            "label": "- precipitation: Double",
            "name": "precipitation",
            "nameCamelCase": "precipitation",
            "namePascalCase": "Precipitation",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "Double",
            "isKey": False,
            "label": "- humidity: Double",
            "name": "humidity",
            "nameCamelCase": "humidity",
            "namePascalCase": "Humidity",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "Double",
            "isKey": False,
            "label": "- wind: Double",
            "name": "wind",
            "nameCamelCase": "wind",
            "namePascalCase": "Wind",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Address": [
        {
            "className": "String",
            "isKey": False,
            "label": "- street: String",
            "name": "street",
            "nameCamelCase": "street",
            "namePascalCase": "Street",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- city: String",
            "name": "city",
            "nameCamelCase": "city",
            "namePascalCase": "City",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- state: String",
            "name": "state",
            "nameCamelCase": "state",
            "namePascalCase": "State",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- country: String",
            "name": "country",
            "nameCamelCase": "country",
            "namePascalCase": "Country",
            "_type": "org.uengine.model.FieldDescriptor",
        },
        {
            "className": "String",
            "isKey": False,
            "label": "- zipcode: String",
            "name": "zipcode",
            "nameCamelCase": "zipcode",
            "namePascalCase": "ZipCode",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Comment": [
        {
            "className": "List<String>",
            "isKey": False,
            "label": "- content: List<String>",
            "name": "content",
            "nameCamelCase": "content",
            "namePascalCase": "Content",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
    "Rating": [
        {
            "className": "List<String>",
            "isKey": False,
            "label": "- content: List<String>",
            "name": "content",
            "nameCamelCase": "content",
            "namePascalCase": "Content",
            "_type": "org.uengine.model.FieldDescriptor",
        },
    ],
}