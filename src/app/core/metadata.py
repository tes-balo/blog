# app/core/metadata.py

from typing import Any

description = """
Blog App API provides you with a robust set of functionalitites for managing a blog app. 

## Posts

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata: list[dict[str, str]] = [
    {
        "name": "Authentication",
        "description": "Operations related to login and token generation.",
    },
    {
        "name": "Users",
        "description": "Manage users in the system.",
    },
    {
        "name": "Blog Posts",
        "description": "Create, read, update and delete blog posts.",
    },
]

api_metadata: dict[str, Any] = {
    "title": "Blog App",
    "description": description,
    "summary": "Deadpool's favorite app. Nuff said.",
    "version": "0.0.1",
    "terms_of_service": "http://example.com/terms/",
    "contact": {
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "teslimb36@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    "openapi_tags": tags_metadata,
}
