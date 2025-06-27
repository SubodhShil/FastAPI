async def update_data_config():
    """Return data needed for updating records."""
    return {
        "fields": ["name", "age", "gender", "email", "phone", "address", "city", "state"],
        "prompts": {
            "id": "Enter the ID of the student to update: ",
            "field": "Select the field to update: ",
            "value": "Enter the new value: "
        },
        "message_success": "✅ Student updated successfully.",
        "message_not_found": "❌ Student with ID {id} not found.",
        "message_error": "❌ Error updating student: {error}"
    } 