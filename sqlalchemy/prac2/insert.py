async def insert_data_values():
    """Return data needed for inserting records."""
    return {
        "sample_data": {
            "name": "John Doe",
            "age": 20,
            "gender": "Male",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "city": "Anytown",
            "state": "CA",
        },
        "message_success": "✅ Data inserted successfully.",
        "message_error": "❌ Error inserting data: {error}"
    } 