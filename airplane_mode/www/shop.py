import frappe

def get_context(context):
    shop_name = frappe.form_dict.name
    context.shop = frappe.get_doc("Airport Shop", shop_name)
