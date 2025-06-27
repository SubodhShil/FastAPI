async def delete_data_config():
    """Return data needed for deleting records."""
    return {
        "prompts": {
            "id": "Enter the ID of the student to delete: ",
            "confirm": "Are you sure you want to delete this student? "
        },
        "message_success": "✅ Student deleted successfully.",
        "message_not_found": "❌ Student with ID {id} not found.",
        "message_error": "❌ Error deleting student: {error}"
    } 