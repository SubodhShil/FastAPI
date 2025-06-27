import models
from models import meta

async def create_tables_data():
    """Return data needed for creating tables."""
    return {
        "message_start": "Creating tables...",
        "message_success": "✅ Tables created successfully.",
        "message_error": "❌ Error creating tables: {error}"
    } 