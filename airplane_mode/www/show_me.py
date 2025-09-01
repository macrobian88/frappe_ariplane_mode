import frappe
def get_context(context):
    color = frappe.form_dict.color or "black"
    context.color = color
    return context
