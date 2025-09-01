import frappe

def get_context(context):
    # Fetch shops with required fields
    context.shops = frappe.get_all(
        "Airport Shop",
        fields=["name", "shop_name", "airport", "shop_type", "is_occupied"]
    )
