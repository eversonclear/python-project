# views.py
from django.shortcuts import render
from django.http import JsonResponse


def swagger_ui(request):
    return render(request, "swagger_ui.html")


def swagger_json(request):
    json_schema = {
        "openapi": "3.0.0",
        "info": {
            "title": "API DOCS",
            "version": "1.0.0",
            "description": "Python Project API Documentation",
        },
        "paths": {
            "/api/login": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Login user",
                    "description": "Endpoint to authenticate a user and generate JWT token.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {
                                            "type": "string",
                                            "format": "password",
                                        },
                                    },
                                    "required": ["email", "password"],
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Successful login",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "email": {"type": "string"},
                                            "token": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"},
                    },
                }
            },
            "/api/signup": {
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Signup user",
                    "description": "Endpoint to register a new user.",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string", "format": "email"},
                                        "password": {
                                            "type": "string",
                                            "format": "password",
                                        },
                                        "first_name": {"type": "string"},
                                        "last_name": {"type": "string"},
                                    },
                                    "required": ["email", "password"],
                                }
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "User created",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "email": {"type": "string"},
                                            "token": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        },
                        "400": {"$ref": "#/components/responses/BadRequest"},
                    },
                }
            },
            "/api/tasks": {
                "get": {
                    "tags": ["Tasks"],
                    "security": [{"bearerAuth": []}],
                    "summary": "List tasks",
                    "responses": {
                        "200": {
                            "description": "Tasks List",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Task"},
                                    }
                                }
                            },
                        }
                    },
                },
                "post": {
                    "tags": ["Tasks"],
                    "security": [{"bearerAuth": []}],
                    "summary": "Create task",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TaskInput"}
                            }
                        }
                    },
                    "responses": {"201": {"description": "Tarefa criada"}},
                },
            },
            "/api/tasks/{id}": {
                "get": {
                    "tags": ["Tasks"],
                    "security": [{"bearerAuth": []}],
                    "summary": "Task Details",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Task"}
                                }
                            },
                        }
                    },
                },
                "put": {
                    "tags": ["Tasks"],
                    "security": [{"bearerAuth": []}],
                    "summary": "Update task",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/TaskInput"}
                            }
                        }
                    },
                    "responses": {"200": {"description": "Tarefa atualizada"}},
                },
                "delete": {
                    "tags": ["Tasks"],
                    "security": [{"bearerAuth": []}],
                    "summary": "Delete task",
                    "responses": {"204": {"description": "Task deleted"}},
                },
            },
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "responses": {
                "BadRequest": {
                    "description": "Bad request",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {"error": {"type": "string"}},
                            }
                        }
                    },
                }
            },
            "schemas": {
                "Task": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "complete": {"type": "boolean"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "TaskInput": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "complete": {"type": "boolean"},
                    },
                    "required": ["title", "description", "complete"],
                },
            },
        },
    }

    return JsonResponse(json_schema)
