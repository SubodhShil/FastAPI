async def read_data_config():
    """Return data needed for reading records."""
    return {
        "message_header": "📝 Students data:",
        "message_empty": "No students found in the database.",
        "message_error": "❌ Error reading data: {error}"
    } 