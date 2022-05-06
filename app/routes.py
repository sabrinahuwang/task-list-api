from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Create a task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({
            "details": "Invalid data"
            }, 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(
        jsonify({
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": new_task.completed_at is not None
            }
        }), 
        201)


# Getting saved tasks/ no saved tasks
@tasks_bp.route("", methods=["GET"])
def getting_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        })
    return jsonify(tasks_response)


# Get one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response({}, 404)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }


# Update task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    request_body = request.get_json()
    task = Task.query.get(task_id)
    if task is None:
        return make_response({}, 404)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }


# Delete task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response({}, 404)
    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        })


